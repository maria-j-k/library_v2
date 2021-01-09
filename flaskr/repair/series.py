from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Serie 
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, SerieForm
from .publishers import publisher_details

@bp.route('/series', methods=['GET', 'POST'])
def series_list():
    if request.method == 'POST':
        id_list = request.form.getlist('serie_id')
        session['ids'] = id_list
        return redirect(url_for('repair.series_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        series = Serie.fuzzy_search(name)
        s = Serie.query.filter(Serie.id.in_([item['id'] for item in series])
                ).order_by('publisher_id').paginate(page, 20, False)
        
    elif scope == 'incorrect':
        s = Serie.query.filter_by(incorrect=True).order_by('publisher_id',
                    'name').paginate(page, 20, False)
    elif scope == 'all':
        s = Serie.query.order_by('publisher_id', 'name').paginate(
                        page, 20, False)
    return render_template('repair/series_list.html', 
            series=s.items, s=s,
            form=form, scope=scope)

@bp.route('/series/<int:id>', methods=['GET'])
def serie_details(id):
    serie = Serie.query.get(id)
    return render_template('repair/serie_details.html', 
            serie=serie)

@bp.route('/series/<int:id>/edit', methods=['GET', 'POST'])
def serie_edit(id):
    serie = Serie.query.get(id)
    form = SerieForm(name=serie.name)
    if form.validate_on_submit():
        serie_name = form.name.data
        s = Serie.query.filter_by(name=serie_name).first()
        if s:
            flash(f'''Serie {s.name} exists already in the database. \n
                    You have to merge "{serie.name}" with "{s.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            serie.name = serie_name
            db.session.add(serie)
            db.session.commit()
            return redirect(url_for('repair.serie_details', 
                id=serie.id))
            
    return render_template('repair/serie_edit.html', form=form, serie=serie)

@bp.route('/series/merge/', methods=['GET', 'POST'])
def series_merge():
    id_list = session.get('ids')
    series = Serie.query.filter(Serie.id.in_(id_list)).order_by(
            'publisher_id', 'name').all()
    if request.method == 'POST':
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            series = Serie.query.filter(Serie.id.in_(id_list)
                    ).order_by('publisher_id', 'name').all()
            print(id_list)
            return redirect(url_for('repair.series_merge', series=series))
        main = Serie.query.get(request.form.get('serie'))
        print(f'main {main.publisher_id}')
        for serie in series:
            print(f'serie: {serie.publisher_id}')
            if serie.publisher_id != main.publisher_id:
                flash('You can not merge the series of different publishers. You must merge publishers first.')
                return redirect(url_for('repair.series_merge', series=series))
                
            if serie is not main:
                main.books.extend(serie.books)
                db.session.add(main)
                db.session.delete(serie)
                print(f'count: {main.books.count()}')
        db.session.commit()
        return redirect(url_for('repair.serie_details', id=main.id))
        
    return render_template('repair/series_to_merge.html', series=series)
