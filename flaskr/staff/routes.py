from csv import DictReader

from flask import flash, jsonify, redirect, render_template, request, session, url_for, g, current_app

from flaskr import db
from flaskr.staff import bp
from flaskr.staff.forms import AddBookForm, TitleForm, PersonForm
from flaskr.models import Book, Person


@bp.route('/staff/add_book_first', methods=['GET', 'POST'])
def search_title():
    form = TitleForm()
    ctx = {}
    if form.validate_on_submit():
        session['title'] = form.title.data
        return redirect(url_for('staff.choose_title'))
    else:
        print(form.errors)
    return render_template('staff/search_title.html', form=form, ctx=ctx)

@bp.route('/staff/choose_title', methods=['GET', 'POST'])
def choose_title():
    ctx = {}
    title = session['title']
    books = Book.query.filter(Book.title.ilike("%{}%".format(title))).all()
    ctx['books'] = books
    ctx['title'] = title
    if request.method == 'POST':
        print('post')
    return render_template('staff/choose_title.html', ctx=ctx)


@bp.route('/staff/add_book_second', methods=['GET', 'POST'])
def add_book():
    title = session['title']
    form = AddBookForm(title=title) 
    if form.validate_on_submit():
        authors = form.authors.data
        translators = form.translators.data
        print(authors)
        print(translators)
    return render_template('staff/step_form_base.html', form=form)





















