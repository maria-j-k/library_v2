from csv import DictReader

from flask import flash, jsonify, redirect, render_template, request, url_for, g, current_app

from flaskr import db
from flaskr.staff import bp
from flaskr.staff.forms import CreatorsForm, TitleForm, PersonForm
from flaskr.models import Person


@bp.route('/staff/add_book_first', methods=['GET', 'POST'])
def search_title():
    person_form = PersonForm()
    form = TitleForm()
    if form.validate_on_submit():
        title = form.title.data
        print(title)
    return render_template('staff/search_title.html', form=form, person_form=person_form)

@bp.route('/staff/add_book_sec', methods=['GET', 'POST'])
def add_book():
    form = CreatorsForm()
    form.person.min_entries=12
    if form.validate_on_submit():
        name = form.name.data
        print(name)
    return render_template('staff/add_book_steps.html', form =form)

@bp.route('/autocomplete_person')
def autocomplete_person():
    q = request.args.get('q')
    persons = Person.search(q)
    return jsonify(matching_persons=persons)

@bp.route('/try')
def try_autocomplete():
    return render_template('staff/load-data-via-ajax.html')
