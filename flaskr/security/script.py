from flask import current_app, render_template, url_for, request
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
from flask_security.models import fsqla_v2 as fsqla

from flaskr import db
from flaskr.security import bp

#from flaskr.security.forms import ReaderRegisterForm
#from new_forms import RegisterForm


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'), nullable=True)


class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    school = db.Column(db.String(32), nullable=True)
    level = db.Column(db.Integer, nullable=False)
    students = db.relationship('User', backref='division', lazy='dynamic')


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
















