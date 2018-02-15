import sys
sys.path.insert(0, '/var/www/flask_ac/projects/blog')
from app import create_app

application = create_app()
