from itertools import chain

from flask import flash, jsonify, redirect, render_template, request, session, url_for, g, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Book, City, Copy, Creator, Person, Publisher, Serie
from flaskr.staff import bp
from flaskr.staff.forms import AddBookForm, BookForm, CopyForm, TitleForm, PersonForm
from scripts.utils import get_or_create


@bp.route('/staff/add_book_first', methods=['GET', 'POST'])
@login_required
def search_title():
    form = TitleForm()
    ctx = {}
    if form.validate_on_submit():
        session['title'] = form.title.data
        return redirect(url_for('staff.choose_title'))
    else:
        print(form.errors)
    return render_template('staff/search_title.html', form=form, ctx=ctx)

@bp.route('/staff/try', methods=['GET', 'POST'])
def try_form():
    form = AddBookForm()
    return render_template('staff/add_book.html', form=form)

@bp.route('/staff/choose_title', methods=['GET', 'POST'])
@login_required
def choose_title():
    ctx = {}
    title = session.get('title')
    if not title:
        return redirect(url_for('staff.search_title'))
    books = Book.query.filter(Book.title.ilike("%{}%".format(title))).all()
    ctx['books'] = books
    ctx['title'] = title
    if request.method == 'POST':
        print('post')
    return render_template('staff/choose_title.html', ctx=ctx)


@bp.route('/staff/add_book_second', methods=['GET', 'POST'])
@login_required
def add_book():
    title = session.get('title')
    if not title:
        return redirect(url_for('staff.search_title'))
    form = BookForm(title=title) 
    if form.validate_on_submit():
        title = form.title.data 
        pub_name = form.publisher_name.data
        pub_place = form.city.data
        publisher = form.publisher_name.data or None
        serie = form.serie.data or None
        
        city, _ = get_or_create(db.session, City, name=pub_place)
        book = Book(title=title, pub_year=form.pub_year.data, city=city)
        db.session.add(book)
        if publisher:
            publisher, _ = get_or_create(db.session, Publisher, name=pub_name)
            book.publisher=publisher
            db.session.add(publisher)
        if serie:
            serie, _ = get_or_create(db.session, Serie, name=serie, publisher=publisher)
            db.session.add(serie)
        creators = chain(form.authors.data, form.translators.data, form.redactors.data, form.intro.data)
        for creator in creators:
            role = creator['role']
            if creator['id_']:
                c = Creator(person_id=creator['id_'], book=book, role=role)
                db.session.add(c)
            elif creator['name'] != '':
                person = Person(name=creator['name'])
                db.session.add(person)
        book.isbn = form.isbn.data or None
        book.origin_language = form.origin_language.data or None
        book.first_edition = form.first_edition.data or None
        book.genre = form.genre.data or None
        book.literary_form = form.literary_form.data or None
        book.fiction = form.fiction.data or None
        book.precision = form.precision.data or None
        book.nukat = form.nukat.data or None
#        book.subject = form.subject.data or None
#        book.periodic_num = form.book.periodic_num.data or None
        db.session.add(book)
#        copy = Copy(book=book)
#        copy.signature_mark = form.copy.signature_mark.data or None
#        copy.on_shelf = form.copy.on_shelf.data
#        copy.location = form.copy.location.data or None
#        copy.collecion = form.copy.collection.data or None
#        copy.remarques = form.copy.remarques.data or None
#        db.session.add(copy)
        db.session.commit()
    else:
        print(form.errors)
    return render_template('staff/step_form_base.html', form=form)


@bp.route('/staff/add_copy/<int:id>', methods=['GET', 'POST'])
@login_required
def add_copy(id):
    form = CopyForm()
    book = Book.query.get_or_404(id)
    if form.validate_on_submit():
        copy = Copy(book=book)
        copy.signature_mark = form.signature_mark.data or None
        copy.on_shelf = form.on_shelf.data
        copy.location = form.location.data or None
        copy.collection = form.collection.data or None
        copy.remarques = form.remarques.data or None
        db.session.add(copy)
        db.session.commit()
        return redirect(url_for('staff.search_title'))
    else:
        print(form.errors)
    return render_template('staff/add_copy.html', book=book, form=form)

