from django.db import models

class AdministrativePOI(models.Model):
    name = models.CharField(max_length=255)
    poi_type = models.CharField(max_length=100) # e.g., CAF, CPAM, Préfecture
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    services_offered = models.TextField(blank=True, help_text="Démarches prises en charge")
    wait_time_minutes = models.IntegerField(default=0, help_text="Temps d'attente estimé")

    def __str__(self):
        return f"{self.name} ({self.poi_type})"
