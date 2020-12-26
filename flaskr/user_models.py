import enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
#    phone_number
#    division = foreign key (division -> name, school, start_year)
#    role = foreign key

    def __repr__(self):
        return '<User{} {}>'.format(self.first_name, self.last_name)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


@login.user_loader
def load_user(id):
    print(id)
    return User.query.get(id)
