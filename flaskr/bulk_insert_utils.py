from csv import DictReader

from flaskr import db
from flaskr.models import Person


def add_bulk():
    filepath = '/home/maria/persons.csv'
    form = TitleForm()
    with open(filepath) as f:
        csv_file = DictReader(f)
        for row in csv_file:
            person = Person(name=row['name'])
            db.session.add(person)
        db.session.commit()
    return render_template('search_title.html', form=form)
