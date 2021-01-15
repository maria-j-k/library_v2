from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Person
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, PersonForm

@bp.route('/persons', methods=['GET', 'POST'])
def persons_list():
    session['ids'] = []
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
    if request.method == 'POST':
        id_list = request.form.getlist('person_id')
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return render_template('repair/persons_list.html', 
            persons=p.items, p=p, form=form, scope=scope)
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return render_template('repair/persons_list.html', 
            persons=p.items, p=p, form=form, scope=scope)
        session['ids'] = id_list
        return redirect(url_for('repair.persons_merge'))
    return render_template('repair/persons_list.html', 
            persons=p.items, p=p, form=form, scope=scope)

@bp.route('/persons/<int:id>', methods=['GET'])
def person_details(id):
    session['ids'] = []
    person = Person.query.get(id)
    return render_template('repair/person_details.html', person=person)

@bp.route('/persons/<int:id>/edit', methods=['GET', 'POST'])
def person_edit(id):
    session['ids'] = []
    person = Person.query.get(id)
    form = PersonForm(name=person.name, 
            approuved=person.approuved, 
            incorrect=person.incorrect)
    if form.validate_on_submit():
        person_name = form.name.data
        if person.name != person_name:
            p = Person.query.filter_by(name=person_name).first()
            if p: 
                flash(f'''Person {p.name} exists already in the database. \n
                    You have to merge "{person.name}" with "{p.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            person.name = person_name
            person.approuved = form.approuved.data
            person.incorrect = form.incorrect.data
            db.session.add(person)
            db.session.commit()
            return redirect(url_for('repair.person_details', id=person.id))
            
    return render_template('repair/person_edit.html', form=form, person=person)


@bp.route('/persons/merge_h/', methods=['GET'])
def persons_merge_helper():
    session['ids'] = []
    ids = request.args.getlist('ids')
    session['ids'] = ids
    return redirect(url_for('repair.persons_merge'))


@bp.route('/persons/merge/', methods=['GET', 'POST'])
def persons_merge():
    id_list = session.get('ids')
    persons = Person.query.filter(Person.id.in_(id_list)).order_by('name').all()
    print(f'persons: {persons}')
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.persons_list'))
            return redirect(url_for('repair.persons_merge'))
        main = Person.query.get(request.form.get('person'))
        print(main.id)
        for person in persons:
            print(f'zew loop {person is main}')
            if person is not main:
                for creator in person.creator.all():
                    for c in main.creator.all():
                        if (creator.book_id, creator.role) == (c.book_id,
                                c.role):
                            print(creator.__tablename__, creator.id)
                            db.session.delete(creator)
                            
                        else:
                            creator.person_id = main.id
                            db.session.add(creator)
                        db.session.commit()
                db.session.delete(person)
        db.session.commit()
        return redirect(url_for('repair.person_details', id=main.id))
        
    return render_template('repair/persons_to_merge.html', persons=persons)
