from flaskr import create_app, db
from flaskr.models import Book, Collection, Copy, Creator, Location, Person, Publisher, Serie

app = create_app()
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Book': Book, 'Collection': Collection, 'Copy': Copy, 'Creator': Creator, 'Location': Location, 'Person': Person, 'Publisher': Publisher, 'Serie': Serie}
