from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CommunityPost, CommunityReply, CommunityCategory

def index_view(request):
    """
    Renders the community landing page with database posts & Discord bot integration.
    """
    if CommunityPost.objects.count() == 0:
        seed_initial_community_posts()
        
    posts = CommunityPost.objects.all().prefetch_related('replies')
    return render(request, 'community/index.html', {'db_posts': posts})

@csrf_exempt
def api_posts(request):
    """
    GET: List all posts from SQLite DB.
    POST: Create a new post & bridge notification to Discord Bot Webhook.
    """
    if CommunityPost.objects.count() == 0:
        seed_initial_community_posts()

    if request.method == 'GET':
        posts = CommunityPost.objects.all().prefetch_related('replies')
        data = [{
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'category_slug': p.category_slug,
            'author_name': p.author_name,
            'author_role': p.author_role,
            'author_avatar': p.author_avatar,
            'likes_count': p.likes_count,
            'replies_count': p.replies.count(),
            'created_at': p.created_at.strftime("%d %b %Y, %H:%M"),
            'sent_to_discord': p.sent_to_discord,
            'replies': [{
                'id': r.id,
                'author_name': r.author_name,
                'author_role': r.author_role,
                'author_avatar': r.author_avatar,
                'content': r.content,
                'is_official_answer': r.is_official_answer,
                'created_at': r.created_at.strftime("%d %b %Y, %H:%M"),
            } for r in p.replies.all()]
        } for p in posts]
        return JsonResponse({'status': 'success', 'posts': data})

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            title = body.get('title')
            content = body.get('content')
            category_slug = body.get('category_slug', 'demarches')
            author_name = body.get('author_name', 'Habitué')
            
            if not title or not content:
                return JsonResponse({'status': 'error', 'message': 'Titre et contenu obligatoires'}, status=400)

            post = CommunityPost.objects.create(
                title=title,
                content=content,
                category_slug=category_slug,
                author_name=author_name,
                author_role="Nouveau membre",
                author_avatar="☕"
            )

            # Bot Discord Notification Bridge
            discord_sent = post.notify_discord_bot()

            return JsonResponse({
                'status': 'success',
                'post_id': post.id,
                'sent_to_discord': discord_sent,
                'message': 'Question publiée en Grande Salle et transmise au Bot Discord !'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def api_like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(CommunityPost, id=post_id)
        post.likes_count += 1
        post.save(update_fields=['likes_count'])
        return JsonResponse({'status': 'success', 'likes_count': post.likes_count})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def api_add_reply(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(CommunityPost, id=post_id)
        try:
            body = json.loads(request.body)
            content = body.get('content')
            author_name = body.get('author_name', 'Habitué')
            
            if not content:
                return JsonResponse({'status': 'error', 'message': 'Contenu vide'}, status=400)

            reply = CommunityReply.objects.create(
                post=post,
                content=content,
                author_name=author_name,
                author_role="Habitué du Café",
                author_avatar="☕"
            )
            post.replies_count = post.replies.count()
            post.save(update_fields=['replies_count'])

            return JsonResponse({'status': 'success', 'reply_id': reply.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=400)

def seed_initial_community_posts():
    p1 = CommunityPost.objects.create(
        title="Combien de temps avant la fin de mon titre dois-je renouveler sur l'ANEF ?",
        content="Mon titre de séjour étudiant expire dans 2 mois. J'ai entendu dire qu'il faut le faire à J-90. Est-ce trop tard ou est-ce que j'aurai une attestation de prolongation d'instruction (API) rapidement ?",
        category_slug="demarches",
        author_name="Youssef M.",
        author_role="Habitué du Café",
        author_avatar="🎓",
        likes_count=18
    )
    CommunityReply.objects.create(
        post=p1,
        author_name="Le Barista IA",
        author_role="Assistant IA Officiel",
        author_avatar="👨‍🍳",
        content="Bonjour Youssef ! Il est recommandé d'initier la demande sur l'ANEF entre J-90 et J-60. À 2 mois de l'échéance (J-60), vous êtes parfaitement dans les temps ! Déposez votre dossier dès aujourd'hui pour obtenir votre Attestation de Dépôt puis votre API sans rupture de droits.",
        is_official_answer=True
    )

    p2 = CommunityPost.objects.create(
        title="Garantie Visale refusée car diplôme étranger ? Comment valider ?",
        content="J'essaie d'obtenir la caution Visale pour mon appartement à Lyon mais le site bloque sur la pièce justificative. Quel document avez-vous fourni pour débloquer le certificat ?",
        category_slug="logement",
        author_name="Amina K.",
        author_role="Membre Récent",
        author_avatar="🏠",
        likes_count=12
    )
    CommunityReply.objects.create(
        post=p2,
        author_name="Sarah L.",
        author_role="Mentor Logement",
        author_avatar="🔑",
        content="Il faut fournir votre certificat de scolarité provisoire ou votre attestation d'admission universitaire en France (Campus France), et votre visa VLS-TS avec tampon d'entrée !",
        is_official_answer=False
    )
