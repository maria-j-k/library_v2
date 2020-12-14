
from staff_zone.models import (Book, Change, Collection, Copy, Creator, Location,
        Person, Publisher, Serie)
from staff_zone.scripts.parsers import parse_collection

strange_borns = ['AZ nazwisko', 'AZ tytuł', 'XVI-XVIII opracowanie tzn. górna półka', 'szukać przy Kapuścińskim', '1957 ale szukaj pod Kapuścińskim',  's', '1910 ale szukaj pod newtonem (1643)', 'szukaj po dacie wydania', 'rok wydania 1991', 'seria', 'szukaj pod super dawno', 'Szukaj pod Lemem Czyli 1921',  'wtdanie 2009', 'seria konfrontacje historyczne', 'por data wydania 1978', 'antologia', '?']


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
coll_created = items_counter('Collections created: ', counter)
person_created = items_counter('Persons created: ', counter)
publisher_created = items_counter('Publishers created: ', counter)
book_created = items_counter('Books created: ', counter)
role_created = items_counter('Roles created: ', counter)
loc_created = items_counter('Locations created: ', counter)
copy_created = items_counter('Copies created: ', counter)

serie_got = items_counter('Series got from database: ', counter)
coll_got = items_counter('Collections got from database: ', counter)
person_got = items_counter('Persons got from database: ', counter)
publisher_got = items_counter('Publishers got from database: ', counter)
book_got = items_counter('Books got from database: ', counter)
role_got = items_counter('Roles got from database: ', counter)
loc_got = items_counter('Locations got from database: ', counter)

row_counter = items_counter('Rows in total: ', counter)

def create_serie(name, publisher, user):
    obj, created = Serie.objects.get_or_create(name=name, publisher=publisher)
    if created:
        serie_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        serie_got()
    return obj, created

def create_person(person, user):
    obj, created = Person.objects.get_or_create(name=person)
    if created:
        person_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        person_got()
    return obj, created

def create_pub_serie(user, **publisher_data):
    name = publisher_data['name']
    city = publisher_data['city']
    obj, created = Publisher.objects.get_or_create(name=name, city=city)
    if created:
        publisher_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        publisher_got()
    serie = publisher_data.get('serie')
    if serie:
        create_serie(name=serie, user=user, publisher=obj)
    return obj, created

def create_book(publisher, user, **book_data):
    title = book_data.get('title')
    pub_year = book_data.get('pub_year')
    obj, created = Book.objects.get_or_create(title=title, pub_year=pub_year, publisher=publisher)
    if created:
        book_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        book_got()
    return obj, created

def create_creator(person, role, book, user):
    person, _ = create_person(person=person, user=user)
    obj, created = Creator.objects.get_or_create(person=person, role=role, book=book)
    if created:
        role_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        role_got()
    return obj, created

def complete_book(book, user, **book_data):
    book.origin_language = book.origin_language or book_data['origin_language']
    book.first_edition = book.first_edition or book_data['first_edition']
    book.periodic_num = book.periodic_num or book_data['periodic_num']
    book.ficition = book.fiction or book_data['fiction']
    book.genre = book.genre or book_data['genre']
    book.literary_form = book.literary_form or book_data['literary_form']
    book.subject = book.subject or book_data['subject']
    book.precision = book.precision or book_data['precision']
    book.nukat = book.nukat or book_data['nukat']
    book.save()
    Change.objects.create(user=user, content_object=book, action='M')
    return book


def create_collection(coll, user):
    obj, created = Collection.objects.get_or_create(name=coll)
    if created:
        coll_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        coll_got()
    return obj, created

def create_location(location, user):
    obj, created = Location.objects.get_or_create(room=location)
    if created:
        loc_created()
        Change.objects.create(user=user, content_object=obj, action='C')
    else:
        loc_got()
    return obj, created

def create_copy(book, location, collection, user, **copy_data):
    obj = Copy.objects.create(book=book, location=location, collection=collection, **copy_data)
    copy_created()
    Change.objects.create(user=user, content_object=obj, action='C')
    return obj
