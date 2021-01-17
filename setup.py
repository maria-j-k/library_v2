import os 
from dotenv import load_dotenv

from flaskr import create_app, db
from flaskr.models import Book, City, Collection, Copy, Creator, Person, Publisher, Room,  Serie, Shelf
from flaskr.user_models import User


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db, 
            'Book': Book, 
            'City': City,
            'Collection': Collection, 
            'Copy': Copy, 
            'Creator': Creator, 
            'Person': Person, 
            'Publisher': Publisher, 
            'Room': Room,
            'Serie': Serie,
            'Shelf': Shelf,
            'User': User,
            }

#def deploy():
#   upgrade()
#   insert_roles()
#   create_indices()
#   dla każego modelu reindex()
#
