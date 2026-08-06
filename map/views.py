from django.shortcuts import render
from django.http import JsonResponse
from .models import AdministrativePOI

def map_view(request):
    """
    Renders the map interface.
    """
    return render(request, 'map/index.html')

def api_pois(request):
    """
    Returns a list of POIs in JSON format based on the official 14 government resources.
    Re-seeds if total count is under 25 to ensure nationwide coverage across French cities.
    """
    if AdministrativePOI.objects.count() < 26:
        AdministrativePOI.objects.all().delete()
        
        AdministrativePOI.objects.bulk_create([
            # ==================== PARIS & ÎLE-DE-FRANCE ====================
            AdministrativePOI(
                name="Préfecture de Police de Paris - Titres de Séjour",
                poi_type="Préfecture",
                address="92 Boulevard Ney",
                city="Paris",
                postal_code="75018",
                latitude=48.8988,
                longitude=2.3512,
                services_offered="Dépôt titres de séjour, renouvellements ANEF, remise de cartes, passeport talent",
                wait_time_minutes=120
            ),
            AdministrativePOI(
                name="Centre OFII de Paris (Direction Régionale)",
                poi_type="OFII",
                address="48 Rue de la Roquette",
                city="Paris",
                postal_code="75011",
                latitude=48.8548,
                longitude=2.3734,
                services_offered="Validation VLS-TS, Signature CIR, Visite médicale, Formations civiques",
                wait_time_minutes=45
            ),
            AdministrativePOI(
                name="Campus France Siège National & Accueil International",
                poi_type="Campus France",
                address="28 Rue de la Grange aux Belles",
                city="Paris",
                postal_code="75010",
                latitude=48.8742,
                longitude=2.3670,
                services_offered="Information étudiants internationaux, orientation Études en France, bourses",
                wait_time_minutes=20
            ),
            AdministrativePOI(
                name="OFPRA - Siège National (Asile & Réfugiés)",
                poi_type="OFPRA",
                address="201 Rue Carnot",
                city="Fontenay-sous-Bois",
                postal_code="94136",
                latitude=48.8524,
                longitude=2.4770,
                services_offered="Instruction demandes d'asile, entretien, statut de réfugié et protection subsidiaire",
                wait_time_minutes=90
            ),
            AdministrativePOI(
                name="CAF de Paris (Centre 15e / APL & Logement)",
                poi_type="CAF",
                address="50 Rue du Dr Finlay",
                city="Paris",
                postal_code="75015",
                latitude=48.8502,
                longitude=2.2921,
                services_offered="Aides au logement (APL), RSA, primes d'activité, accompagnement Visale",
                wait_time_minutes=40
            ),
            AdministrativePOI(
                name="CPAM de Paris - Assurance Maladie Internationales",
                poi_type="Assurance Maladie",
                address="17 Place de l'Argonne",
                city="Paris",
                postal_code="75019",
                latitude=48.8891,
                longitude=2.3833,
                services_offered="Affiliation étudiants Ameli, ouverture droits Sécurité Sociale, Carte Vitale",
                wait_time_minutes=30
            ),
            AdministrativePOI(
                name="CROUS de Paris - Guichet Logement & Bourses",
                poi_type="CROUS",
                address="39 Avenue Georges Bernanos",
                city="Paris",
                postal_code="75005",
                latitude=48.8392,
                longitude=2.3399,
                services_offered="Résidences universitaires, aide sociale, restauration et caution Visale",
                wait_time_minutes=15
            ),

            # ==================== LILLE & HAUTS-DE-FRANCE ====================
            AdministrativePOI(
                name="Préfecture du Nord (Lille) - Service des Étrangers",
                poi_type="Préfecture",
                address="12 Rue Jean Sans Peur",
                city="Lille",
                postal_code="59000",
                latitude=50.6318,
                longitude=3.0611,
                services_offered="Titres de séjour ANEF, vie privée et familiale, regroupement familial, asile",
                wait_time_minutes=95
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Lille",
                poi_type="OFII",
                address="2 Rue de Tenremonde",
                city="Lille",
                postal_code="59000",
                latitude=50.6360,
                longitude=3.0520,
                services_offered="Contrat d'Intégration Républicaine (CIR), test linguistique, visite médicale",
                wait_time_minutes=35
            ),
            AdministrativePOI(
                name="Campus France Lille - Guichet International",
                poi_type="Campus France",
                address="2 Boulevard Louis XIV",
                city="Lille",
                postal_code="59000",
                latitude=50.6280,
                longitude=3.0710,
                services_offered="Accueil étudiants étrangers, validation diplômes, orientation",
                wait_time_minutes=15
            ),
            AdministrativePOI(
                name="CAF du Nord (Lille)",
                poi_type="CAF",
                address="82 Rue Brûle Maison",
                city="Lille",
                postal_code="59000",
                latitude=50.6268,
                longitude=3.0561,
                services_offered="Dossiers APL, garantie Visale, allocations familiales",
                wait_time_minutes=30
            ),

            # ==================== LYON & AUVERGNE-RHÔNE-ALPES ====================
            AdministrativePOI(
                name="Préfecture du Rhône (Lyon) - Direction des Migrations",
                poi_type="Préfecture",
                address="97 Rue Molière",
                city="Lyon",
                postal_code="69003",
                latitude=45.7610,
                longitude=4.8465,
                services_offered="Renouvellements ANEF, passeport talent, vie privée et familiale, récépissés",
                wait_time_minutes=110
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Lyon",
                poi_type="OFII",
                address="7 Rue Quivogne",
                city="Lyon",
                postal_code="69002",
                latitude=45.7485,
                longitude=4.8285,
                services_offered="Contrat d'Intégration Républicaine (CIR), bilans de compétence et langue",
                wait_time_minutes=40
            ),
            AdministrativePOI(
                name="Espace Ulys / Campus France Lyon",
                poi_type="Campus France",
                address="16 Rue Jean-Marie Leclair",
                city="Lyon",
                postal_code="69009",
                latitude=45.7760,
                longitude=4.8050,
                services_offered="Accueil chercheurs et étudiants internationaux, aides installation",
                wait_time_minutes=20
            ),
            AdministrativePOI(
                name="GUDA Lyon (Guichet Unique Asile OFPRA)",
                poi_type="OFPRA",
                address="3 Rue du Docteur Bouchut",
                city="Lyon",
                postal_code="69003",
                latitude=45.7605,
                longitude=4.8580,
                services_offered="Enregistrement demande d'asile, orientation SPADA et OFPRA",
                wait_time_minutes=75
            ),

            # ==================== MARSEILLE & PACA ====================
            AdministrativePOI(
                name="Préfecture des Bouches-du-Rhône (Marseille)",
                poi_type="Préfecture",
                address="Place Félix Baret",
                city="Marseille",
                postal_code="13006",
                latitude=43.2923,
                longitude=5.3787,
                services_offered="Sejour étrangers, télé-procédures ANEF, titres de séjour salariés et étudiants",
                wait_time_minutes=130
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Marseille",
                poi_type="OFII",
                address="61 Boulevard Rabatau",
                city="Marseille",
                postal_code="13008",
                latitude=43.2790,
                longitude=5.3920,
                services_offered="Signature du CIR, formations civiques, bilans de santé OFII",
                wait_time_minutes=50
            ),
            AdministrativePOI(
                name="Campus France Marseille - Espace International",
                poi_type="Campus France",
                address="58 Boulevard Charles Livon",
                city="Marseille",
                postal_code="13007",
                latitude=43.2910,
                longitude=5.3580,
                services_offered="Accueil étudiants Aix-Marseille Université, démarches de rentrée",
                wait_time_minutes=15
            ),

            # ==================== TOULOUSE & OCCITANIE ====================
            AdministrativePOI(
                name="Préfecture de la Haute-Garonne (Toulouse)",
                poi_type="Préfecture",
                address="1 Place Saint-Étienne",
                city="Toulouse",
                postal_code="31000",
                latitude=43.6001,
                longitude=1.4492,
                services_offered="Service des étrangers, cartes de séjour, renouvellement ANEF, titres étudiants",
                wait_time_minutes=85
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Toulouse",
                poi_type="OFII",
                address="7 Rue Arthur Rimbaud",
                city="Toulouse",
                postal_code="31200",
                latitude=43.6210,
                longitude=1.4420,
                services_offered="Accompagnement républicain CIR, formations linguistiques, visite médicale",
                wait_time_minutes=30
            ),
            AdministrativePOI(
                name="Espace Accueil Étudiants Toulouse / Campus France",
                poi_type="Campus France",
                address="41 Allées Jules Guesde",
                city="Toulouse",
                postal_code="31000",
                latitude=43.5950,
                longitude=1.4475,
                services_offered="Guichet unique étudiants internationaux, aides au logement, bourses",
                wait_time_minutes=15
            ),

            # ==================== BORDEAUX & NOUVELLE-AQUITAINE ====================
            AdministrativePOI(
                name="Préfecture de la Gironde (Bordeaux)",
                poi_type="Préfecture",
                address="2 Esplanade Charles de Gaulle",
                city="Bordeaux",
                postal_code="33000",
                latitude=44.8362,
                longitude=-0.5825,
                services_offered="Démarches séjour, cartes vie privée et familiale, passeport talent",
                wait_time_minutes=90
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Bordeaux",
                poi_type="OFII",
                address="55 Rue du Jardin Public",
                city="Bordeaux",
                postal_code="33000",
                latitude=44.8480,
                longitude=-0.5750,
                services_offered="Contrat d'Intégration Républicaine, bilans civiques et médicaux",
                wait_time_minutes=35
            ),

            # ==================== STRASBOURG & GRAND EST ====================
            AdministrativePOI(
                name="Préfecture du Bas-Rhin (Strasbourg)",
                poi_type="Préfecture",
                address="5 Place de la République",
                city="Strasbourg",
                postal_code="67000",
                latitude=48.5870,
                longitude=7.7530,
                services_offered="Guichet étudiants, titres de séjour, statut réfugié OFPRA",
                wait_time_minutes=75
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Strasbourg",
                poi_type="OFII",
                address="4 Rue Jean-Mentelin",
                city="Strasbourg",
                postal_code="67200",
                latitude=48.5780,
                longitude=7.7080,
                services_offered="Signature CIR, examen civique, accompagnement à l'intégration",
                wait_time_minutes=25
            ),

            # ==================== NANTES & PAYS DE LA LOIRE ====================
            AdministrativePOI(
                name="Préfecture de Loire-Atlantique (Nantes)",
                poi_type="Préfecture",
                address="6 Quai Ceineray",
                city="Nantes",
                postal_code="44000",
                latitude=47.2225,
                longitude=-1.5540,
                services_offered="Demandes ANEF, cartes de séjour, regroupement familial",
                wait_time_minutes=80
            ),
            AdministrativePOI(
                name="Direction Régionale OFII de Nantes",
                poi_type="OFII",
                address="9 Rue René Viviani",
                city="Nantes",
                postal_code="44200",
                latitude=47.2060,
                longitude=-1.5410,
                services_offered="Formations civiques CIR, bilans médicaux, accueil des réfugiés",
                wait_time_minutes=30
            ),
        ])
    
    pois = AdministrativePOI.objects.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'poi_type': p.poi_type,
        'address': p.address,
        'city': p.city,
        'postal_code': p.postal_code,
        'latitude': float(p.latitude),
        'longitude': float(p.longitude),
        'services_offered': p.services_offered,
        'wait_time_minutes': p.wait_time_minutes
    } for p in pois]
    
    return JsonResponse({'status': 'success', 'pois': data})
