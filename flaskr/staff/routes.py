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


@bp.route('/staff/add_book_try', methods=['GET', 'POST'])
def check_forms():
    title = 'W poszukiwaniu straconego czasu' # tytuł z pierwszego kroku
    form = CreatorsForm(title=title) 
    if form.validate_on_submit():
        authors = form.authors.data
        translators = form.translators.data
        print(authors)
        print(translators)
    return render_template('staff/step_form_base.html', form=form)


@bp.route('/autocomplete_person') # do API
def autocomplete_person():
    q = request.args.get('q')
    persons = Person.search(q)
    return jsonify(matching_persons=persons)


@bp.route('/autocomplete_publisher') # do API
def autoomplete_publisher():
    q = request.args.get('q')
    publishers = Publisher.search(q)
    return jsonify(matching_publishers=publishers)





















@bp.route('/try') # nie działa
def try_autocomplete():
    q = request.args.get('q')
    q_val = request.args.get('q-value')
#    if q_val - pobieram obiekt
#    else: przekazuję do następnego vidoku q
    return render_template('staff/load-data-via-ajax.html')
@bp.route('/staff/add_book_sec', methods=['GET', 'POST'])
def add_book():
    form = CreatorsForm()
    if request.method == 'POST':
        form = CreatorsForm(request.form)
    if form.validate_on_submit():
        print(form.__dict__)
#        a1 = form.a1_val.data
#        a2 = form.a2.data
#        a3 = form.a3.data
#        print(a1, a2, a3)
    return render_template('staff/add_book_steps.html', form =form)
