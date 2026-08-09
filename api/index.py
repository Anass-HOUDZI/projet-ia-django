import os
import sys

# Ensure root directory is on Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django_intro.wsgi import app  # noqa: F401
