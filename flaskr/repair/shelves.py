from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Shelf, Room
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm, ShelfForm
from .publishers import publisher_details

@bp.route('/shelves', methods=['GET', 'POST'])
def shelves_list():
    session['ids'] = []
    
    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    val = request.args.get('val', None, type=int)
    page = request.args.get('page', 1, type=int)

    form = SearchForm()
    
    if request.method == 'GET':
        if name:
            shelves, total = Shelf.fuzzy_search(name, page, 20)
            if scope == 'incorrect':
                shelves = shelves.filter_by(incorrect=True)
            next_url = url_for('repair.shelves_list', name=name, page=page + 1) \
                if total > page * 20 else None
            prev_url = url_for('repair.shelves_list', name=name, page=page - 1) \
                if page > 1 else None
            return render_template('repair/shelves_list.html', page=page,
                    shelves=shelves, form=form, next_url=next_url, prev_url=prev_url)
        elif val:
            s = Shelf.query.filter_by(room_id=val)
        else:
            s = Shelf.query
        
        if scope == 'all':
            s = s.order_by('name').paginate(page, 20, False)
        elif scope == 'incorrect':
            s = s.filter_by(incorrect=True).order_by('name').paginate(page, 20, False)
    elif request.method == 'POST':
        id_list = request.form.getlist('shelf_id')
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return render_template('repair/shelves_list.html', 
            shelves=s.items, s=s, form=form, scope=scope)
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return render_template('repair/shelves_list.html', 
            shelves=s.items, s=s, form=form, scope=scope)
        session['ids'] = id_list
        return redirect(url_for('repair.shelves_merge'))
    return render_template('repair/shelves_list.html', 
            shelves=s.items, s=s, form=form, scope=scope)

@bp.route('/shelves/<int:id>', methods=['GET'])
def shelf_details(id):
    session['ids'] = []
    shelf = Shelf.query.get(id)
    return render_template('repair/shelf_details.html', 
            shelf=shelf)

@bp.route('/shelves/<int:id>/edit', methods=['GET', 'POST'])
def shelf_edit(id):
    session['ids'] = []
    shelf = Shelf.query.get(id)
    form = ShelfForm(name=shelf.name, 
            room=shelf.room,
            approuved=shelf.approuved,
            incorrect=shelf.incorrect)
    if form.validate_on_submit():
        room = form.room.data
        print(room.id, room.name)
        shelf_name = form.name.data
        if shelf_name != shelf.name:
            s = Shelf.query.filter_by(name=shelf_name, room=room).first()
            if s:
                flash(f'''Shelf {s.name} in {room.name} exists already in the database. \n
                    You have to merge "{shelf.name}" with "{s.name}".\n 
                    Hit "Show similars" to enable merge.''')
                return redirect(url_for('repair.shelf_edit', id=shelf.id))
        shelf.name = shelf_name
        shelf.room = room
        shelf.approuved = form.approuved.data
        shelf.incorrect = form.incorrect.data
        db.session.add(shelf)
        db.session.commit()
        return redirect(url_for('repair.shelf_details', id=shelf.id))
    return render_template('repair/shelf_edit.html', form=form, shelf=shelf)

@bp.route('/shelves/merge/', methods=['GET', 'POST'])
def shelves_merge():
    id_list = session.get('ids')
    shelves = Shelf.query.filter(Shelf.id.in_(id_list)).order_by('name').all()
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.shelves_list'))
            return redirect(url_for('repair.shelves_merge'))
        main = Shelf.query.get(request.form.get('shelf'))
        for shelf in shelves:
            if shelf.room_id != main.room_id:
                flash('''You can not merge the shelves from different rooms.\n 
                        You must change shelf\'s room first.''')
                return redirect(url_for('repair.shelves_merge', shelves=shelves))
                
            if shelf is not main:
                main.copies.extend(shelf.copies)
                db.session.add(main)
                db.session.delete(shelf)
        db.session.commit()
        session['ids'] = []
        return redirect(url_for('repair.shelf_details', id=main.id))
        
    return render_template('repair/shelves_to_merge.html', shelves=shelves)
