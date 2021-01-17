from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Shelf
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm
from .publishers import publisher_details

@bp.route('/shelves', methods=['GET', 'POST'])
def shelves_list():
    session['ids'] = []
    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    val = request.args.get('val', None, type=int)

    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        shelves = Shelf.fuzzy_search('name', name)
        s = Shelf.query.filter(Shelf.id.in_([item['id'] for item in shelves]))
    elif val:
        s = Shelf.query.filter_by(room_id=val)
    else:
        s = Shelf.query
    
    if scope == 'all':
        s = s.order_by('name').paginate(page, 20, False)
    elif scope == 'incorrect':
        s = s.filter_by(incorrect=True).order_by('name').paginate(page, 20, False)
#    if request.method == 'POST':
#        id_list = request.form.getlist('shelf_id')
#        if len(id_list) > 4:
#            flash("You can't merge more than 4 items at once.")
#            return render_template('repair/series_list.html', 
#            series=s.items, s=s, form=form, scope=scope)
#        elif len(id_list) < 2:
#            flash("You need at least 2 items to merge.")
#            return render_template('repair/series_list.html', 
#            series=s.items, s=s, form=form, scope=scope)
#        session['ids'] = id_list
#        return redirect(url_for('repair.series_merge'))
    return render_template('repair/shelves_list.html', 
            shelves=s.items, s=s, form=form, scope=scope)

#@bp.route('/series/<int:id>', methods=['GET'])
#def serie_details(id):
#    session['ids'] = []
#    serie = Serie.query.get(id)
#    return render_template('repair/serie_details.html', 
#            serie=serie)
#
#@bp.route('/series/<int:id>/edit', methods=['GET', 'POST'])
#def serie_edit(id):
#    session['ids'] = []
#    serie = Serie.query.get(id)
#    form = SerieForm(name=serie.name, 
#            publisher=serie.publisher,
#            approuved=serie.approuved,
#            incorrect=serie.incorrect)
#    if form.validate_on_submit():
#        publisher = form.publisher.data
#        serie_name = form.name.data
#        if serie_name != serie.name:
#            s = Serie.query.filter_by(name=serie_name, publisher=publisher).first()
#            if s:
#                flash(f'''Serie {s.name} of {publisher.name} exists already in the database. \n
#                    You have to merge "{serie.name}" with "{s.name}".\n 
#                    Hit "Show similars" to enable merge.''')
#                return redirect(url_for('repair.serie_edit', id=serie.id))
#        serie.name = serie_name
#        serie.publisher = publisher
#        serie.approuved = form.approuved.data
#        serie.incorrect = form.incorrect.data
#        db.session.add(serie)
#        db.session.commit()
#        return redirect(url_for('repair.serie_details', id=serie.id))
#    return render_template('repair/serie_edit.html', form=form, serie=serie)
#
#@bp.route('/series/merge/', methods=['GET', 'POST'])
#def series_merge():
#    id_list = session.get('ids')
#    series = Serie.query.filter(Serie.id.in_(id_list)).order_by(
#            'publisher_id', 'name').all()
#    if request.method == 'POST':
#        to_exclude = request.form.getlist('exclude')
#        if to_exclude:
#            for item in to_exclude:
#                session['ids'].remove(item)
#                session.modified = True
#                if len(session['ids']) < 2:
#                    flash('You need at least 2 items to merge.')
#                    return redirect(url_for('repair.series_list'))
#            return redirect(url_for('repair.series_merge'))
#        main = Serie.query.get(request.form.get('serie'))
#        for serie in series:
#            if serie.publisher_id != main.publisher_id:
#                flash('You can not merge the series of different publishers. You must merge publishers first.')
#                return redirect(url_for('repair.series_merge', series=series))
#                
#            if serie is not main:
#                main.books.extend(serie.books)
#                db.session.add(main)
#                db.session.delete(serie)
#        db.session.commit()
#        session['ids'] = []
#        return redirect(url_for('repair.serie_details', id=main.id))
#        
#    return render_template('repair/series_to_merge.html', series=series)
