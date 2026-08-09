import json

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import CommunityPost, CommunityReply

def ensure_community_tables():
    """
    S'assure que les tables SQLite existent et sont peuplées, sinon exécute les migrations.
    """
    try:
        if CommunityPost.objects.count() == 0:
            seed_initial_community_posts()
    except Exception as e:
        try:
            call_command('migrate', 'community', interactive=False)
            if CommunityPost.objects.count() == 0:
                seed_initial_community_posts()
        except Exception as migrate_err:
            print("Auto migration community error:", migrate_err)

def index_view(request):
    """
    Renders the community landing page with database posts & Discord bot integration.
    """
    try:
        ensure_community_tables()
        posts = CommunityPost.objects.all().prefetch_related('replies')
    except Exception as e:
        print("Index view database recovery:", e)
        posts = []
    return render(request, 'community/index.html', {'db_posts': posts})

@csrf_exempt
def api_posts(request):
    """
    GET: List all posts from SQLite DB.
    POST: Create a new post & bridge notification to Discord Bot Webhook.
    """
    ensure_community_tables()

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

            # Creating CommunityPost fires Django post_save signal auto_notify_discord_on_create!
            post = CommunityPost.objects.create(
                title=title,
                content=content,
                category_slug=category_slug,
                author_name=author_name,
                author_role="Nouveau membre",
                author_avatar="☕"
            )

            return JsonResponse({
                'status': 'success',
                'post_id': post.id,
                'sent_to_discord': post.sent_to_discord,
                'message': 'Question publiée en Grande Salle et synchronisée automatiquement sur Discord !'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def api_discord_incoming_webhook(request):
    """
    Endpoint bidirectionnel Discord -> Site : Reçoit les messages postés sur Discord et les publie en Grande Salle.
    """
    ensure_community_tables()
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            content = body.get('content') or body.get('message') or body.get('title')
            username = body.get('username') or (body.get('author', {}).get('username') if isinstance(body.get('author'), dict) else 'Membre Discord')
            
            if not content:
                return JsonResponse({'status': 'ignored', 'message': 'Contenu vide'}, status=200)

            # Prevent loops if message came from our own bot
            if 'Barista Discord Bot' in str(username):
                return JsonResponse({'status': 'ignored', 'message': 'Bot message ignored'}, status=200)

            title = content[:80] + ("..." if len(content) > 80 else "")

            # Create post with sent_to_discord=True to prevent loopback
            post = CommunityPost.objects.create(
                title=title,
                content=content,
                category_slug='demarches',
                author_name=f"{username} (Discord)",
                author_role="Discord Community",
                author_avatar="🤖",
                sent_to_discord=True
            )

            return JsonResponse({
                'status': 'success',
                'post_id': post.id,
                'message': 'Message Discord publié automatiquement dans la Grande Salle !'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def api_sync_discord(request):
    """
    Synchronise les questions non encore transmises avec le serveur Discord.
    """
    ensure_community_tables()
    posts = CommunityPost.objects.filter(sent_to_discord=False)
    count = 0
    for p in posts:
        if p.notify_discord_bot():
            count += 1
    return JsonResponse({'status': 'success', 'synced_count': count, 'message': f'{count} question(s) transmise(s) à Discord !'})

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
