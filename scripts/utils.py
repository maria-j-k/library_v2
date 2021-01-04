from flaskr import db
from flaskr.models import (Book, City, Collection, Copy, Creator, Location,
        Person, Publisher, Serie)
from .parsers import parse_collection


def items_counter(action, dictionary):
    cnt = 0
    def inner():
        nonlocal cnt
        cnt += 1
        dictionary[action] = cnt
        return dictionary
    return inner

counter = {}
serie_created = items_counter('Series created: ', counter)
serie_got = items_counter('Series got from database: ', counter)
coll_created = items_counter('Collections created: ', counter)
coll_got = items_counter('Collections got from database: ', counter)
person_created = items_counter('Persons created: ', counter)
person_got = items_counter('Persons got from database: ', counter)
publisher_created = items_counter('Publishers created: ', counter)
publisher_got = items_counter('Publishers got from database: ', counter)
book_created = items_counter('Books created: ', counter)
book_got = items_counter('Books got from database: ', counter)
role_created = items_counter('Roles created: ', counter)
role_got = items_counter('Roles got from database: ', counter)
loc_created = items_counter('Locations created: ', counter)
loc_got = items_counter('Locations got from database: ', counter)
copy_created = items_counter('Copies created: ', counter)
city_created = items_counter('Cities created: ', counter)
city_got = items_counter('Cities got: ', counter)

row_counter = items_counter('Rows in total: ', counter)


def get_or_create(session, Model, defaults=None, **kwargs):
    instance = session.query(Model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        kwargs.update(defaults or {})
        instance = Model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance, True


def create_serie(name, publisher):
    obj, created = get_or_create(db.session, Serie, name=name, publisher_id=publisher.id)
    serie_created() if created else serie_got()
    return obj, created

def create_person(person):
    obj, created = get_or_create(db.session, Person, name=person)
#    db.session.add(obj)
    person_created() if created else person_got()
    return obj, created

def create_pub(publisher_name):
    pub_obj, created = get_or_create(db.session, Publisher, name=publisher_name)
    publisher_created() if created else publisher_got()
    return pub_obj, created

def create_city(city):
    obj, created = get_or_create(db.session, City, name=city)
    city_created() if created else city_got()
    return obj, created

def create_book(publisher, pub_place, **book_data):
    title = book_data.get('title')
    pub_year = book_data.get('pub_year')
    obj, created = get_or_create(db.session, Book, title=title, pub_year=pub_year, city_id=pub_place.id, publisher_id=publisher.id)
    book_created() if created else book_got()
    return obj, created

def create_creator(person, role, book):
    person_obj, _ = create_person(person)
    creator_obj, created = get_or_create(db.session, Creator, person=person_obj, role=role, book=book)
    role_created() if created else role_got()
    return creator_obj, created

def complete_book(book, **book_data):
    book.origin_language = book.origin_language or book_data['origin_language']
    book.first_edition = book.first_edition or book_data['first_edition']
    book.ficition = book.fiction or book_data['fiction']
    book.genre = book.genre or book_data['genre']
    book.literary_form = book.literary_form or book_data['literary_form']
#    book.subject = book.subject or book_data['subject']
    book.precision = book.precision or book_data['precision']
    book.nukat = book.nukat or book_data['nukat']
    return book

def create_collection(coll):
    obj, created = get_or_create(db.session, Collection, name=coll)
    coll_created() if created else coll_got()
    return obj, created

def create_location(location):
    obj, created = get_or_create(db.session, Location, room=location)
    loc_created() if created else loc_got()
    return obj, created

def create_copy(book, location, collection, **copy_data):
    obj = Copy(book_id=book.id, location_id=location.id, collection_id=collection.id, **copy_data)
#    db.session.add(obj)
#    db.session.commit()
    copy_created()
    return obj









































