from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Book, City, Creator, Person, Publisher, Serie
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import BookForm, CityForm, PublisherForm, SearchForm, SerieForm
from .publishers import publisher_details

@bp.route('/books', methods=['GET', 'POST'])
def books_list():
    if request.method == 'POST':
        id_list = request.form.getlist('book_id')
        session['ids'] = id_list
        return redirect(url_for('repair.books_merge'))

    scope = request.args.get('filter', 'all', type=str)
    print(f'scope: {scope}')
    name = request.args.get('name', None)
    val = request.args.get('val', None, type=int)
    domain = request.args.get('domain', None, type=str)
    
    form = SearchForm()
    page = request.args.get('page', 1, type=int)

    b = Book.query
    if name:
        print(name)
        books = Book.fuzzy_search('title', name)
        b = b.filter(Book.id.in_([item['id'] for item in books]))
    elif domain:
        if domain == 'pub':
            b = b.filter_by(publisher_id=val)
        elif domain == 'serie':
            b = b.filter_by(serie_id=val)
        elif domain == 'person':
            b = Book.query.join(Creator).join(Person).filter(
                    Creator.person_id==val)
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
    return render_template('repair/books_list.html', 
            books=b.items, b=b, form=form, scope=scope)

@bp.route('/books/<int:id>', methods=['GET'])
def book_details(id):
    book = Book.query.get(id)
    return render_template('repair/book_details.html', book=book)

@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def book_edit(id):
    book = Book.query.get(id)
    form = BookForm(title=book.title, 
            isbn = book.isbn or None,
            authors = book.print_authors() or None,
            publisher = book.publisher.name if book.publisher else None,
            serie = book.serie.name if book.serie else None,
            city = book.city.name if book.city else None,
            pub_year = book.pub_year,
            fiction = book.fiction, 
            literary_form = book.literary_form,
            genre = book.genre,
            precision = book.precision,
            nukat = book.nukat,
            incorrect = book.incorrect,
            approuved = book.approuved)
#    if form.validate_on_submit():
#        book_title = form.title.data
#        isbn = form.isbn.data
#        pub_year = form.pub_year.data
#        fiction = form.fiction.data 
#        literary_form = form.literary_form.data
#        genre = form.genre.data
#        precision = form.precision.data
#        nukat = form.nukat.data
#        incorrect = form.incorrect.data
#        approuved = form.approuved.data
#        b = Book.query.filter_by(title=book_title).first()
#        if b:
#            flash(f'''Book {b.title} exists already in the database. \n
#                    You have to merge "{book.title}" with "{b.title}".\n 
#                    Hit "Show similars" to enable merge.''')
#        else:
#            book.title = book_title
#            book.isbn = form.isbn.data
#            book.pub_year = form.pub_year.data
#            book.fiction = form.fiction.data 
#            book.literary_form = form.literary_form.data
#            book.genre = form.genre.data
#            book.precision = form.precision.data
#            book.nukat = form.nukat.data
#            book.incorrect = form.incorrect.data
#            book.approuved = form.approuved.data
#            b = Book.query.filter_by(title=book_title).first()
#            db.session.add(book)
##            db.session.commit()
#            return redirect(url_for('repair.book_details', id=book.id))
#            
    return render_template('repair/book_edit.html', form=form, book=book)
#
@bp.route('/books/<int:id>/edit/publisher', methods=['GET', 'POST'])
def book_edit_publisher(id):
    book = Book.query.get_or_404(id)
    form = PublisherForm(name = book.publisher
            , name_id=book.publisher.id
            )
    if form.validate_on_submit():
        if form.name_id.data and form.name_id.data !=book.publisher_id:
            new_pub = Publisher.query.get(form.name_id.data)
            if new_pub is not None:
                book.publisher_id = new_pub.id
                db.session.add(book)
                db.session.commit()
            else:
                flush('We didn\'t succeed to change publisher. Try again')
        elif not form.name_id.data:
            publisher = Publisher(name = form.name.data)
            book.publisher = publisher
            db.session.add(book)
            db.session.commit()

        return redirect(url_for('repair.book_edit', id=book.id))
    return render_template('repair/book_edit_related.html', form=form)


@bp.route('/books/<int:id>/edit/<int:pub_id>/serie', methods=['GET', 'POST'])
def book_edit_serie(id, pub_id):
    book = Book.query.get_or_404(id)
    form = SerieForm(name = book.serie, name_id=book.serie_id)
    if form.validate_on_submit():
        print(form.name_id.data)
        if form.name_id.data and form.name_id.data !=book.serie_id:
            new_serie = Serie.query.get(form.name_id.data)
            if new_serie is not None:
                book.serie_id = new_serie.id
                db.session.add(book)
                db.session.commit()
            else:
                flush('We didn\'t succeed to change serie. Try again')
        elif not form.name_id.data:
            serie = Serie(name = form.name.data, publisher_id=pub_id)
            book.serie = serie
            db.session.add(book)
            db.session.commit()

        return redirect(url_for('repair.book_edit', id=book.id))
    return render_template('repair/book_edit_related.html', form=form)


@bp.route('/books/<int:id>/edit/city', methods=['GET', 'POST'])
def book_edit_city(id):
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
#@bp.route('/books/merge/', methods=['GET', 'POST'])
#def books_merge():
#    id_list = session.get('ids')
#    books = Book.query.filter(Book.id.in_(id_list)).order_by('title').all()
#    if request.method == 'POST':
#        to_exclude = request.form.get('exclude')
#        if to_exclude:
#            id_list.remove(to_exclude)
#            books = Book.query.filter(Book.id.in_(id_list)).order_by('title').all()
#            return redirect(url_for('repair.books_merge', books=books))
#
#        main = Book.query.get(request.form.get('book'))
#        for book in books:
#            if book is not main:
#                main.books.extend(serie.books)
#                db.session.add(main)
#                db.session.delete(serie)
#                print(f'count: {main.books.count()}')
#        db.session.commit()
#        return redirect(url_for('repair.serie_details', id=main.id))
#        
#    return render_template('repair/series_to_merge.html', series=series)
