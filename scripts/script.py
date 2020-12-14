"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run:
                                1) manage.py shell
                                2) exec(open('staff_zone/scripts/script.py').read())
"""
from csv import DictReader
from datetime import datetime
from time import perf_counter

from accounts.models import User
from staff_zone.scripts.utils import (complete_book, create_book,
        create_collection, create_copy, create_creator, create_location,
        create_person, create_pub_serie, counter, row_counter)
from staff_zone.scripts import parsers
from library.local_settings import BULK_PSWD 


filepath = '/home/maria/Documents/portfolio/library/library/staff_zone/scripts/bulk_insert_log.txt'
csvpath = '/home/maria/Downloads/katalogWLH_2VIII2020.csv'
row_count = 0
born_count = 0
datetime_now = datetime.now()
now = datetime_now.strftime('%A, %d/%m/%Y, %H:%M:%S')


time_start = perf_counter()

try:
    user = User.objects.get(username='bulk')
except User.DoesNotExist:
    User.objects.create_user(username='bulk', password=BULK_PSWD)
    user = User.objects.get(username='bulk')
with open(csvpath) as csv_file:
    csv_reader = DictReader(csv_file)
    print('Loading ...')
    for row in csv_reader:
        row_counter()
        authors = parsers.parse_author(row)
        translators = parsers.parse_translator(row)
        redaction = parsers.parse_redaction(row)
        intro = parsers.parse_intro(row)
        collection = parsers.parse_collection(row)
        publisher_data = parsers.parse_publisher(row)
        book_data = parsers.parse_book(row)
        location = parsers.parse_location(row)
        copy_data = parsers.parse_copy(row)

        publisher, created = create_pub_serie(user=user, **publisher_data)
        book, created = create_book(user=user, publisher=publisher, **book_data)
        if authors:
            for author in authors:
                create_creator(person=author, role='A', book=book, user=user)
        if translators:
            for person in translators:
                create_creator(person=person, role='T', book=book, user=user)
        if redaction:
            for person in redaction:
                create_creator(person=person, role='R', book=book, user=user)
        if intro:
            for person in intro:
                create_creator(person=person, role='I', book=book, user=user)
        book = complete_book(book=book, user=user, **book_data)
        if collection:
            coll_obj, created = create_collection(coll=collection, user=user)
        if location:
            loc_obj, created = create_location(location=location, user=user)
        copy = create_copy(book=book, location=loc_obj, collection=coll_obj,
                user=user, **copy_data)
        row_count += 1
        if row_count == 1:
            break

time_stop = perf_counter()

print("Elapsed time:", time_stop, time_start)
print("Elapsed time during the whole program in seconds:",
                                        time_stop-time_start)



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
