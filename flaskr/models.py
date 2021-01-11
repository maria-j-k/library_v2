import enum 
from sqlalchemy.sql import func

from flaskr import db
from flaskr.search import add_to_index, remove_from_index, es_fuzzy_search
#from flaskr.es_search import fts

class SearchableMixin(object):
#    @classmethod
#    def search(cls, expression):
#        res = autocomplete(cls.__tablename__, expression)
#        return res
#    
#    @classmethod
#    def es_search(cls, expression, fields):
#        res = fts(cls.__tablename__, expression, fields)
#        return res
#
    @classmethod
    def fuzzy_search(cls, field, expression):
        res = es_fuzzy_search(cls.__tablename__, field, expression)
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
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class FlagMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_modified = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    approuved = db.Column(db.Boolean(), default=False)
    incorrect = db.Column(db.Boolean())

    @classmethod
    def get_foreign_keys(cls):
        return [column.name for column in cls.__table__.columns if column.foreign_keys]

    @classmethod
    def printModel(cls, obj):
        columns = [x.__str__().split('.')[1]
                for x in cls.__table__.columns]
        return columns

    @classmethod
    def to_dict(cls, obj):
        return [{x.__str__().split('.')[1]: getattr(obj, x.__str__().split('.')[1])} 
                for x in cls.__table__.columns]
    
    def toggle_incorrect(obj):
        if obj.incorrect:
            obj.incorrect = False
        else:
            obj.incorrect = True
        db.session.add(obj)
        db.session.commit()
        return obj

def get_class_by_tablename(tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in db.Model._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c



class BookRoles(enum.Enum):
    A = 'Author'
    T = 'Translation'
    R = 'Redaction'
    I = 'Introduction'




class Person(SearchableMixin, FlagMixin, db.Model):
    __tablename__='persons'
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    born = db.Column(db.String(64), nullable=True) # wylatuje
    creator = db.relationship('Creator', backref='person', lazy='dynamic')
    
    def __str__(self):
        if self.born:
            return f'{self.name}, ur. {self.born}'
        return self.name

    @property
    def is_incorrect(self):
        return self.incorrect 
    
    def author(self):
        return Creator.query.filter_by(role = 'A', person=self)

    def translator(self):
        return Creator.query.filter_by(role = 'T', person=self)

    def redaction(self):
        return Creator.query.filter_by(role = 'R', person=self)

    def introduction(self):
        return Creator.query.filter_by(role = 'I', person=self)


class Publisher(SearchableMixin, FlagMixin, db.Model):
    __tablename__='publishers'
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    series = db.relationship('Serie', backref='publisher', lazy='dynamic')
    books = db.relationship('Book', backref='publisher', lazy='dynamic') 
    
    def __str__(self):
        return self.name

    def to_dict(self):
        data = {
                'id': self.id,
                'name': self.name,
                'city': self.city,
                'series': [s.id for s in self.series.all()]
                }
        return data
    
    @property
    def is_incorrect(self):
        return self.incorrect or self.serie.incorrect

class City(SearchableMixin, FlagMixin, db.Model):
    __tablename__= 'cities'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    books = db.relationship('Book', backref='city', lazy='dynamic') 

    def __repr__(self):
        return self.name

    @property
    def is_incorrect(self):
        return self.incorrect 

#class PublicationPlace(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    role = db.Column(db.Enum(BookRoles))
#    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
#    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
#    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class Serie(SearchableMixin, FlagMixin, db.Model):
    __tablename__='series'
    __searchable__=['name', 'publisher_id']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    books = db.relationship('Book', backref='serie', lazy='dynamic')
    
    def __str__(self):
        return self.name


    @property
    def is_incorrect(self):
        return self.incorrect 


class Collection(SearchableMixin, FlagMixin, db.Model):
    __tablename__='collections'
    __searchable__=['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    copies = db.relationship('Copy', backref='collection', lazy='dynamic')
    
    def __str__(self):
        return self.name


    @property
    def is_incorrect(self):
        return self.incorrect 


class Location(SearchableMixin, FlagMixin, db.Model):
    __tablename__='locations'
    __searchable__=['room']
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(64))# wymagane
    shelf = db.Column(db.String(3), nullable=True)# regex A4
    copies = db.relationship('Copy', backref='location', lazy='dynamic')

    def __str__(self):
        return self.room


    @property
    def is_incorrect(self):
        return self.incorrect 


class FormChoices(enum.Enum):
#    NA = 'N/A'
    PO = 'Poetry'
    PR = 'Prose'
    DR = 'Drama'


class FictionChoices(enum.Enum):
    F = 'Fiction'
    NF = 'Non-fiction'


class Book(SearchableMixin, FlagMixin, db.Model):
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
    creator = db.relationship('Creator', backref='book', lazy='dynamic')
    copies = db.relationship('Copy', backref='book', lazy='dynamic') 

    def __str__(self):
        return self.title

    def print_authors(self):
        authors = [c.person for c in self.creator
                if c.role._name_ == 'A']
        return authors
#        return ", ".join(authors)

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
    
    def authors(self):
        return Creator.query.filter_by(role = 'A', book=self)

    def translators(self):
        return Creator.query.filter_by(role = 'T', book=self)

    def redaction(self):
        return Creator.query.filter_by(role = 'R', book=self)

    def introduction(self):
        return Creator.query.filter_by(role = 'I', book=self)



    @property
    def is_incorrect(self):
        return any(c.person.incorrect for c in self.creator)\
                or self.city.incorrect or \
                self.publisher.incorrect or self.incorrect


class Creator(FlagMixin, db.Model):
    __tablename__='creators'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(BookRoles))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    @property
    def is_incorrect(self):
        return self.incorrect 


class Copy(FlagMixin, db.Model):
    __tablename__='copies'
    id = db.Column(db.Integer, primary_key=True)
    signature_mark = db.Column(db.String(32), nullable=True)
    on_shelf = db.Column(db.Boolean(), nullable=False)
    section = db.Column(db.String(255), nullable=True)
    remarques = db.Column(db.String(255), nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    @property
    def is_incorrect(self):
        return any((self.incorrect, self.book.is_incorrect, self.location.incorrect, self.collection.incorrect))
