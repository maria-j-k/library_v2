from flaskr import create_app, db
from flaskr.models import Person

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Person': Person}
