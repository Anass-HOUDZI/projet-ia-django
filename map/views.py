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
    Returns a list of POIs in JSON format.
    Seeds the database with dummy data if empty (for prototype).
    """
    # Verify if we need to seed or re-seed (if old models without city exist)
    if AdministrativePOI.objects.count() < 10:
        # Clear old dummy data if they don't have city fields (to cleanly re-seed)
        AdministrativePOI.objects.all().delete()
        
        AdministrativePOI.objects.bulk_create([
            # PARIS
            AdministrativePOI(name="Préfecture de Police", poi_type="Préfecture", address="92 Boulevard Ney", city="Paris", postal_code="75018", latitude=48.8988, longitude=2.3512, services_offered="Titre de séjour, Renouvellement", wait_time_minutes=120),
            AdministrativePOI(name="CAF de Paris (15e)", poi_type="CAF", address="50 Rue du Dr Finlay", city="Paris", postal_code="75015", latitude=48.8502, longitude=2.2921, services_offered="APL, RSA, Prime d'activité", wait_time_minutes=45),
            AdministrativePOI(name="CPAM de Paris", poi_type="Assurance Maladie", address="17 Place de l'Argonne", city="Paris", postal_code="75019", latitude=48.8891, longitude=2.3833, services_offered="Carte Vitale, CSS", wait_time_minutes=30),
            AdministrativePOI(name="CROUS de Paris", poi_type="CROUS", address="39 Avenue Georges Bernanos", city="Paris", postal_code="75005", latitude=48.8392, longitude=2.3399, services_offered="Logement étudiant, Bourses", wait_time_minutes=15),
            AdministrativePOI(name="Pôle Emploi Paris", poi_type="Emploi", address="26 Rue de Crimée", city="Paris", postal_code="75019", latitude=48.8800, longitude=2.3900, services_offered="Recherche d'emploi, Inscription", wait_time_minutes=60),
            
            # LILLE
            AdministrativePOI(name="Préfecture du Nord", poi_type="Préfecture", address="12 Rue Jean Sans Peur", city="Lille", postal_code="59000", latitude=50.6318, longitude=3.0611, services_offered="Titre de séjour, Asile", wait_time_minutes=90),
            AdministrativePOI(name="CAF du Nord", poi_type="CAF", address="82 Rue Brûle Maison", city="Lille", postal_code="59000", latitude=50.6268, longitude=3.0561, services_offered="APL, RSA", wait_time_minutes=35),
            AdministrativePOI(name="CPAM de Lille", poi_type="Assurance Maladie", address="2 Rue d'Iéna", city="Lille", postal_code="59000", latitude=50.6219, longitude=3.0558, services_offered="Droits, Carte Vitale", wait_time_minutes=25),
            AdministrativePOI(name="CROUS de Lille", poi_type="CROUS", address="74 Rue de Cambrai", city="Lille", postal_code="59000", latitude=50.6225, longitude=3.0725, services_offered="Bourses, Restauration", wait_time_minutes=10),
            
            # LYON
            AdministrativePOI(name="Préfecture du Rhône", poi_type="Préfecture", address="97 Rue Molière", city="Lyon", postal_code="69003", latitude=45.7610, longitude=4.8465, services_offered="Étrangers, Naturalisation", wait_time_minutes=110),
            AdministrativePOI(name="CAF du Rhône", poi_type="CAF", address="67 Boulevard Marius Vivier Merle", city="Lyon", postal_code="69003", latitude=45.7595, longitude=4.8569, services_offered="Aides financières", wait_time_minutes=40),
            AdministrativePOI(name="CPAM de Lyon", poi_type="Assurance Maladie", address="276 Cours Lafayette", city="Lyon", postal_code="69003", latitude=45.7630, longitude=4.8655, services_offered="CSS, Arrêts", wait_time_minutes=20),
            
            # MARSEILLE
            AdministrativePOI(name="Préfecture des Bouches-du-Rhône", poi_type="Préfecture", address="Place Félix Baret", city="Marseille", postal_code="13006", latitude=43.2923, longitude=5.3787, services_offered="Visas, Renouvellement", wait_time_minutes=130),
            AdministrativePOI(name="CAF des Bouches-du-Rhône", poi_type="CAF", address="215 Chemin de Gibbes", city="Marseille", postal_code="13014", latitude=43.3256, longitude=5.3901, services_offered="Prestations familiales", wait_time_minutes=50),
        ])
    
    pois = AdministrativePOI.objects.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'poi_type': p.poi_type,
        'address': p.address,
        'city': p.city,
        'postal_code': p.postal_code,
        'latitude': str(p.latitude),
        'longitude': str(p.longitude),
        'services_offered': p.services_offered,
        'wait_time_minutes': p.wait_time_minutes
    } for p in pois]
    
    return JsonResponse({'status': 'success', 'pois': data})
