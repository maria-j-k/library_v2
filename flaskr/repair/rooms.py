from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Room, Shelf
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, RoomForm

@bp.route('/rooms', methods=['GET', 'POST'])
def rooms_list():
    session['ids'] = []
    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        rooms, total = Room.fuzzy_search(name, page, 20)
        print(total)
        next_url = url_for('repair.rooms_list', name=name, page=page + 1) \
            if total > page * 20 else None
        prev_url = url_for('repair.rooms_list', name=name, page=page - 1) \
            if page > 1 else None
        return render_template('repair/rooms_list.html', page=page,
                rooms=rooms, form=form, next_url=next_url, prev_url=prev_url)
        
    elif scope == 'incorrect':
        r = Room.query.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
    elif scope == 'all':
        r = Room.query.order_by('name').paginate(
                        page, 20, False)
    if request.method == 'POST':
        id_list = request.form.getlist('room_id')
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return render_template('repair/rooms_list.html', 
            rooms=r.items, r=r, form=form, scope=scope)
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return render_template('repair/rooms_list.html', 
            rooms=r.items, r=r, form=form, scope=scope)
        session['ids'] = id_list
        return redirect(url_for('repair.rooms_merge'))
    return render_template('repair/rooms_list.html', 
            rooms=r.items, r=r, form=form, scope=scope)


@bp.route('/rooms/<int:id>', methods=['GET'])
def room_details(id):
    session['ids'] = []
    room = Room.query.get(id)
    return render_template('repair/room_details.html', room=room)

@bp.route('/rooms/<int:id>/edit', methods=['GET', 'POST'])
def room_edit(id):
    session['ids'] = []
    room = Room.query.get(id)
    form = RoomForm(name=room.name, 
            incorrect=room.incorrect,
            approuved=room.approuved)
    if form.validate_on_submit():
        room_name = form.name.data
        if room_name != room.name:
            r = Room.query.filter_by(name=room_name).first()
            if r:
                flash(f'''Room {r.name} exists already in the database. \n
                    You have to merge "{room.name}" with "{r.name}".\n 
                    Hit "Show similars" to enable merge.''')
                return redirect(url_for('repair.room_edit', id=room.id))
        room.name = room_name
        room.approuved = form.approuved.data
        room.incorrect = form.incorrect.data
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('repair.room_details', id=room.id))
            
    return render_template('repair/room_edit.html',form=form, room=room)

@bp.route('/roomss/merge/', methods=['GET', 'POST'])
def rooms_merge():
    id_list = session.get('ids')
    rooms = Room.query.filter(Room.id.in_(id_list)).all()
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.rooms_list'))
            return redirect(url_for('repair.rooms_merge'))
        main = Room.query.get(request.form.get('room'))
        for room in rooms:
            if room is not main:
                main.shelves.extend(room.shelves)
                db.session.add(main)
                db.session.delete(room)
        db.session.commit()
        session['ids'] = []
        return redirect(url_for('repair.room_details', id=main.id))
        
    return render_template('repair/rooms_to_merge.html', rooms=rooms)
