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
    if not AdministrativePOI.objects.exists():
        # Paris coordinates roughly
        AdministrativePOI.objects.bulk_create([
            AdministrativePOI(name="Préfecture de Police", poi_type="Préfecture", latitude=48.8543, longitude=2.3488, services_offered="Titre de séjour, Renouvellement", wait_time_minutes=120),
            AdministrativePOI(name="CAF de Paris (15e)", poi_type="CAF", latitude=48.8412, longitude=2.2981, services_offered="APL, RSA, Prime d'activité", wait_time_minutes=45),
            AdministrativePOI(name="CPAM de Paris", poi_type="Assurance Maladie", latitude=48.8821, longitude=2.3683, services_offered="Carte Vitale, CSS", wait_time_minutes=30),
            AdministrativePOI(name="CROUS de Paris", poi_type="CROUS", latitude=48.8402, longitude=2.3399, services_offered="Logement étudiant, Bourses", wait_time_minutes=15),
            AdministrativePOI(name="Pôle Emploi Paris", poi_type="Emploi", latitude=48.8710, longitude=2.3600, services_offered="Recherche d'emploi, Inscription", wait_time_minutes=60),
        ])
    
    pois = AdministrativePOI.objects.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'poi_type': p.poi_type,
        'latitude': str(p.latitude),
        'longitude': str(p.longitude),
        'services_offered': p.services_offered,
        'wait_time_minutes': p.wait_time_minutes
    } for p in pois]
    
    return JsonResponse({'status': 'success', 'pois': data})
