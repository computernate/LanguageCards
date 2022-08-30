#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/LanguageCards')

from main import app as application