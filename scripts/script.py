from csv import DictReader
from datetime import datetime
from time import perf_counter

from flaskr import db
from . import utils
from .utils import counter
from . import parsers

books_path = '/home/maria/Downloads/Katalog_biblioteczny_ksiazki_WLH.csv'
periodics_path = '/home/maria/Downloads/Katalog_biblioteczny_czasopisma_WLH.csv'
filepath = '/home/maria/Documents/portfolio/flask_library/scripts/bulk_insert_test.txt'
#csvpath = '/home/maria/Downloads/katalogWLH_2VIII2020.csv'
row_count = 0
periodic_count = 0
datetime_now = datetime.now()
now = datetime_now.strftime('%A, %d/%m/%Y, %H:%M:%S')


time_start = perf_counter()



with open(books_path) as csv_file:
    csv_reader = DictReader(csv_file)
    print('Loading ...')
    for row in csv_reader:
        utils.row_counter()
        authors = parsers.parse_author(row)
        translators = parsers.parse_translator(row)
        redaction = parsers.parse_redaction(row)
        intro = parsers.parse_intro(row)
        collection = parsers.parse_collection(row)
        publisher = parsers.parse_publisher(row)
        city = parsers.parse_city(row)
        serie = parsers.parse_serie(row) or None
        book_data = parsers.parse_book(row)
        room = parsers.parse_room(row)
        shelf = parsers.parse_shelf(row)
        copy_data = parsers.parse_copy(row)

        publisher, _ = utils.create_pub(publisher)
        pub_place, _ = utils.create_city(city)
        serie, _ = utils.create_serie(serie, publisher)
        room, _ = utils.create_room(room)
        shelf, _ = utils.create_shelf(room, shelf)
        authors_list = []
        if authors:
            for author in authors:
                person, _ = utils.create_person(person=author)
                authors_list.append(person)
        if len(authors_list) == 0:
            person, _ = utils.create_person(person='Brak')
            authors_list.append(person)
        book, created = utils.create_book(publisher=publisher,
                serie=serie, pub_place=pub_place, 
                person_list=authors_list, **book_data)
        if translators:
            for person in translators:
                obj, _ = utils.create_creator(person=person, role='T', book=book)
        if redaction:
            for person in redaction:
                obj, _ = utils.create_creator(person=person, role='R', book=book)
        if intro:
            for person in intro:
                obj, _ = utils.create_creator(person=person, role='I', book=book)
        book = utils.complete_book(book=book, **book_data)
        if collection:
            coll_obj, created = utils.create_collection(coll=collection)
        else:
            coll_obj = None
        copy = utils.create_copy(book=book,  shelf=shelf, collection=coll_obj, **copy_data)
        db.session.add(copy)
        db.session.commit()
#        row_count += 1
#        if row_count == 20:
#            break

    time_stop = perf_counter()

    print("Elapsed time:", time_stop, time_start)
    print("Elapsed time during the whole program in minutes:",
                                            (time_stop-time_start)/60)

    print(f'skipped: {periodic_count}')

    with open(filepath, 'a') as log_file:
        log_file.write(now)
        log_file.write('\n')
        for key, val in counter.items():
            log_file.write(f'{key}{val}')
            log_file.write('\n')
        log_file.write('End of transcript')
        log_file.write('\n')
        log_file.write('\n')

    for key, val in counter.items():
        print(key, val)
