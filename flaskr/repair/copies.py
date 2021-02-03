import math
from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Book, Collection, Copy, Room, Shelf
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import (BookForm, CityForm, CreatorForm, PublisherForm, SearchForm, SerieForm)


@bp.route('/copies/<domain>/<int:val>', methods=['GET', 'POST'])
def copies_list(domain, val):
    session['ids'] = []

    scope = request.args.get('filter', 'all', type=str)
    page = request.args.get('page', 1, type=int)
    

    c = Copy.query
#    if request.method == 'POST':
#        id_list = request.form.getlist('copy_id')
#        if len(id_list) > 4:
#            flash("You can't merge more than 4 items at once.")
#            return redirect(url_for('repair.copy_list', domain=domain, val=val))
#        elif len(id_list) < 2:
#            flash("You need at least 2 items to merge.")
#            return redirect(url_for('repair.copy_list', domain=domain, val=val))
#        session['ids'] = id_list
#        ### powinno być delete
#        return redirect(url_for('repair.copies_merge'))
#
    if domain == 'book':
        c = c.filter_by(book_id=val)
    elif domain == 'collection':
        c = c.filter_by(collection_id=val)
    elif domain == 'shelf':
        c = c.filter_by(shelf_id=val)
    elif domain == 'room':
        c = Copy.query.join(Shelf, Shelf.id == Copy.shelf_id).join(Room,
                Room.id == Shelf.room_id).filter(Room.id==val)
    
    if scope == 'all':
        c = c.paginate(page, 20, False)
    elif scope == 'incorrect':
        c = c.filter_by(incorrect=True).paginate(page, 20, False)
    return render_template('repair/copies_list.html', copies=c.items, 
            c=c, scope=scope, domain=domain, val=val)


@bp.route('/copies/<int:id>', methods=['GET'])
def copy_details(id):
    copy = Copy.query.get(id)
    return render_template('repair/copy_details.html', copy=copy)


### TODO edycja obiektów zależnych resetuje zmiany w polach formularza. Ajax?
#@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
#def book_edit(id):
#    session['ids'] = []
#    book = Book.query.get(id)
#    form = BookForm(title=book.title, 
#            isbn = book.isbn or None,
#            authors = book.print_authors() or None,
#            translation = book.print_trans() or None,
#            redaction = book.print_red() or None,
#            introduction = book.print_intro() or None,
#            publisher = book.publisher.name if book.publisher else None,
#            publisher_id = book.publisher_id if book.publisher else None,
#            serie = book.serie.name if book.serie else None,
#            city = book.city.name if book.city else None,
#            pub_year = book.pub_year,
#            origin_language = book.origin_language or None,
#            fiction = book.fiction, 
#            literary_form = book.literary_form,
#            genre = book.genre,
#            precision = book.precision,
#            nukat = book.nukat,
#            incorrect = book.incorrect,
#            approuved = book.approuved)
#    if form.validate_on_submit():
#        book.title = form.title.data
#        book.isbn = form.isbn.data
#        book.pub_year = form.pub_year.data
#        book.origin_language = form.origin_language.data
#        book.fiction = form.fiction.data 
#        book.literary_form = form.literary_form.data
#        book.genre = form.genre.data
#        book.precision = form.precision.data
#        book.nukat = form.nukat.data
#        book.incorrect = form.incorrect.data
#        book.approuved = form.approuved.data
#        db.session.add(book)
#        db.session.commit()
#        return redirect(url_for('repair.book_details', id=book.id))
##            
#    return render_template('repair/book_edit.html', form=form, book=book)
##
#@bp.route('/books/<int:id>/edit/publisher', methods=['GET', 'POST'])
#def book_edit_publisher(id):
#    session['ids'] = []
#    book = Book.query.get_or_404(id)
#    form = PublisherForm(name = book.publisher, name_id=book.publisher.id)
#    if form.validate_on_submit():
#        if form.name_id.data and form.name_id.data !=book.publisher_id:
#            publisher = book.publisher
#            new_pub = Publisher.query.get(form.name_id.data)
#            if new_pub is not None:
#                book.publisher_id = new_pub.id
#                db.session.add(book)
#                if publisher.books.count() == 0:
#                    db.session.delete(publisher)
#                db.session.commit()
#            else:
#                flush('We didn\'t succeed to change publisher. Try again')
#        elif not form.name_id.data:
#            new_publisher = Publisher(name = form.name.data)
#            book.publisher = new_publisher
#            db.session.add(book)
#            if publisher.books.count() == 0:
#                db.session.delete(publisher)
#            db.session.commit()
#
#        return redirect(url_for('repair.book_edit', id=book.id))
#    return render_template('repair/book_edit_related.html', form=form)
#
#
#@bp.route('/books/<int:id>/edit/<int:pub_id>/serie', methods=['GET', 'POST'])
#def book_edit_serie(id, pub_id):
#    print('jestem tu')
#    session['ids'] = []
#    book = Book.query.get_or_404(id)
#    form = SerieForm(name = book.serie, 
#            name_id=book.serie_id,
#            publisher=book.publisher)
#    if form.validate_on_submit():
#        print(form.name_id.data)
#        if form.name_id.data and form.name_id.data !=book.serie_id:
#            new_serie = Serie.query.get(form.name_id.data)
#            serie = book.serie
#            if new_serie is not None:
#                book.serie_id = new_serie.id
#                db.session.add(book)
#                if serie.books.count() == 0:
#                    db.session.delete(serie)
#                db.session.commit()
#            else:
#                flush('We didn\'t succeed to change serie. Try again')
#        elif not form.name_id.data:
#            new_serie = Serie(name = form.name.data, publisher_id=pub_id)
#            serie = book.serie
#            book.serie = new_serie
#            db.session.add(book)
#            if serie.books.count() == 0:
#                db.session.delete(serie)
#            db.session.commit()
#
#        return redirect(url_for('repair.book_edit', id=book.id))
#    print(form.errors)
#    return render_template('repair/book_edit_related.html', form=form)
#
#
#@bp.route('/books/<int:id>/edit/city', methods=['GET', 'POST'])
#def book_edit_city(id):
#    session['ids'] = []
#    book = Book.query.get_or_404(id)
#    form = CityForm(name = book.city, name_id=book.city_id)
#    if form.validate_on_submit():
#        if form.name_id.data and form.name_id.data !=book.city_id:
#            new_city = City.query.get(form.name_id.data)
#            if new_city is not None:
#                book.city_id = new_city.id
#                db.session.add(book)
#                db.session.commit()
#            else:
#                flush('We didn\'t succeed to change publication place. Try again')
#        elif not form.name_id.data:
#            city = City(name = form.name.data)
#            book.city = city
#            db.session.add(city)
#            db.session.commit()
##
#        return redirect(url_for('repair.book_edit', id=book.id))
#    return render_template('repair/book_edit_related.html', form=form)
#
#
#@bp.route('/books/<int:id>/edit/<role>/person', methods=['GET', 'POST'])
#def book_edit_creators(id, role):
#    session['ids'] = []
#    book = Book.query.get_or_404(id)
#    if role == 'authors':
#        person_list = [p.person for p in book.authors()]
#    elif role == 'translators':
#        person_list = [p.person for p in book.translators()]
#    elif role == 'redaction':
#        person_list = [p.person for p in book.redaction()]
#    elif role == 'introduction':
#        person_list = [p.person for p in book.introduction()]
#    else:
#        print('return 404')
#    form = CreatorForm()
#    default = role[0].upper()
#    if request.method == 'POST':
#        if form.validate_on_submit():
#            new_person_list =[]
#            for f in form.creators:
#                if f.form.name_id.data:
#                    person = Person.query.get_or_404(f.form.name_id.data)
#                    new_person_list.append(person)
#                elif f.form.name.data and not f.form.name_id.data:
#                    person = Person(name=f.form.name.data)
#                    new_person_list.append(person)
#            for p in new_person_list:
#                if p not in person_list:
#                    c = Creator(person=p, book=book, role=default)
#                    db.session.add(c)
#            db.session.commit()
#            
#            for p in person_list:
#                if p not in new_person_list:
#                    c = book.creator.filter_by(person_id = p.id).first()
#                    db.session.delete(c)
#                    if p.creator.count() < 1:
#                        db.session.delete(p)
#            db.session.commit()
#            
#            return redirect(url_for('repair.book_edit', id=book.id))
#        else: 
#            print(form.errors)
#            return render_template('repair/book_edit_creators.html', form=form, role=role)
#    
#    for i in range(3):
#        if i < len(person_list):
#            data = {'name': person_list[i].name, 
#                    'name_id': person_list[i].id,
#                    'approuved': person_list[i].approuved,
#                    'incorrect': person_list[i].incorrect,
#                    'role': default
#                    }
#            form.creators.append_entry(data)
#        else:
#            form.creators.append_entry({'role': default})
#    return render_template('repair/book_edit_creators.html', form=form, role=role)
#
