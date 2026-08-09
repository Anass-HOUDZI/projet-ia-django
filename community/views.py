import json

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import CommunityPost, CommunityReply

def seed_initial_community_posts():
    """
    S'assure que les 6 questions de référence pour toutes les thématiques existent en base.
    """
    posts_data = [
        {
            "title": "Récépissé ANEF pas reçu après 2 mois de demande de renouvellement : que faire ?",
            "content": "J'ai déposé mon dossier de renouvellement de VLS-TS étudiant sur l'ANEF il y a 2 mois à la préfecture de Lyon. Mon titre actuel expire dans 10 jours et je n'ai toujours pas reçu l'Attestation de Prolongation d'Instruction (API). Est-ce normal ?",
            "category_slug": "demarches",
            "author_name": "Youssef M.",
            "author_role": "Habitué du Café",
            "author_avatar": "🎓",
            "likes_count": 18,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Youssef ! Pas de panique. L'Attestation de Prolongation d'Instruction (API) est téléchargeable sur votre espace ANEF dès que la préfecture valide la complétude du dossier. À Lyon, le délai moyen d'instruction est de 6 à 8 semaines. Vous pouvez envoyer une relance polie via le formulaire de contact ANEF sans frais.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Sonia K.",
                    "author_role": "Guide Préfecture",
                    "author_avatar": "🇩🇿",
                    "content": "À Lyon ça prend souvent entre 6 et 8 semaines. Vérifie bien l'onglet 'Mes démarches' sur l'ANEF, l'attestation apparaît parfois directement sans notification !",
                    "is_official_answer": False
                }
            ]
        },
        {
            "title": "Garantie Visale refusée sans garant physique : quelles alternatives crédibles ?",
            "content": "Je viens d'arriver pour un Master à Paris. Mon dossier Visale est validé mais le propriétaire exige malgré tout un garant physique résidant en France. Quels recours avez-vous utilisés dans ce cas ?",
            "category_slug": "logement",
            "author_name": "Amina K.",
            "author_role": "Membre Récent",
            "author_avatar": "🏠",
            "likes_count": 14,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Amina ! Rappelez au bailleur que la Garantie Visale est accordée par Action Logement, 100% gratuite et garantit les loyers impayés jusqu'à 36 mois sans franchise. Si le bailleur persiste, vous pouvez proposer des organismes agréés complémentaires comme Garantme ou Unkle, ou utiliser la caution bancaire.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Amine T.",
                    "author_role": "Mentor Logement",
                    "author_avatar": "🔑",
                    "content": "Tu peux lui envoyer la notice explicative Action Logement destinée aux propriétaires, cela rassure 90% des bailleurs hésitants !",
                    "is_official_answer": False
                }
            ]
        },
        {
            "title": "Changement de statut Étudiant vers Salarié / Passeport Talent : délai moyen de l'autorisation de travail ?",
            "content": "J'ai signé une promesse d'embauche CDI en tant qu'ingénieur logiciel à Lille. Mon employeur a fait la demande d'autorisation de travail en ligne sur démarches-simplifiées. Combien de temps cela prend-il actuellement ?",
            "category_slug": "emploi",
            "author_name": "Mamadou S.",
            "author_role": "Habitué du Café",
            "author_avatar": "💼",
            "likes_count": 22,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Mamadou ! Félicitations pour votre CDI. Si votre rémunération brute annuelle est supérieure à 1,5 x le SMIC (environ 32 000€/an pour un diplôme de niveau Master), l'autorisation de travail est accordée de droit. Le délai moyen de délivrance de l'attestation préfectorale est de 3 à 4 semaines.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Lucie V.",
                    "author_role": "Guide Emploi",
                    "author_avatar": "🇫🇷",
                    "content": "Si ton salaire dépasse le seuil, la préfecture traite le dossier très vite. Garde bien ton récépissé de dépôt de changement de statut !",
                    "is_official_answer": False
                }
            ]
        },
        {
            "title": "Demande de bourse CROUS et repas à 1€ pour les étudiants internationaux : quelles conditions ?",
            "content": "Est-ce que les étudiants internationaux hors-UE peuvent bénéficier du repas CROUS à 1€ et demander un logement en résidence universitaire si une place se libère en cours d'année ?",
            "category_slug": "etudiant",
            "author_name": "Olena K.",
            "author_role": "Membre Récent",
            "author_avatar": "🎓",
            "likes_count": 16,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Olena ! Oui ! Les étudiants non-boursiers en situation de précarité peuvent demander la tarification sociale à 1€ pour les repas CROUS en déposant un dossier sur la plateforme messervices.etudiant.gouv.fr. Pour les logements CROUS, les places désistées sont remises en ligne chaque semaine sur trouverunlogement.crous.fr.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Karim M.",
                    "author_role": "Ambassadeur Étudiant",
                    "author_avatar": "🇲🇦",
                    "content": "Fais ta demande d’évaluation sociale sur le site du CROUS de ton académie, l'accès au repas à 1€ est accordé très rapidement !",
                    "is_official_answer": False
                }
            ]
        },
        {
            "title": "Réductions transports Navigo / TER et Carte Avantage Jeune pour les démarches administratives",
            "content": "Quelles sont les meilleures astuces et cartes de réduction pour voyager entre les préfectures régionales et son université à petit budget ?",
            "category_slug": "bons_plans",
            "author_name": "Carlos R.",
            "author_role": "Habitué du Café",
            "author_avatar": "💡",
            "likes_count": 19,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Carlos ! En Île-de-France, le forfait Imagine R Étudiant offre 50% de réduction sur les transports Navigo. Pour les déplacements régionaux en France, la Carte Avantage Jeune SNCF (49€/an) garantit -30% sur tous les TGV InOui et TER avec des prix plafonnés à 39€, 59€ et 79€.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Inès B.",
                    "author_role": "Mentor Bons Plans",
                    "author_avatar": "🇲🇦",
                    "content": "Achète la Carte Avantage lors des ventes flash SNCF (souvent à 25€), elle est amortie dès ton premier trajet !",
                    "is_official_answer": False
                }
            ]
        },
        {
            "title": "Validation du VLS-TS et taxe de séjour auprès de l'OFII : quelle est la procédure obligatoire ?",
            "content": "Je suis arrivée en France avec un Visa Long Séjour valant Titre de Séjour (VLS-TS). Comment valider le visa et régler la taxe de séjour dans les 3 mois réglementaires ?",
            "category_slug": "demarches",
            "author_name": "Lina T.",
            "author_role": "Membre Récent",
            "author_avatar": "📄",
            "likes_count": 25,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Lina ! Bienvenue en France. La validation du VLS-TS s'effectue obligatoirement en ligne dans les 3 mois suivant votre arrivée sur le portail ANEF (rubrique 'Valider mon VLS-TS'). Vous y achèterez votre timbre fiscal dématérialisé (75€ pour les étudiants). À l'issue, l'OFII vous convoquera pour la visite médicale et la signature du Contrat d'Intégration Républicaine (CIR).",
                    "is_official_answer": True
                },
                {
                    "author_name": "David M.",
                    "author_role": "Guide Intégration",
                    "author_avatar": "🇨🇩",
                    "content": "Fais-le dès la première semaine ! Tu auras ton attestation de confirmation de validation tout de suite, nécessaire pour valider ton inscription administrative à la fac.",
                    "is_official_answer": False
                }
            ]
        }
    ]

    for pdata in posts_data:
        post, created = CommunityPost.objects.get_or_create(
            title=pdata["title"],
            defaults={
                "content": pdata["content"],
                "category_slug": pdata["category_slug"],
                "author_name": pdata["author_name"],
                "author_role": pdata["author_role"],
                "author_avatar": pdata["author_avatar"],
                "likes_count": pdata["likes_count"],
                "sent_to_discord": True
            }
        )
        if created:
            for rdata in pdata["replies"]:
                CommunityReply.objects.create(
                    post=post,
                    author_name=rdata["author_name"],
                    author_role=rdata["author_role"],
                    author_avatar=rdata["author_avatar"],
                    content=rdata["content"],
                    is_official_answer=rdata["is_official_answer"],
                    sent_to_discord=True
                )

def ensure_community_tables():
    """
    S'assure que les tables SQLite existent et contiennent tous les sujets de référence.
    """
    try:
        seed_initial_community_posts()
    except Exception as e:
        print("Initial seed attempt error:", e)
        try:
            call_command('migrate', 'community', interactive=False)
            seed_initial_community_posts()
        except Exception as migrate_err:
            print("Auto migration community error:", migrate_err)

def index_view(request):
    """
    Renders the community landing page with database posts & Discord bot integration.
    """
    ensure_community_tables()
    posts = CommunityPost.objects.all().prefetch_related('replies')
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

            if 'Barista Discord Bot' in str(username):
                return JsonResponse({'status': 'ignored', 'message': 'Bot message ignored'}, status=200)

            title = content[:80] + ("..." if len(content) > 80 else "")

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
