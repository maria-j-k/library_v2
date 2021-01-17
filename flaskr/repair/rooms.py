from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Room, Shelf
from flaskr.repair import bp
from scripts.utils import get_or_create
from .forms import SearchForm

@bp.route('/rooms', methods=['GET', 'POST'])
def rooms_list():
    session['ids'] = []
    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        rooms = Room.fuzzy_search('name', name)
        r = Room.query.filter(Room.id.in_(
            [item['id'] for item in rooms])).paginate(page, 20, False)

        
    elif scope == 'incorrect':
        r = Room.query.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
    elif scope == 'all':
        r = Room.query.order_by('name').paginate(
                        page, 20, False)
#    if request.method == 'POST':
#        id_list = request.form.getlist('room_id')
#        if len(id_list) > 4:
#            flash("You can't merge more than 4 items at once.")
#            return render_template('repair/rooms_list.html', 
#            rooms=r.items, r=r, form=form, scope=scope)
#        elif len(id_list) < 2:
#            flash("You need at least 2 items to merge.")
#            return render_template('repair/rooms_list.html', 
#            rooms=r.items, r=r, form=form, scope=scope)
#        session['ids'] = id_list
#        return redirect(url_for('repair.rooms_merge'))
    return render_template('repair/rooms_list.html', 
            rooms=r.items, r=r, form=form, scope=scope)


#@bp.route('/publishers/<int:id>', methods=['GET'])
#def publisher_details(id):
#    session['ids'] = []
#    publisher = Publisher.query.get(id)
#    return render_template('repair/publisher_details.html', 
#            publisher=publisher)
#
#@bp.route('/publishers/<int:id>/edit', methods=['GET', 'POST'])
#def publisher_edit(id):
#    session['ids'] = []
#    publisher = Publisher.query.get(id)
#    form = PublisherForm(name=publisher.name, 
#            incorrect=publisher.incorrect,
#            approuved=publisher.approuved)
#    if form.validate_on_submit():
#        publisher_name = form.name.data
#        if publisher_name != publisher.name:
#            p = Publisher.query.filter_by(name=publisher_name).first()
#            if p:
#                flash(f'''Publisher {p.name} exists already in the database. \n
#                    You have to merge "{publisher.name}" with "{p.name}".\n 
#                    Hit "Show similars" to enable merge.''')
#                return redirect(url_for('repair.publisher_edit', id=publisher.id))
#        publisher.name = publisher_name
#        publisher.approuved = form.approuved.data
#        publisher.incorrect = form.incorrect.data
#        db.session.add(publisher)
#        db.session.commit()
#        return redirect(url_for('repair.publisher_details', id=publisher.id))
#            
#    return render_template('repair/publisher_edit.html', 
#            form=form, publisher=publisher)
#
#@bp.route('/publishers/merge/', methods=['GET', 'POST'])
#def publishers_merge():
#    '''dodać funkcję usuwania z listy rekordów do łączenia. w templatce już jest checkbox nazwa exclude'''
#    id_list = session.get('ids')
#    publishers = Publisher.query.filter(Publisher.id.in_(id_list)).order_by('name').all()
#    if request.method == 'POST':
#        to_exclude = request.form.getlist('exclude')
#        if to_exclude:
#            for item in to_exclude:
#                session['ids'].remove(item)
#                session.modified = True
#                if len(session['ids']) < 2:
#                    flash('You need at least 2 items to merge.')
#                    return redirect(url_for('repair.publishers_list'))
#            return redirect(url_for('repair.publishers_merge'))
#        main = Publisher.query.get(request.form.get('publisher'))
#        for publisher in publishers:
#            if publisher is not main:
#                main.books.extend(publisher.books)
#                main.series.extend(publisher.series)
#                db.session.add(main)
#                db.session.delete(publisher)
#        db.session.commit()
#        session['ids'] = []
#        return redirect(url_for('repair.publisher_details', id=main.id))
#        
#    return render_template('repair/publishers_to_merge.html', publishers=publishers)
