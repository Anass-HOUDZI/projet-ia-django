import io
import json
from html import escape as html_escape

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .models import Conversation, Message
from .services import HIDDEN_CONTEXT_RE, ChatbotService

def chat_view(request):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="testuser", defaults={"nationality": "Inconnue"})
    conversation, _ = Conversation.objects.get_or_create(user=user, title="Mon Assistant IA")

    # Strip hidden context from displayed messages (old messages saved before the fix may contain it)
    messages = []
    for msg in conversation.messages.all().order_by('timestamp'):
        msg.content = HIDDEN_CONTEXT_RE.sub('', msg.content).strip()
        messages.append(msg)

    return render(request, 'ai/chat.html', {'conversation': conversation, 'messages': messages})

def export_conversation_pdf(request, conversation_id):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="testuser", defaults={"nationality": "Inconnue"})

    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
    except Conversation.DoesNotExist:
        raise Http404

    messages = list(conversation.messages.exclude(role='system').order_by('timestamp'))

    # Ask AI for a structured summary
    chatbot = ChatbotService()
    summary_text = chatbot.summarize_conversation(messages)

    # Build PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'PDFTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#2F5D50'),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        'PDFSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=22,
    )
    section_style = ParagraphStyle(
        'PDFSection',
        parent=styles['Normal'],
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2F5D50'),
        spaceBefore=16,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        'PDFBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1F2937'),
        leftIndent=16,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        'PDFBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6,
    )
    error_style = ParagraphStyle(
        'PDFError',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#B91C1C'),
        spaceAfter=10,
    )

    now = timezone.now()
    story = [
        Paragraph("Résumé de votre consultation — Le Barista", title_style),
        Paragraph(
            f"Généré le {now.strftime('%d/%m/%Y à %H:%M')} · Café des Nations",
            subtitle_style,
        ),
        Spacer(1, 0.3 * cm),
    ]

    if summary_text is None:
        story.append(Paragraph(
            "Impossible de générer le résumé pour le moment. Réessayez plus tard.",
            error_style,
        ))
    else:
        for line in summary_text.splitlines():
            stripped = line.strip()
            if not stripped:
                story.append(Spacer(1, 0.15 * cm))
            elif stripped.startswith('## '):
                story.append(Paragraph(html_escape(stripped[3:]), section_style))
            elif stripped.startswith('- '):
                story.append(Paragraph(f"• {html_escape(stripped[2:])}", bullet_style))
            else:
                story.append(Paragraph(html_escape(stripped), body_style))

    doc.build(story)
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"resume-barista-{conversation_id}.pdf",
        content_type='application/pdf',
    )


@csrf_exempt
def send_message(request):
    """
    API endpoint to receive a message and return the AI's response.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation_id = data.get('conversation_id')
            content = data.get('content', '')
            # hidden_context is injected by the frontend for AI context only — never stored in DB
            hidden_context = data.get('hidden_context', '')
            image_base64 = data.get('image_base64')

            conversation = Conversation.objects.get(id=conversation_id)

            # Save the clean message (no hidden context) so it never leaks into the UI or PDF
            Message.objects.create(conversation=conversation, role='user', content=content)

            # The AI receives content + hidden context; generate_response skips the last DB
            # message when current_message is provided, so there is no duplication.
            full_for_ai = content + hidden_context
            chatbot = ChatbotService()
            ai_response = chatbot.generate_response(
                conversation,
                current_message=full_for_ai if full_for_ai else None,
                image_base64=image_base64,
            )
            
            return JsonResponse({'status': 'success', 'reply': ai_response})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
