from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Book, City, Collection, Copy, Creator, Location, Person, Publisher, Serie
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import PublisherForm, SearchForm

@bp.route('/publishers', methods=['GET', 'POST'])
def publishers_list():
    if request.method == 'POST':
        id_list = request.form.getlist('publisher_id')
        session['ids'] = id_list
        return redirect(url_for('repair.publishers_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
#    if form.validate_on_submit():
#        q = form.name.data
#        publishers = Publisher.fuzzy_search(q)
#        pubs = Publisher.query.filter(Publisher.id.in_(
#            [item['id'] for item in publishers])).paginate(page, 20, False)
    if name:
        publishers = Publisher.fuzzy_search('name', name)
        pubs = Publisher.query.filter(Publisher.id.in_(
            [item['id'] for item in publishers])).paginate(page, 20, False)
        
    elif scope == 'incorrect':
        pubs = Publisher.query.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
    elif scope == 'all':
        pubs = Publisher.query.order_by('name').paginate(
                        page, 20, False)
    return render_template('repair/publishers_list.html', 
            publishers=pubs.items, pubs=pubs,
            form=form, scope=scope)


@bp.route('/publishers/<int:id>/series', methods=['GET', 'POST'])
def publisher_series(id):
    publisher = Publisher.query.get(id)
    if request.method == 'POST':
        id_list = request.form.getlist('serie_id')
        session['ids'] = id_list
        return redirect(url_for('repair.series_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    series = Serie.query.filter_by(publisher_id=publisher.id)   
    if name:
        publishers = Publisher.fuzzy_search(name)
        pubs = Publisher.query.filter(Publisher.id.in_(
            [item['id'] for item in publishers])).paginate(page, 20, False)
    elif scope == 'incorrect':
        s = series.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
    elif scope == 'all':
        s = series.order_by('name').paginate(page, 20, False)
    return render_template('repair/series_list.html', 
            series=s.items, s=s, form=form, scope=scope)


@bp.route('/publishers/<int:id>', methods=['GET'])
def publisher_details(id):
    publisher = Publisher.query.get(id)
    return render_template('repair/publisher_details.html', 
            publisher=publisher)

@bp.route('/publishers/<int:id>/edit', methods=['GET', 'POST'])
def publisher_edit(id):
    publisher = Publisher.query.get(id)
    form = PublisherForm(name=publisher.name)
    if form.validate_on_submit():
        publisher_name = form.name.data
        p = Publisher.query.filter_by(name=publisher_name).first()
        if p:
            flash(f'''Publisher {p.name} exists already in the database. \n
                    You have to merge "{publisher.name}" with "{p.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            publisher.name = publisher_name
            db.session.add(publisher)
            db.session.commit()
            return redirect(url_for('repair.publisher_details', 
                id=publisher.id))
            
    return render_template('repair/publisher_edit.html', 
            form=form, publisher=publisher)

@bp.route('/publishers/merge/', methods=['GET', 'POST'])
def publishers_merge():
    '''dodać funkcję usuwania z listy rekordów do łączenia. w templatce już jest checkbox nazwa exclude'''
    id_list = session.get('ids')
    publishers = Publisher.query.filter(Publisher.id.in_(id_list)).order_by('name').all()
    if request.method == 'POST':
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            publishers = Publisher.query.filter(Publisher.id.in_(id_list)).order_by('name').all()
            print(id_list)
            return redirect(url_for('repair.publishers_merge', publishers=publishers))
        main = Publisher.query.get(request.form.get('publisher'))
        for publisher in publishers:
            if publisher is not main:
                main.books.extend(publisher.books)
                main.series.extend(publisher.series)
                db.session.add(main)
                db.session.delete(publisher)
        db.session.commit()
        return redirect(url_for('repair.publisher_details', id=main.id))
        
    return render_template('repair/publishers_to_merge.html', publishers=publishers)
