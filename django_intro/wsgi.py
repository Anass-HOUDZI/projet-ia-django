"""
WSGI config for django_intro project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_intro.settings')

application = get_wsgi_application()

# Auto-migrate SQLite on Vercel serverless startup if tables don't exist
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("Vercel auto-migration status:", e)

# Alias for Vercel Serverless Function Handler
app = application
