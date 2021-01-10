from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Person
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, PersonForm

@bp.route('/persons', methods=['GET', 'POST'])
def persons_list():
    if request.method == 'POST':
        id_list = request.form.getlist('person_id')
        session['ids'] = id_list
        return redirect(url_for('repair.persons_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        persons = Person.fuzzy_search('name', name)
        p = Person.query.filter(Person.id.in_([item['id'] for item in persons])
                ).order_by('name').paginate(page, 20, False)
        
    elif scope == 'incorrect':
        p = Person.query.filter_by(incorrect=True).order_by(
                'name').paginate(page, 20, False)
    elif scope == 'all':
        p = Person.query.order_by('name').paginate(page, 20, False)
    return render_template('repair/persons_list.html', 
            persons=p.items, p=p,
            form=form, scope=scope)

@bp.route('/persons/<int:id>', methods=['GET'])
def person_details(id):
    person = Person.query.get(id)
    return render_template('repair/person_details.html', person=person)

@bp.route('/persons/<int:id>/edit', methods=['GET', 'POST'])
def person_edit(id):
    person = Person.query.get(id)
    form = PersonForm(name=person.name)
    if form.validate_on_submit():
        person_name = form.name.data
        p = Person.query.filter_by(name=person_name).first()
        if p:
            flash(f'''Person {p.name} exists already in the database. \n
                    You have to merge "{person.name}" with "{p.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            person.name = person_name
            db.session.add(person)
            db.session.commit()
            return redirect(url_for('repair.person_details', id=person.id))
            
    return render_template('repair/person_edit.html', form=form, person=person)

@bp.route('/persons/merge/', methods=['GET', 'POST'])
def persons_merge():
    id_list = session.get('ids')
    print(id_list)
    persons = Person.query.filter(Person.id.in_(id_list)).order_by('name').all()
    print(persons)
    if request.method == 'POST':
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            persons = Person.query.filter(Person.id.in_(id_list)
                    ).order_by('name').all()
            return redirect(url_for('repair.persons_merge',person=person))
        main = Person.query.get(request.form.get('person'))
        for person in persons:
            if person is not main:
                for creator in person.creator.all():
                    print(creator.id)
                    creator.person_id = main.id
                    db.session.add(creator)
                    db.session.commit()
                db.session.delete(person)
        db.session.commit()
        return redirect(url_for('repair.person_details', id=main.id))
        
    return render_template('repair/persons_to_merge.html', persons=persons)
