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
    born = db.Column(db.String(64))

    def __str__(self):
        if self.born:
            return f'{self.name}, ur. {self.born}'
        return self.name


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64))
    series = db.relationship('Serie', backref='publisher', lazy='dynamic')
    
    def __str__(self):
        return f'{self.name}, {self.city}'


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    
    def __str__(self):
        return self.name


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __str__(self):
        return self.name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(64))# wymagane
    shelf = db.Column(db.String(3))# regex A4

    def __str__(self):
        return self.room
