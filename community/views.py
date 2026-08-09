import json

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from community.models import CommunityPost, CommunityReply

def seed_initial_community_posts():
    """
    Peuple la base de données avec 15 questions réelles et concrètes avec leurs réponses du Barista IA
    et des membres de la communauté sur l'ensemble des 5 thématiques.
    """
    posts_data = [
        # 1. Démarches - Récépissé ANEF
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
        # 2. Logement - Garantie Visale
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
        # 3. Emploi - Changement de statut
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
        # 4. Étudiant - Repas 1€ CROUS
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
        # 5. Bons plans - Transports
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
        # 6. Démarches - VLS-TS & OFII
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
        },
        # 7. Démarches - Changement d'adresse ANEF
        {
            "title": "Changement d'adresse sur l'ANEF après un déménagement : quel délai pour l'attestation ?",
            "content": "J'ai déménagé de Marseille vers Bordeaux pour mes études. J'ai déclaré mon changement d'adresse sur l'ANEF il y a 3 semaines. Dois-je attendre un nouveau titre ou l'attestation suffit-elle pour la CAF ?",
            "category_slug": "demarches",
            "author_name": "Nadia B.",
            "author_role": "Habitué du Café",
            "author_avatar": "📄",
            "likes_count": 13,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Nadia ! L'attestation de changement d'adresse téléchargeable immédiatement sur votre espace ANEF fait foi auprès de la CAF et des organismes publics. Il n'est pas nécessaire de refaire fabriquer une carte physique avant l'échéance de votre titre actuel.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Sami P.",
                    "author_role": "Guide ANEF",
                    "author_avatar": "🇹🇳",
                    "content": "Télécharge directement le PDF de confirmation de changement d'adresse sur l'ANEF et envoie-le à la CAF de Gironde via ton espace en ligne !",
                    "is_official_answer": False
                }
            ]
        },
        # 8. Logement - Demande d'APL CAF
        {
            "title": "Délai de versement de la première APL par la CAF pour un logement étudiant",
            "content": "J'ai soumis ma demande d'Aide Personnalisée au Logement (APL) le 5 septembre sur caf.fr. Pourquoi n'ai-je rien reçu en septembre et quand le premier versement arrive-t-il ?",
            "category_slug": "logement",
            "author_name": "Kevin R.",
            "author_role": "Membre Récent",
            "author_avatar": "🏠",
            "likes_count": 21,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Kevin ! Le premier mois d'entrée dans le logement (septembre) est un mois de carence légal durant lequel aucune APL n'est versée. Le droit s'ouvre au 1er octobre et le virement effectif intervient autour du 5 novembre sur votre compte bancaire.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Chloé D.",
                    "author_role": "Experte CAF",
                    "author_avatar": "🇫🇷",
                    "content": "C'est tout à fait normal ! La CAF paie à terme échu avec un mois de décalage. Vérifie bien que ton RIB et ton attestation de loyer (remplie par le bailleur) sont validés sur caf.fr.",
                    "is_official_answer": False
                }
            ]
        },
        # 9. Emploi - Quota 60% d'heures de travail
        {
            "title": "Limite des 964 heures de travail étudiant par an : comment est calculé le quota d'heures ?",
            "content": "Je travaille 15h par semaine en job étudiant dans une boulangerie. Est-ce que le quota de 964 heures/an (60% de la durée annuelle légale) s'applique par année civile ou sur la durée de mon visa ?",
            "category_slug": "emploi",
            "author_name": "Mehdi C.",
            "author_role": "Habitué du Café",
            "author_avatar": "💼",
            "likes_count": 17,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Mehdi ! Le quota de 964 heures s'apprécie sur la période de validité de votre titre de séjour (12 mois glissants). À 15h/semaine sur 40 semaines, vous réalisez 600 heures, ce qui est parfaitement dans les limites autorisées.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Alexandre T.",
                    "author_role": "Mentor Droit du Travail",
                    "author_avatar": "⚖️",
                    "content": "Attention si tu travailles à temps plein pendant l'été ! Garde un tableau Excel récapitulatif de tes fiches de paie pour prouver que tu ne dépasses pas 964h sur l'année.",
                    "is_official_answer": False
                }
            ]
        },
        # 10. Étudiant - CVEC & Inscription administrative
        {
            "title": "Paiement de la CVEC (103€) et exonération : qui peut être dispensé ?",
            "content": "Je dois finaliser mon inscription à la faculté de Strasbourg. La Contribution Vie Étudiante et de Campus (CVEC) est-elle obligatoire pour tous et qui peut en être exonéré ?",
            "category_slug": "etudiant",
            "author_name": "Chloé M.",
            "author_role": "Membre Récent",
            "author_avatar": "🎓",
            "likes_count": 15,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Chloé ! L'attestation CVEC est obligatoire pour toute inscription dans l'enseignement supérieur. Sont exonérés de plein droit : les boursiers du CROUS, les réfugiés, les bénéficiaires de la protection subsidiaire ou demandeurs d'asile.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Yassine N.",
                    "author_role": "Ambassadeur Campus",
                    "author_avatar": "🇩🇿",
                    "content": "Va sur cvec.etudiant.gouv.fr. Même si tu es exonérée, tu dois obligatoirement générer ton attestation d'exonération avec le QR Code pour l'université !",
                    "is_official_answer": False
                }
            ]
        },
        # 11. Bons plans - Équipement & Emmaüs
        {
            "title": "Meilleures plateformes pour meubler son studio étudiant à moins de 100€",
            "content": "Quels sont vos bons plans pour trouver du mobilier, un matelas et de la vaisselle à très bas prix en arrivant dans une nouvelle ville ?",
            "category_slug": "bons_plans",
            "author_name": "Sami L.",
            "author_role": "Habitué du Café",
            "author_avatar": "💡",
            "likes_count": 27,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Sami ! Pensez aux applications de don entre particuliers comme Geev ou Donnons.org, ainsi qu'aux ressourceries Emmaüs et aux bourses aux affaires organisées par les CROUS et les associations étudiantes.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Manon F.",
                    "author_role": "Reine des Bons Plans",
                    "author_avatar": "🎉",
                    "content": "Télécharge l'appli GEEV ! Les gens donnent gratuitement des tables, chaises et vaisselle en parfait état, il faut juste aller les chercher.",
                    "is_official_answer": False
                }
            ]
        },
        # 12. Démarches - Permis de conduire étranger
        {
            "title": "Échange de permis de conduire étranger sur la téléprocédure ANTS : quand faire la demande ?",
            "content": "J'ai un permis de conduire marocain valide. Puis-je conduire la première année avec mon VLS-TS et quand dois-je faire la demande d'échange en permis français ?",
            "category_slug": "demarches",
            "author_name": "Yassine A.",
            "author_role": "Membre Récent",
            "author_avatar": "📄",
            "likes_count": 19,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Yassine ! Pendant toute la durée de vos études sous statut étudiant, votre permis étranger accompagné d'une traduction assermentée est valable sans limite de durée. Si vous passez sous statut salarié, la demande d'échange doit être effectuée sur l'ANTS dans l'année suivant l'obtention de votre premier titre de séjour non-étudiant.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Tariq K.",
                    "author_role": "Guide Auto",
                    "author_avatar": "🇲🇦",
                    "content": "Garde bien ton permis original et ta traduction officielle toujours avec toi dans la voiture en cas de contrôle de police !",
                    "is_official_answer": False
                }
            ]
        },
        # 13. Logement - État des lieux & Caution
        {
            "title": "Délai légal de restitution du dépôt de garantie (caution) par le propriétaire",
            "content": "J'ai rendu les clés de mon ancien appartement le 30 juin sans aucune dégradation constatée lors de l'état des lieux. Le propriétaire a-t-il 1 ou 2 mois pour me rembourser la caution ?",
            "category_slug": "logement",
            "author_name": "Camille P.",
            "author_role": "Habitué du Café",
            "author_avatar": "🏠",
            "likes_count": 18,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Camille ! Lorsque l'état des lieux de sortie est conforme à l'état des lieux d'entrée, le propriétaire dispose d'un délai légal maximal de 1 mois pour vous restituer le dépôt de garantie. En cas de retard, une majoration de 10% du loyer hors charges s'applique par mois de retard commencé.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Benoît V.",
                    "author_role": "Conseiller Logement",
                    "author_avatar": "⚖️",
                    "content": "Si le délai de 1 mois est dépassé, envoie une lettre recommandée avec accusé de réception (LRAR) de mise en demeure de restituer le dépôt de garantie !",
                    "is_official_answer": False
                }
            ]
        },
        # 14. Emploi - Stage fin d'études & Gratification
        {
            "title": "Gratification minimale de stage (4.35€/h) et dépassement des 2 mois : comment est-ce calculé ?",
            "content": "Mon entreprise me propose un stage de 5 mois. La gratification minimale est-elle obligatoire et est-elle exonérée d'impôts sur le revenu ?",
            "category_slug": "emploi",
            "author_name": "Omar Z.",
            "author_role": "Membre Récent",
            "author_avatar": "💼",
            "likes_count": 20,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Omar ! Dès lors que la durée du stage dépasse 2 mois (308 heures de présence), la gratification minimale horaire (4,35€/h en 2024, soit environ 650€/mois pour 35h/semaine) est légalement obligatoire. Elle est totalement exonérée d'impôt sur le revenu dans la limite du montant annuel du SMIC.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Laura G.",
                    "author_role": "Guide RH",
                    "author_avatar": "💼",
                    "content": "Tu as aussi droit au remboursement de 50% du pass Navigo/transport et aux tickets restaurant si les salariés en bénéficient !",
                    "is_official_answer": False
                }
            ]
        },
        # 15. Étudiant - Sécurité sociale Ameli
        {
            "title": "Inscription des étudiants internationaux sur etudiant-etranger.ameli.fr",
            "content": "J'ai fait mon inscription sur Ameli étudiant étranger il y a 1 mois. Quel est le délai pour obtenir mon Numéro de Sécurité Sociale définitif et commander la carte Vitale ?",
            "category_slug": "etudiant",
            "author_name": "Fatou D.",
            "author_role": "Habitué du Café",
            "author_avatar": "🎓",
            "likes_count": 23,
            "replies": [
                {
                    "author_name": "Le Barista IA",
                    "author_role": "Assistant IA Officiel",
                    "author_avatar": "👨‍🍳",
                    "content": "Bonjour Fatou ! La CPAM attribue d'abord un numéro provisoire (commençant par 7 ou 8) pour ouvrir vos droits aux remboursements de soins. Le délai pour obtenir le numéro définitif (commençant par 1 ou 2) et commander la carte Vitale est d'environ 2 à 3 mois après validation de votre attestation de scolarité.",
                    "is_official_answer": True
                },
                {
                    "author_name": "Kenza B.",
                    "author_role": "Ambassadrice Santé",
                    "author_avatar": "🏥",
                    "content": "Pense à télécharger ton attestation de droits provisoire sur ton compte ameli pour te faire rembourser tes consultations chez le médecin en attendant la carte Vitale !",
                    "is_official_answer": False
                }
            ]
        }
    ]

    for pdata in posts_data:
        likes_val = pdata.get("likes_count", 0)
        likes_num = likes_val if isinstance(likes_val, int) else 0
        post, created = CommunityPost.objects.get_or_create(
            title=str(pdata["title"]),
            defaults={
                "content": str(pdata["content"]),
                "category_slug": str(pdata["category_slug"]),
                "author_name": str(pdata["author_name"]),
                "author_role": str(pdata["author_role"]),
                "author_avatar": str(pdata["author_avatar"]),
                "likes_count": likes_num,
                "sent_to_discord": True
            }
        )
        if created:
            replies = pdata.get("replies")
            if isinstance(replies, list):
                for rdata in replies:
                    if isinstance(rdata, dict):
                        CommunityReply.objects.create(
                            post=post,
                            author_name=str(rdata.get("author_name", "")),
                            author_role=str(rdata.get("author_role", "")),
                            author_avatar=str(rdata.get("author_avatar", "")),
                            content=str(rdata.get("content", "")),
                            is_official_answer=bool(rdata.get("is_official_answer", False)),
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
