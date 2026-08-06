from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Profil Étendu', {'fields': ('nationality', 'status', 'visa_type', 'family_situation')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
