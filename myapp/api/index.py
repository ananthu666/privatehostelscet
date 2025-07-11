import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

# Import Django and configure
import django
django.setup()

from myapp.wsgi import application

# Vercel expects the WSGI application to be named 'app'
app = application
