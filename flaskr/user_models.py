import enum

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import db, login


class Permission:
    read = 1
    make_reservations = 2
    loan = 4
    add_to_readings = 8
    register_users = 16
    delete_users = 32
    make_loans = 64
    manage_reservations = 128
    create_objects = 256
    edit_objects = 512
    create_restricted_objects = 1024
    edit_restricted_objects = 2048
    make_volunteer = 4096
    make_librarian = 8192
    make_admin = 16384

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'roles', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role {}>'.format(self.name)
    
    @staticmethod
    def insert_roles():
        roles = {
                'Visitor': [Permission.read,],
                'Graduate': [Permission.read, Permission.make_reservations,],
                'Student': [Permission.read, Permission.make_reservations, Permission.loan],
                'Teacher': [Permission.read, Permission.make_reservations, 
                    Permission.loan, Permission.add_to_readings],
                'Volunteer': [Permission.read, Permission.make_reservations, 
                    Permission.loan, Permission.create_objects, Permission.edit_objects],
                'Librarian': [Permission.read, Permission.make_reservations, 
                    Permission.loan, Permission.create_objects, Permission.edit_objects, 
                    Permission.register_user, Permission.delete_user, 
                    Permission.make_loans, Permission.manage_reservations, permission.make_volunteer],
                'Admin': [Permission.read, Permission.make_reservations, 
                    Permission.loan, Permission.create_objects, Permission.create_restricted_objects, 
                    Permission.update_restricted_objects, Permission.edit_objects, 
                    Permission.register_user, Permission.delete_user, 
                    Permission.make_loans, Permission.manage_reservations, 
                    Permission.make_volunteer, Permission.make_librarian, 
                    Permission.make_admin, Permission.add_to_readings],
                }
        default_role = 'Visitor'
        for role in roles:
            r = Role.query.filter_by(name=role).first()
            if r is None:
                r = Role(name=role)
                r.reset_permissions()
                for perm in roles[role]:
                    r.add_permission(perm)
                r.default = (r.name == default_role)
                db.session.add(r)
            db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
#    phone_number # regex
#    division = foreign key (division -> name, school, start_year)
#    role = foreign key

    @property
    def password(self):
        raise AttributeError('Can not read password property')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: 
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')
   
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.admin)


    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_admin(self):
        return Flase

login.anonymous_user = AnonymousUser

@login.user_loader
def load_user(id):
    return User.query.get(id)
