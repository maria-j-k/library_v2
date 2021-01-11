from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import City 
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, CityForm

@bp.route('/cities', methods=['GET', 'POST'])
def cities_list():
    if request.method == 'POST':
        id_list = request.form.getlist('city_id')
        session['ids'] = id_list
        return redirect(url_for('repair.cities_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        cities = City.fuzzy_search('name', name)
        c = City.query.filter(City.id.in_([item['id'] for item in cities])
                ).order_by('name').paginate(page, 20, False)
        
    elif scope == 'incorrect':
        c = City.query.filter_by(incorrect=True).order_by(
                'name').paginate(page, 20, False)
    elif scope == 'all':
        c = City.query.order_by('name').paginate(page, 20, False)
    return render_template('repair/cities_list.html', 
            cities=c.items, c=c,
            form=form, scope=scope)

@bp.route('/cities/<int:id>', methods=['GET'])
def city_details(id):
    city = City.query.get(id)
    return render_template('repair/city_details.html', city=city)

@bp.route('/cities/<int:id>/edit', methods=['GET', 'POST'])
def city_edit(id):
    city = City.query.get(id)
    form = CityForm(name=city.name)
    if form.validate_on_submit():
        city_name = form.name.data
        if city_name != city.name:
            c = City.query.filter_by(name=city_name).first()
            if c:
                flash(f'''City {c.name} exists already in the database. \n
                    You have to merge "{city.name}" with "{c.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
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
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            cities = City.query.filter(City.id.in_(id_list)
                    ).order_by('name').all()
            return redirect(url_for('repair.cities_merge', cities=cities))
        main = City.query.get(request.form.get('city'))
        for city in cities:
            if city is not main:
                main.books.extend(city.books)
                db.session.add(main)
                db.session.delete(city)
        db.session.commit()
        return redirect(url_for('repair.city_details', id=main.id))
        
    return render_template('repair/cities_to_merge.html', cities=cities)
