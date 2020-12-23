from csv import DictReader
from itertools import chain

from flask import flash, jsonify, redirect, render_template, request, session, url_for, g, current_app

from flaskr import db
from flaskr.models import Book, Copy, Creator, Person, Publisher, Serie
from flaskr.staff import bp
from flaskr.staff.forms import AddBookForm, TitleForm, PersonForm
from scripts.utils import get_or_create


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
        title = form.title.data 
        pub_name = form.published.publisher_name.data
        pub_place = form.published.city.data
        publisher, _ = get_or_create(db.session, Publisher, name=pub_name, city=pub_place)
        serie = form.published.serie.data or None
        if serie:
            serie, _ = get_or_create(db.session, Serie, name=serie, publisher=publisher)
        book = Book(title=title, pub_year=form.book.pub_year.data, publisher=publisher, serie=serie)
        db.session.add(book)
        creators = chain(form.authors.data, form.translators.data, form.redactors.data, form.intro.data)
        for creator in creators:
            role = creator['role']
            if creator['id_']:
                c = Creator(person_id=creator['id_'], book=book, role=role)
                db.session.add(c)
            elif creator['name'] != '':
                person = Person(name=creator['name'])
                db.session.add(person)
        book.isbn = form.book.isbn.data or None
        book.origin_language = form.book.origin_language.data or None
        book.first_edition = form.book.first_edition.data or None
        book.periodic_num = form.book.periodic_num.data or None
        book.genre = form.book.genre.data or None
        book.literary_form = form.book.literary_form.data or None
        book.fiction = form.book.fiction.data or None
        book.subject = form.book.subject.data or None
        book.precision = form.book.precision.data or None
        book.nukat = form.book.nukat.data or None
        copy = Copy(book=book, on_shelf=form.copy.on_shelf.data)
        db.session.add(copy)
        db.session.commit()
    else:
        print(form.errors)
    return render_template('staff/step_form_base.html', form=form)





















