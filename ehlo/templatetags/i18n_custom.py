from django import template
from django.conf import settings
import json
import os

register = template.Library()

# Load translations once
BASE_DIR = settings.BASE_DIR
TRANS_PATH = os.path.join(BASE_DIR, 'ehlo', 'translations.json')

translations = {}
try:
    with open(TRANS_PATH, 'r', encoding='utf-8') as f:
        translations = json.load(f)
except Exception as e:
    print("Error loading translations:", e)

@register.simple_tag(takes_context=True)
def t(context, key):
    request = context.get('request')
    lang = getattr(request, 'lang', 'fr')
    
    # Try to find the translation, default to French, then fallback to key
    if key in translations:
        return translations[key].get(lang, translations[key].get('fr', key))
    return key
