from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import urllib.request
import ssl

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
        Bridge Bot Discord : Envoie une notification instantanée au serveur Discord via Webhook.
        """
        webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
        if not webhook_url or 'dummy' in webhook_url:
            print(f"[Discord Bot Warning] Webhook URL absente ou dummy : '{self.title}'")
            return False

        category_name = str(self.category_slug).upper()
        text_message = (
            f"☕ **[GRANDE SALLE - {category_name}]**\n"
            f"👤 **Auteur:** {self.author_name} ({self.author_role})\n"
            f"📌 **Titre:** {self.title}\n"
            f"💬 **Question:**\n> {self.content}\n\n"
            f"👉 *Rejoindre et répondre : https://cafedesnations.fr/community/*"
        )

        payload = json.dumps({
            "username": "Le Barista",
            "content": text_message
        }).encode('utf-8')

        try:
            context = ssl._create_unverified_context()
            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, context=context, timeout=8) as response:
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
    sent_to_discord = models.BooleanField(default=False)

    def __str__(self):
        return f"Réponse à {self.post.title} par {self.author_name}"

    def notify_discord_bot(self):
        """
        Transmet les réponses au webhook Discord.
        """
        webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
        if not webhook_url or 'dummy' in webhook_url:
            return False

        header_prefix = "👨‍🍳 **[RÉPONSE DU BARISTA IA ☕]**" if self.is_official_answer else "💬 **[NOUVELLE RÉPONSE EN GRANDE SALLE]**"
        
        text_message = (
            f"{header_prefix}\n"
            f"📌 **Question:** *{self.post.title}*\n"
            f"👤 **Auteur réponse:** {self.author_name} ({self.author_role})\n"
            f"💬 **Réponse:**\n> {self.content}\n\n"
            f"👉 *Voir la suite : https://cafedesnations.fr/community/*"
        )
        
        payload = json.dumps({
            "username": "Le Barista Bot",
            "content": text_message
        }).encode('utf-8')
        
        try:
            context = ssl._create_unverified_context()
            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, context=context, timeout=8) as response:
                print(f"[Discord Reply Bot Success] Status: {response.status}")
                if response.status in [200, 204]:
                    self.sent_to_discord = True
                    CommunityReply.objects.filter(id=self.id).update(sent_to_discord=True)
                    return True
        except Exception as e:
            print("[Discord Reply Bot Error]:", e)
        return False

@receiver(post_save, sender=CommunityPost)
def auto_notify_discord_on_create(sender, instance, created, **kwargs):
    """
    Signal automatique :
    1. Envoie la question sur Discord.
    2. Génère une réponse IA automatique via Mistral.
    3. Publie la réponse IA sur le site et l'envoie sur Discord.
    """
    if created:
        if not instance.sent_to_discord:
            instance.notify_discord_bot()
        
        # Generer automatiquement une réponse IA Mistral pour la question
        try:
            from ai.services import ChatbotService
            service = ChatbotService()
            ai_text = service.generate_community_answer(instance.title, instance.content)
            
            # Sauvegarder la réponse IA (qui déclenchera son propre signal Discord)
            CommunityReply.objects.create(
                post=instance,
                author_name="Le Barista IA",
                author_role="Assistant IA Officiel",
                author_avatar="👨‍🍳",
                content=ai_text,
                is_official_answer=True
            )
        except Exception as e:
            print("Error auto-generating Mistral AI reply:", e)

@receiver(post_save, sender=CommunityReply)
def auto_notify_discord_on_reply(sender, instance, created, **kwargs):
    """
    Signal automatique : Transmet les nouvelles réponses (utilisateurs ou IA) vers Discord.
    """
    if created and not instance.sent_to_discord:
        instance.notify_discord_bot()
