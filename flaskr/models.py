import enum 

from flaskr import db
# null true, required false
from flaskr.search import autocomplete, add_to_index, remove_from_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression):
        res = autocomplete(cls.__tablename__, expression)
        return res

    @classmethod
    def before_commit(cls, session):
        session._changes = {
                'add': list(session.new),
                'update': list(session.dirty),
                'delete': list(session.deleted)
        }
    
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        print('reindex')
        for obj in cls.query:
            print(obj)
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)





class Person(SearchableMixin, db.Model):
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    born = db.Column(db.String(64), nullable=True)
    books = db.relationship('Creators', backref='person', lazy=True)

    def __str__(self):
        if self.born:
            return f'{self.name}, ur. {self.born}'
        return self.name


class Publisher(db.Model):
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64))
    series = db.relationship('Serie', backref='publisher', lazy='dynamic')
    
    def __str__(self):
        return f'{self.name}, {self.city}'


class Serie(db.Model):
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    
    def __str__(self):
        return self.name


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    copies = db.relationship('Copy', backref='collection', lazy=True)
    
    def __str__(self):
        return self.name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(64))# wymagane
    shelf = db.Column(db.String(3), nullable=True)# regex A4
    copies = db.relationship('Copy', backref='location')

    def __str__(self):
        return self.room


class FormChoices(enum.Enum):
    PO = 'Poetry'
    PR = 'Prose'
    DR = 'Drama'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ISBN_REGEX=r'^(97(8|9))?\d{9}(\d|X)$'
    isbnIssn = db.Column(db.String(13), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    origin_language = db.Column(db.String(32), nullable=True)
    pub_year = db.Column(db.String(32), nullable=True) #potem zmienić na False
    first_edition = db.Column(db.String(64), nullable=True) #potem zmienić na False
    periodic_num = db.Column(db.String(64), nullable=True)
    fiction = db.Column(db.Boolean(), nullable=True)
    genre = db.Column(db.String(64), nullable=True)
    literary_form = db.Column(db.Enum(FormChoices))
    subject = db.Column(db.String(64), nullable=True)
    precision = db.Column(db.Text, nullable=True)
    nukat = db.Column(db.Text, nullable=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=True) #potem zmienić na False
    creators = db.relationship('Creators', backref='book')

    def __str__(self):
        return self.title


class BookRoles(enum.Enum):
    A = 'Author'
    T = 'Translation'
    R = 'Redaction'
    I = 'Introduction'


class Creators(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    role = db.Column(db.Enum(BookRoles))
#    book = db.relationship('Book', backref='books')
#    creator =  db.relationship('Person', backref='creators')

class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_shelf = db.Column(db.Boolean(), nullable=False)
    section = db.Column(db.String(255), nullable=True)
    remarques = db.Column(db.String(255), nullable=False)
    signature_mark = db.Column(db.String(32), nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)

    
    
