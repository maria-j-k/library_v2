from flaskr import create_app, db
from flaskr.models import Collection, Location, Person, Publisher, Serie

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Collection': Collection, 'Location': Location, 'Person': Person, 'Publisher': Publisher, 'Serie': Serie}
