from csv import DictReader
from datetime import datetime
from time import perf_counter

from flaskr import db
from scripts import utils
from scripts.utils import counter
from scripts import parsers

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
        location = parsers.parse_location(row)
        copy_data = parsers.parse_copy(row)

        publisher, created = utils.create_pub(publisher)
        pub_place, created = utils.create_city(city)
        book, created = utils.create_book(publisher=publisher, pub_place=pub_place, **book_data)
        if serie: 
            serie_obj, created = utils.create_serie(name=serie, publisher=publisher)
            serie_obj.books.append(book)
            serie = serie_obj
        if authors:
            for author in authors:
                obj, _ = utils.create_creator(person=author, role='A', book=book)
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
        if location:
            loc_obj, created = utils.create_location(location=location)
        copy = utils.create_copy(book=book, location=loc_obj, collection=coll_obj, **copy_data)
        db.session.add(copy)
        db.session.commit()
        row_count += 1
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
        log_file.write('\n*3')

    for key, val in counter.items():
        print(key, val)