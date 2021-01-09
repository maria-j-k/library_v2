from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Location
from flaskr.repair import bp
from .forms import LocationForm, SearchForm

@bp.route('/locations', methods=['GET', 'POST'])
def locations_list():
    if request.method == 'POST':
        id_list = request.form.getlist('location_id')
        session['ids'] = id_list
        return redirect(url_for('repair.locations_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        locations = Location.fuzzy_search('room', name)
        l = Location.query.filter(Location.id.in_(
            [item['id'] for item in locations])
            ).order_by('room').paginate(page, 20, False)
        
    elif scope == 'incorrect':
        l = Location.query.filter_by(incorrect=True).order_by(
                'room').paginate(page, 20, False)
    elif scope == 'all':
        l = Location.query.order_by('room').paginate(page, 20, False)
    return render_template('repair/locations_list.html', 
            locations = l.items, l=l,
            form=form, scope=scope)

@bp.route('/locations/<int:id>', methods=['GET'])
def location_details(id):
    location = Location.query.get(id)
    return render_template('repair/location_details.html', 
            location=location)

@bp.route('/locations/<int:id>/edit', methods=['GET', 'POST'])
def location_edit(id):
    location = Location.query.get(id)
    form = LocationForm(room=location.room)
    if form.validate_on_submit():
        location_room = form.room.data
        l = Location.query.filter_by(room=location_room).first()
        if c:
            flash(f'''Location {l.room} exists already in the database. \n
                    You have to merge "{location_room}" with "{l.room}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            location.room = location_room
            db.session.add(location)
            db.session.commit()
            return redirect(url_for('repair.location_details', id=location.id))
            
    return render_template('repair/location_edit.html', 
            form=form, location=location)

@bp.route('/locations/merge/', methods=['GET', 'POST'])
def locations_merge():
    id_list = session.get('ids')
    locations = Location.query.filter(Location.id.in_(id_list)
            ).order_by('room').all()
    if request.method == 'POST':
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            locations = Location.query.filter(Location.id.in_(id_list)
                    ).order_by('room').all()
            return redirect(url_for('repair.locations_merge',
                locations=locations))
        main = Location.query.get(request.form.get('location'))
        for location in locations:
            if location is not main:
                main.copies.extend(location.copies)
                db.session.add(main)
                db.session.delete(location)
        db.session.commit()
        return redirect(url_for('repair.location_details', id=main.id))
        
    return render_template('repair/locations_to_merge.html',
            locations=locations)
