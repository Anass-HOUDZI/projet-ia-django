import json
import urllib.request

from django.conf import settings
from django.db import models


class CommunityCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='💬')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.icon} {self.name}"

class CommunityPost(models.Model):
    category = models.ForeignKey(CommunityCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    author_name = models.CharField(max_length=100, default='Anonyme')
    author_role = models.CharField(max_length=100, default='Habitué du Café')
    author_avatar = models.CharField(max_length=10, default='☕')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category_slug = models.CharField(max_length=50, default='demarches')
    likes_count = models.IntegerField(default=0)
    replies_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_discord = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def notify_discord_bot(self):
        """
        Bridge Bot Discord : Envoie une notification formatée (Embed) au serveur Discord (via urllib.request).
        """
        webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
        if not webhook_url or 'dummy' in webhook_url:
            print(f"[Discord Bot] Question enregistrée en BDD : '{self.title}' (Prêt pour webhook Discord)")
            return False

        embed = {
            "title": f"📢 NOUVELLE QUESTION EN GRANDE SALLE : {self.title}",
            "description": self.content[:350] + ("..." if len(self.content) > 350 else ""),
            "url": "https://cafedesnations.fr/community/",
            "color": 15230000, # Terracotta #E8622C
            "fields": [
                {
                    "name": "Catégorie",
                    "value": self.category_slug.upper(),
                    "inline": True
                },
                {
                    "name": "Auteur",
                    "value": f"{self.author_avatar} {self.author_name} ({self.author_role})",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Café des Nations • Bot Discord d'Entraide 🤖",
            }
        }

        payload = json.dumps({
            "username": "Le Barista Discord Bot ☕",
            "embeds": [embed]
        }).encode('utf-8')

        try:
            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status in [200, 204]:
                    self.sent_to_discord = True
                    self.save(update_fields=['sent_to_discord'])
                    return True
        except Exception as e:
            print("[Discord Bot Error]:", e)
        return False

class CommunityReply(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='replies')
    author_name = models.CharField(max_length=100, default='Barista IA')
    author_role = models.CharField(max_length=100, default='Mentor Certifié')
    author_avatar = models.CharField(max_length=10, default='👨‍🍳')
    content = models.TextField()
    is_official_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse à {self.post.title} par {self.author_name}"
