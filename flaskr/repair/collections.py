from flask import flash, redirect, render_template, request, session, url_for, current_app
from flask_login import login_required

from flaskr import db
from flaskr.models import Collection 
from flaskr.repair import bp
from .forms import CollectionForm, SearchForm

@bp.route('/collections', methods=['GET', 'POST'])
def collections_list():
    if request.method == 'POST':
        id_list = request.form.getlist('collection_id')
        session['ids'] = id_list
        return redirect(url_for('repair.collections_merge'))

    scope = request.args.get('filter', 'all', type=str)
    name = request.args.get('name', None)
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if name:
        collections = Collection.fuzzy_search('name', name)
        c = Collection.query.filter(Collection.id.in_(
            [item['id'] for item in collections])
            ).order_by('name').paginate(page, 20, False)
        
    elif scope == 'incorrect':
        c = Collection.query.filter_by(incorrect=True).order_by(
                'name').paginate(page, 20, False)
    elif scope == 'all':
        c = Collection.query.order_by('name').paginate(page, 20, False)
    return render_template('repair/collections_list.html', 
            collections=c.items, c=c,
            form=form, scope=scope)

@bp.route('/collections/<int:id>', methods=['GET'])
def collection_details(id):
    collection = Collection.query.get(id)
    return render_template('repair/collection_details.html', 
            collection=collection)

@bp.route('/collections/<int:id>/edit', methods=['GET', 'POST'])
def collection_edit(id):
    collection = Collection.query.get(id)
    form = CollectionForm(name=collection.name)
    if form.validate_on_submit():
        collection_name = form.name.data
        c = Collection.query.filter_by(name=collection_name).first()
        if c:
            flash(f'''Collection {c.name} exists already in the database. \n
                    You have to merge "{collection.name}" with "{c.name}".\n 
                    Hit "Show similars" to enable merge.''')
        else:
            collection.name = collection_name
            db.session.add(collection)
            db.session.commit()
            return redirect(url_for('repair.collection_details', id=collection.id))
            
    return render_template('repair/collection_edit.html', 
            form=form, collection=collection)

@bp.route('/collections/merge/', methods=['GET', 'POST'])
def collections_merge():
    id_list = session.get('ids')
    collections = Collection.query.filter(Collection.id.in_(id_list)
            ).order_by('name').all()
    if request.method == 'POST':
        to_exclude = request.form.get('exclude')
        if to_exclude:
            id_list.remove(to_exclude)
            collections = Collection.query.filter(Collection.id.in_(id_list)
                    ).order_by('name').all()
            return redirect(url_for('repair.collections_merge',
                collections=collections))
        main = Collection.query.get(request.form.get('collection'))
        for collection in collections:
            if collection is not main:
                main.copies.extend(collection.copies)
                db.session.add(main)
                db.session.delete(collection)
        db.session.commit()
        return redirect(url_for('repair.collection_details', id=main.id))
        
    return render_template('repair/collections_to_merge.html',
            collections=collections)
