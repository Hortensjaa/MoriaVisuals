import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoriaVisuals.settings')

application = get_wsgi_application()

sys.path = [p for p in sys.path if not p.endswith('eggs')]
