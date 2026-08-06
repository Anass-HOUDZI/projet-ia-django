from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Nationality and Status
    nationality = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nationalité")
    status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Statut (ex: étudiant, VPF, etc.)")
    visa_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type de visa / Titre de séjour")
    family_situation = models.CharField(max_length=100, blank=True, null=True, verbose_name="Situation familiale")

    def __str__(self):
        return self.username
