from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import urllib.request
import ssl

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
        Bridge Bot Discord : Envoie une notification formatée (Embed) au serveur Discord via Webhook.
        """
        webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
        if not webhook_url or 'dummy' in webhook_url:
            print(f"[Discord Bot Warning] Webhook URL absente ou dummy : '{self.title}'")
            return False

        embed = {
            "title": f"📢 NOUVELLE QUESTION EN GRANDE SALLE : {self.title}",
            "description": self.content[:350] + ("..." if len(self.content) > 350 else ""),
            "url": "https://cafedesnations.fr/community/",
            "color": 15230000, # Terracotta #E8622C
            "fields": [
                {
                    "name": "Catégorie",
                    "value": str(self.category_slug).upper(),
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
            "content": f"☕ **Nouvelle question posée par {self.author_name} en Grande Salle !**",
            "username": "Le Barista Discord Bot ☕",
            "embeds": [embed]
        }).encode('utf-8')
        
        try:
            context = ssl._create_unverified_context()
            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, context=context, timeout=6) as response:
                print(f"[Discord Bot Success] Webhook response status: {response.status} pour '{self.title}'")
                if response.status in [200, 204]:
                    self.sent_to_discord = True
                    CommunityPost.objects.filter(id=self.id).update(sent_to_discord=True)
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

@receiver(post_save, sender=CommunityPost)
def auto_notify_discord_on_create(sender, instance, created, **kwargs):
    """
    Signal automatique : Déclenche la synchronisation Discord instantanée dès création d'une question.
    """
    if created and not instance.sent_to_discord:
        instance.notify_discord_bot()
