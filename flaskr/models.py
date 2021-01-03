import enum 

from flaskr import db
# null true, required false
from flaskr.search import autocomplete, add_to_index, remove_from_index
from flaskr.es_search import fts

class SearchableMixin(object):
    @classmethod
    def search(cls, expression):
        res = autocomplete(cls.__tablename__, expression)
        return res
    
    @classmethod
    def es_search(cls, expression, fields):
        res = fts(cls.__tablename__, expression, fields)
        return res

#    @classmethod
#    def search_title(cls, expression):
#        res = autocomplete_t(cls.__tablename__, expression)
#        return res
#    
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


#TODO
#on delete - cascade czy protect
#skrypty


class BookRoles(enum.Enum):
    A = 'Author'
    T = 'Translation'
    R = 'Redaction'
    I = 'Introduction'




class Person(SearchableMixin, db.Model):
    __tablename__='persons'
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    born = db.Column(db.String(64), nullable=True) # wylatuje
    creator = db.relationship('Creator', backref='person', lazy=True)
    
    def __str__(self):
        if self.born:
            return f'{self.name}, ur. {self.born}'
        return self.name


class Publisher(SearchableMixin, db.Model):
    __tablename__='publishers'
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    series = db.relationship('Serie', backref='publisher', lazy='dynamic')
    books = db.relationship('Book', backref='publisher', lazy='dynamic') 
    
    def __str__(self):
        return f'{self.name}, {self.city}'

    def to_dict(self):
        data = {
                'id': self.id,
                'name': self.name,
                'city': self.city,
                'series': [s.id for s in self.series.all()]
                }
        return data


class City(db.Model):
    __tablename__= 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    books = db.relationship('Book', backref='city', lazy='dynamic') 

    def __repr__(self):
        return self.name

#class PublicationPlace(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    role = db.Column(db.Enum(BookRoles))
#    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
#    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
#    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class Serie(SearchableMixin, db.Model):
    __tablename__='series'
    __searchable__=['name', 'publisher_id']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    books = db.relationship('Book', backref='serie', lazy='dynamic')
    
    def __str__(self):
        return self.name


class Collection(db.Model):
    __tablename__='collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    copies = db.relationship('Copy', backref='collection', lazy=True)
    
    def __str__(self):
        return self.name


class Location(db.Model):
    __tablename__='locations'
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(64))# wymagane
    shelf = db.Column(db.String(3), nullable=True)# regex A4
    copies = db.relationship('Copy', backref='location')

    def __str__(self):
        return self.room


class FormChoices(enum.Enum):
#    NA = 'N/A'
    PO = 'Poetry'
    PR = 'Prose'
    DR = 'Drama'


class FictionChoices(enum.Enum):
    F = 'Fiction'
    NF = 'Non-fiction'


class Book(SearchableMixin, db.Model):
    __tablename__='books'
    __searchable__=['title']
    id = db.Column(db.Integer, primary_key=True)
    ISBN_REGEX=r'^(97(8|9))?\d{9}(\d|X)$'
    isbn = db.Column(db.String(13), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    origin_language = db.Column(db.String(32), nullable=True)
    pub_year = db.Column(db.String(32), nullable=True) #potem zmienić na False
#    pub_place = db.Column(db.String(64)) # do osobnego modelu m2m
    first_edition = db.Column(db.String(64), nullable=True) #potem zmienić na False
    genre = db.Column(db.String(64), nullable=True)
    literary_form = db.Column(db.Enum(FormChoices), nullable=True)

    #fiction = db.Column(db.Enum(FictionChoices), nullable=True)
    fiction = db.Column(db.Boolean(), nullable=True)
#    subject = db.Column(db.String(64), nullable=True)
    precision = db.Column(db.Text, nullable=True)
    nukat = db.Column(db.Text, nullable=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True) #potem zmienić na False
    serie_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=True)
    creator = db.relationship('Creator', backref='book', lazy=True)
    copies = db.relationship('Copy', backref='book', lazy='dynamic') 

    def __str__(self):
        return self.title

    def print_authors(self):
        authors = [c.person.name for c in self.creator
                if c.role._name_ == 'A']
        return ", ".join(authors)

    def print_trans(self):
        trans = [c.person.name for c in self.creator
                if c.role._name_ == 'T']
        return ", ".join(trans)

    def print_red(self):
        red = [c.person.name for c in self.creator
                if c.role._name_ == 'R']
        return ", ".join(red)

    def print_intro(self):
        intro = [c.person.name for c in self.creator
                if c.role._name_ == 'I']
        return ", ".join(intro)


class Creator(db.Model):
    __tablename__='creators'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(BookRoles))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Copy(db.Model):
    __tablename__='copies'
    id = db.Column(db.Integer, primary_key=True)
    signature_mark = db.Column(db.String(32), nullable=True)
    on_shelf = db.Column(db.Boolean(), nullable=False)
    section = db.Column(db.String(255), nullable=True)
    remarques = db.Column(db.String(255), nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


