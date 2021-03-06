from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Collection 
from flaskr.repair import bp
from .forms import CollectionForm, SearchForm

@bp.route('/collections', methods=['GET', 'POST'])
def collections_list():
    session['ids'] = []

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    page = request.args.get('page', 1, type=int)
    
    form = SearchForm()
    
    if request.method == 'GET':
        if name:
            collections, total = Collection.fuzzy_search(name, page, 20)
            if scope == 'incorrect':
                collections = collections.filter_by(incorrect=True)
            next_url = url_for('repair.collections_list', name=name, page=page + 1) \
                if total > page * 20 else None
            prev_url = url_for('repair.collections_list', name=name, page=page - 1) \
                if page > 1 else None
            return render_template('repair/collections_list.html', collections=collections, 
                    form=form, page=page, next_url=next_url, prev_url=prev_url)
            
        elif scope == 'incorrect':
            c = Collection.query.filter_by(incorrect=True).order_by(
                    'name').paginate(page, 20, False)
        elif scope == 'all':
            c = Collection.query.order_by('name').paginate(page, 20, False)
    
    elif request.method == 'POST':
        id_list = request.form.getlist('collection_id')
        if len(id_list) > 4:
            flash("You can't merge more than 4 items at once.")
            return render_template('repair/collections_list.html', 
            collections=c.items, c=c, form=form, scope=scope)
        elif len(id_list) < 2:
            flash("You need at least 2 items to merge.")
            return render_template('repair/collections_list.html', 
            collections=c.items, c=c, form=form, scope=scope)
        session['ids'] = id_list
        return redirect(url_for('repair.collections_merge'))
    return render_template('repair/collections_list.html', 
            collections=c.items, c=c, form=form, scope=scope)

@bp.route('/collections/<int:id>', methods=['GET'])
def collection_details(id):
    session['ids'] = []
    collection = Collection.query.get(id)
    return render_template('repair/collection_details.html', 
            collection=collection)

@bp.route('/collections/<int:id>/edit', methods=['GET', 'POST'])
def collection_edit(id):
    session['ids'] = []
    collection = Collection.query.get(id)
    form = CollectionForm(name=collection.name,
            incorrect=collection.incorrect,
            approuved=collection.approuved)
    if form.validate_on_submit():
        collection_name = form.name.data
        if collection_name != collection.name:
            c = Collection.query.filter_by(name=collection_name).first()
            if c:
                flash(f'''Collection {c.name} exists already in the database. \n
                    You have to merge "{collection.name}" with "{c.name}".\n 
                    Hit "Show similars" to enable merge.''')
                return redirect(url_for('repair.collection_edit',id=collection.id)) 
        collection.name = collection_name
        collection.approuved = form.approuved.data
        collection.incorrect = form.incorrect.data
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('repair.collection_details', id=collection.id))
            
    return render_template('repair/collection_edit.html', 
            form=form, collection=collection)

@bp.route('/collections/merge/', methods=['GET', 'POST'])
def collections_merge():
    id_list = session.get('ids')
    print(id_list)
    collections = Collection.query.filter(Collection.id.in_(id_list)
            ).order_by('name').all()
    if request.method == 'POST':
        to_exclude = request.form.getlist('exclude')
        if to_exclude:
            for item in to_exclude:
                session['ids'].remove(item)
                session.modified = True
                if len(session['ids']) < 2:
                    flash('You need at least 2 items to merge.')
                    return redirect(url_for('repair.collections_list'))
            return redirect(url_for('repair.collections_merge'))
        main = Collection.query.get(request.form.get('collection'))
        for collection in collections:
            if collection is not main:
                main.copies.extend(collection.copies)
                db.session.add(main)
                db.session.delete(collection)
        db.session.commit()
        session['ids'] = []
        return redirect(url_for('repair.collection_details', id=main.id))
        
    return render_template('repair/collections_to_merge.html',
            collections=collections)
