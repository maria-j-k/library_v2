import math
from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Book, City, Creator, Person, Publisher, Serie
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import (BookForm, CityForm, CreatorForm, PublisherForm, SearchForm, SerieForm)
from .publishers import publisher_details


@bp.route('/books', methods=['GET', 'POST'])
def books_list():
    session['ids'] = []

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    val = request.args.get('val', None, type=int)
    domain = request.args.get('domain', None, type=str)
    
    form = SearchForm()
    page = request.args.get('page', 1, type=int)

    b = Book.query
    if request.method == 'POST':
        id_list = request.form.getlist('book_id')
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return redirect(url_for('repair.books_list', name=name))
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return redirect(url_for('repair.books_list', name=name))
        session['ids'] = id_list
        return redirect(url_for('repair.books_merge'))

    if name:
        books, total = Book.fuzzy_search(name, page,20)
        print(total)
        next_url = url_for('repair.books_list', name=name, page=page + 1) \
            if total > page * 20 else None
        prev_url = url_for('repair.books_list', name=name, page=page - 1) \
            if page > 1 else None
        total_pages = math.ceil(total/20)
        return render_template('repair/books_list.html', books=books, form=form, 
                page=page,next_url=next_url, prev_url=prev_url, total_pages=total_pages)
    elif domain:
        if domain == 'pub':
            b = b.filter_by(publisher_id=val)
        elif domain == 'serie':
            b = b.filter_by(serie_id=val)
        elif domain == 'city':
            b = b.filter_by(city_id=val)
        elif domain == 'person':
            b = Book.query.join(Creator).join(Person).filter(Creator.person_id==val)
        elif domain == 'author':
            b = Book.query.join(Creator).join(Person).filter(
                    Creator.person_id==val, Creator.role=='A')
        elif domain == 'translator':
            b = Book.query.join(Creator).join(Person).filter(
                    Creator.person_id==val, Creator.role=='T')
        elif domain == 'red':
            b = Book.query.join(Creator).join(Person).filter(
                    Creator.person_id==val, Creator.role=='R')
        elif domain == 'intro':
            b = Book.query.join(Creator).join(Person).filter(
                    Creator.person_id==val, Creator.role=='I')
        
    if scope == 'all':
        b = b.order_by('title').paginate(page, 20, False)
    elif scope == 'incorrect':
        b = b.filter_by(incorrect=True).order_by(
                'title').paginate(page, 20, False)
    return render_template('repair/books_list.html', books=b.items, 
            b=b, form=form, scope=scope, domain=domain, val=val, name=name)


@bp.route('/books/<int:id>', methods=['GET'])
def book_details(id):
    session['ids'] = []
    book = Book.query.get(id)
    return render_template('repair/book_details.html', book=book)


## TODO edycja obiektów zależnych resetuje zmiany w polach formularza. Ajax?
@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def book_edit(id):
    session['ids'] = []
    book = Book.query.get(id)
    form = BookForm(title=book.title, 
            isbn = book.isbn or None,
            authors = book.print_authors() or None,
            translation = book.print_trans() or None,
            redaction = book.print_red() or None,
            introduction = book.print_intro() or None,
            publisher = book.publisher.name if book.publisher else None,
            publisher_id = book.publisher_id if book.publisher else None,
            serie = book.serie.name if book.serie else None,
            city = book.city.name if book.city else None,
            pub_year = book.pub_year,
            origin_language = book.origin_language or None,
            fiction = book.fiction, 
            literary_form = book.literary_form,
            genre = book.genre,
            precision = book.precision,
            nukat = book.nukat,
            incorrect = book.incorrect,
            approuved = book.approuved)
    if form.validate_on_submit():
        book.title = form.title.data
        book.isbn = form.isbn.data
        book.pub_year = form.pub_year.data
        book.origin_language = form.origin_language.data
        book.fiction = form.fiction.data 
        book.literary_form = form.literary_form.data
        book.genre = form.genre.data
        book.precision = form.precision.data
        book.nukat = form.nukat.data
        book.incorrect = form.incorrect.data
        book.approuved = form.approuved.data
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('repair.book_details', id=book.id))
#            
    return render_template('repair/book_edit.html', form=form, book=book)
#
@bp.route('/books/<int:id>/edit/publisher', methods=['GET', 'POST'])
def book_edit_publisher(id):
    session['ids'] = []
    book = Book.query.get_or_404(id)
    form = PublisherForm(name = book.publisher, name_id=book.publisher.id)
    if form.validate_on_submit():
        if form.name_id.data and form.name_id.data !=book.publisher_id:
            publisher = book.publisher
            new_pub = Publisher.query.get(form.name_id.data)
            if new_pub is not None:
                book.publisher_id = new_pub.id
                db.session.add(book)
                if publisher.books.count() == 0:
                    db.session.delete(publisher)
                db.session.commit()
            else:
                flush('We didn\'t succeed to change publisher. Try again')
        elif not form.name_id.data:
            new_publisher = Publisher(name = form.name.data)
            book.publisher = new_publisher
            db.session.add(book)
            if publisher.books.count() == 0:
                db.session.delete(publisher)
            db.session.commit()

        return redirect(url_for('repair.book_edit', id=book.id))
    return render_template('repair/book_edit_related.html', form=form)


@bp.route('/books/<int:id>/edit/<int:pub_id>/serie', methods=['GET', 'POST'])
def book_edit_serie(id, pub_id):
    print('jestem tu')
    session['ids'] = []
    book = Book.query.get_or_404(id)
    form = SerieForm(name = book.serie, 
            name_id=book.serie_id,
            publisher=book.publisher)
    if form.validate_on_submit():
        print(form.name_id.data)
        if form.name_id.data and form.name_id.data !=book.serie_id:
            new_serie = Serie.query.get(form.name_id.data)
            serie = book.serie
            if new_serie is not None:
                book.serie_id = new_serie.id
                db.session.add(book)
                if serie.books.count() == 0:
                    db.session.delete(serie)
                db.session.commit()
            else:
                flush('We didn\'t succeed to change serie. Try again')
        elif not form.name_id.data:
            new_serie = Serie(name = form.name.data, publisher_id=pub_id)
            serie = book.serie
            book.serie = new_serie
            db.session.add(book)
            if serie.books.count() == 0:
                db.session.delete(serie)
            db.session.commit()

        return redirect(url_for('repair.book_edit', id=book.id))
    print(form.errors)
    return render_template('repair/book_edit_related.html', form=form)


@bp.route('/books/<int:id>/edit/city', methods=['GET', 'POST'])
def book_edit_city(id):
    session['ids'] = []
    book = Book.query.get_or_404(id)
    form = CityForm(name = book.city, name_id=book.city_id)
    if form.validate_on_submit():
        if form.name_id.data and form.name_id.data !=book.city_id:
            new_city = City.query.get(form.name_id.data)
            if new_city is not None:
                book.city_id = new_city.id
                db.session.add(book)
                db.session.commit()
            else:
                flush('We didn\'t succeed to change publication place. Try again')
        elif not form.name_id.data:
            city = City(name = form.name.data)
            book.city = city
            db.session.add(city)
            db.session.commit()
#
        return redirect(url_for('repair.book_edit', id=book.id))
    return render_template('repair/book_edit_related.html', form=form)


@bp.route('/books/<int:id>/edit/<role>/person', methods=['GET', 'POST'])
def book_edit_creators(id, role):
    session['ids'] = []
    book = Book.query.get_or_404(id)
    if role == 'authors':
        person_list = [p.person for p in book.authors()]
    elif role == 'translators':
        person_list = [p.person for p in book.translators()]
    elif role == 'redaction':
        person_list = [p.person for p in book.redaction()]
    elif role == 'introduction':
        person_list = [p.person for p in book.introduction()]
    else:
        print('return 404')
    form = CreatorForm()
    default = role[0].upper()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_person_list =[]
            for f in form.creators:
                if f.form.name_id.data:
                    person = Person.query.get_or_404(f.form.name_id.data)
                    new_person_list.append(person)
                elif f.form.name.data and not f.form.name_id.data:
                    person = Person(name=f.form.name.data)
                    new_person_list.append(person)
            for p in new_person_list:
                if p not in person_list:
                    c = Creator(person=p, book=book, role=default)
                    db.session.add(c)
            db.session.commit()
            
            for p in person_list:
                if p not in new_person_list:
                    c = book.creator.filter_by(person_id = p.id).first()
                    db.session.delete(c)
                    if p.creator.count() < 1:
                        db.session.delete(p)
            db.session.commit()
            
            return redirect(url_for('repair.book_edit', id=book.id))
        else: 
            print(form.errors)
            return render_template('repair/book_edit_creators.html', form=form, role=role)
    
    for i in range(3):
        if i < len(person_list):
            data = {'name': person_list[i].name, 
                    'name_id': person_list[i].id,
                    'approuved': person_list[i].approuved,
                    'incorrect': person_list[i].incorrect,
                    'role': default
                    }
            form.creators.append_entry(data)
        else:
            form.creators.append_entry({'role': default})
    return render_template('repair/book_edit_creators.html', form=form, role=role)

@bp.route('/books/merge/', methods=['GET', 'POST'])
def books_merge():
    id_list = session.get('ids')
    books = Book.query.filter(Book.id.in_(id_list)).all()
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.books_list'))
            return redirect(url_for('repair.books_merge'))
        main = Book.query.get(request.form.get('book'))
        for book in books:
            if book is not main:
                main.copies.extend(book.copies)
                db.session.add(main)
                db.session.delete(book)
        db.session.commit()
        session['ids'] = []
        return redirect(url_for('repair.book_details', id=main.id))
        
    return render_template('repair/books_to_merge.html', books=books)
