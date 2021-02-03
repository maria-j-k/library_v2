from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import City 
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, CityForm

@bp.route('/cities', methods=['GET', 'POST'])
def cities_list():
    session['ids'] = []

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    page = request.args.get('page', 1, type=int)
    
    form = SearchForm()
    
    if request.method == 'GET':
        if name:
            cities, total = City.fuzzy_search(name, page, 20)
            if scope == 'incorrect':
                cities = cities.filter_by(incorrect=True)
            next_url = url_for('repair.cities_list', name=name, page=page + 1) \
                if total > page * 20 else None
            prev_url = url_for('repair.cities_list', name=name, page=page - 1) \
                if page > 1 else None
            return render_template('repair/cities_list.html', cities=cities, form=form,
                               page=page, next_url=next_url, prev_url=prev_url)
            
        elif scope == 'incorrect':
            c = City.query.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
        elif scope == 'all':
            c = City.query.order_by('name').paginate(page, 20, False)

    elif request.method == 'POST':
        id_list = request.form.getlist('city_id')
        print(id_list)
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return render_template('repair/cities_list.html', 
            cities=c.items, c=c, form=form, scope=scope)
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return render_template('repair/cities_list.html', 
            cities=c.items, c=c, form=form, scope=scope)
        session['ids'] = id_list
        return redirect(url_for('repair.cities_merge'))
    return render_template('repair/cities_list.html', 
            cities=c.items, c=c,
            form=form, scope=scope)

@bp.route('/cities/<int:id>', methods=['GET'])
def city_details(id):
    session['ids'] = []
    city = City.query.get(id)
    return render_template('repair/city_details.html', city=city)

@bp.route('/cities/<int:id>/edit', methods=['GET', 'POST'])
def city_edit(id):
    session['ids'] = []
    city = City.query.get(id)
    form = CityForm(name=city.name, 
            incorrect=city.incorrect,
            approuved=city.approuved)
    if form.validate_on_submit():
        city_name = form.name.data
        if city_name != city.name:
            c = City.query.filter_by(name=city_name).first()
            if c:
                flash(f'''City {c.name} exists already in the database. \n
                    You have to merge "{city.name}" with "{c.name}".\n 
                    Hit "Show similars" to enable merge.''')
                return redirect(url_for('repair.city_edit', id=city.id))
        city.name = city_name
        city.approuved = form.approuved.data
        city.incorrect = form.incorrect.data
        db.session.add(city)
        db.session.commit()
        return redirect(url_for('repair.city_details', id=city.id))
            
    return render_template('repair/city_edit.html', form=form, city=city)

@bp.route('/cities/merge/', methods=['GET', 'POST'])
def cities_merge():
    id_list = session.get('ids')
    cities = City.query.filter(City.id.in_(id_list)).order_by('name').all()
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.cities_list'))
            return redirect(url_for('repair.cities_merge'))
        main = City.query.get(request.form.get('city'))
        for city in cities:
            if city is not main:
                main.books.extend(city.books)
                db.session.add(main)
                db.session.delete(city)
        db.session.commit()
        session['ids'] = []
        return redirect(url_for('repair.city_details', id=main.id))
        
    return render_template('repair/cities_to_merge.html', cities=cities)
