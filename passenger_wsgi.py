import sys, os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), '/var/www/django_admin'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'chips.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()