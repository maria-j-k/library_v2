from flask import current_app, redirect, render_template, request, session, url_for
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    hash_password,
#    auth_required,
#    current_user,
#    permissions_accepted,
#    permissions_required,
#    roles_accepted,
)

from flaskr import db
from flaskr.accounts import bp


#from flaskr.security.forms import ReaderRegisterForm
from flaskr.security.script import user_datastore

#@bp.route('/')
##@auth_required()
#def home():
#    return render_template('security/accounts_home.html')
#
#@bp.route('/register', methods=['GET', 'POST'])
#def register():
#    form = ReaderRegisterForm()
#    if request.method == 'POST':
#        if form.validate():
#            user_datastore.create_user(
#                first_name=form.first_name.data,
#                last_name=form.last_name.data,
#                email=form.email.data, 
#                password=hash_password(form.password.data), 
#                roles=[form.role.data]
#        )
#            db.session.commit()
#    return render_template('security/register_user.html', form=form)
