# 1. utworzyć Book z tytułem, twórcami, wydawnictwem, rokiem i miejscem wydania
# 2. dopisać do Book pozostałe pola jeśli są puste. Jeśli nie - wyrzucić do pliku
#     a. row
#     b. book.id 
# 3. utworzyć Copy

"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('catalogue/scripts/book_creator.py').read())
"""

import re
from csv import DictReader
import datetime

from catalogue.models import Book, Person, Creator, Collection, Copy



csvpath = '/home/maria/Downloads/katalogWLH_2VIII2020.csv'
succes_count = 0
wrong_person = []

def set_fiction(row):
    if row in ['F', 'F ', ]:
        return True
    elif row in ['NF', 'NF ?',]:
        return False
    else: 
        return None

# def title_except(s): # nie działa...
#     exceptions = ['von', 'de', 'd\'', 'del', 'gen.', 'ks.', ]
#     word_list = s.split(' ')     
#     final = [word_list[0].capitalize()]
#     for word in word_list[1:]:
#         final.append(word if word in exceptions else word.capitalize())
#     return " ".join(final)


def set_author(row):
    if row.strip() in ['Anonim', 'anonim', 'anonimowy']:
        return "Anonimowy"
    elif row.strip() in [
                'zbiorowe', 'zbiorowy', 'Zbiorowy', 'zbiorowa', 'zbirowy', 
                'wiele', 'Praca zbiorowa', 'praca zbiorowa', 'Praca Zbiorowa'
        ]:
        return "Praca zbiorowa"
    elif row.strip() in ['Antologia', 'antologia']:
        return "Antologia"
    elif row.strip() in ['?', '??', '???', '-------', '—', '']:
        return None
    else:
        return row.strip()

def get_person(row):
    per = re.split(', |/|;', row)
    persons = []
    wrong_person=[]
    for person in per:
        person = set_author(person)
        try:
            persons.append(Person.objects.get(name=person))
        except Person.DoesNotExist:
            if person not in wrong_person:# and person != None:
                wrong_person.append(person)
    with open('wrong_person.txt', 'a+')  as file:
        file.write(f'{row}: \n {wrong_person} \n \n')
    return persons




def set_collection(row):
    if row in ['Jedlickiego', 'jedlickiego',]:
        collection = 'Jedlickiego'
    elif row in ['WLH', 'wlh',]:
        collection = 'WLH'
    elif row in ['J. i Z. Baumana', 'bauman']:
        collection = 'J. i Z. Baumana'
    elif row in ['bibl. IFiS', 'bibl.IFiS', 'Bibl. IFiS', 'Bibl.IFiS']:
        collection = 'Bibl. IFiS'
    elif row in ['Marcel', 'marcel']:
        collection = 'Marcel'
    elif row in ['PS', 'Ps', 'ps']:
        collection = 'PS'
    else:
        collection = row
    return collection

def set_form(row):
    if row in ['proza narracyjna', 'proza narracyjna ', 'prozs narracyjna ',]:
        return 'PR'
    elif row in ['poezja', 'poezja ',]:
        return 'PO'
    elif row == 'dramat':
        return 'DR'
    elif row in ['?', '(?)']:
        return '?'
    else:
        return None


def set_shelf(row):
    if row.lower().strip() == 'x':
        return True
    else:
        return False


def set_location(row):
    if row in ['słownik', 'słowniki']:
        return 'Słowniki'
    else:
        return row.capitalize().strip()






with open(csvpath) as csv_file:
    print(f"start: {datetime.datetime.now()}")
    csv_reader = DictReader(csv_file)
    print('Loading Copy...')


    for i, row in enumerate(csv_reader, 0):
        # if i == 20:
        #     break
        authors = get_person(row['Autor/autorka [Nazwisko Imię]'])
        translations = get_person(row['Tłumacz_ka'])
        redactions = get_person(row['Opracowanie, redakcja [Nazwisko Imię]'])
        introductions = get_person(row['Wstęp, posłowie'])

        collection = Collection.objects.get(name=set_collection(row['Z tajnych archiwów']))
        shelf = set_shelf(row['czy jest na półce?'])

        new_book, created = Book.objects.get_or_create(
            title = row['Tytuł'].strip(),
            pub_year = row['Rok wydania'].strip(),
            pub_place = row['Miejsce wydania'].strip(),
            editor = row['Wydawnictwo'].strip(),
            )
        if created:
            if authors:
                for author in authors:
                    a = Creator(person=author, book=new_book, role='A')
                    a.save()
            if translations:
                for traslation in translations:
                    t = Creator(person=traslation, book=new_book, role='T')
                    t.save()
            if redactions:
                for redaction in redactions:
                    r = Creator(person=redaction, book=new_book, role='R')
                    r.save()
            if introductions:
                for introduction in introductions:
                    i = Creator(person=introduction, book=new_book, role='I')
                    i.save()

        new_copy = Copy.objects.create(on_shelf=shelf,
                                        location=set_location(row['MIEJSCE']),
                                        section=row['Dział'].strip(),
                                        remarques=row['Uwagi do książki'].strip(),
                                        collection = collection,
                                        book = new_book,
             )

        succes_count += 1
    print(f"End copy: {datetime.datetime.now()}")
    print(f'{str(succes_count)} inserted successfully! ')
    print(f"wrong names: {wrong_person}")









with open(csvpath) as csv_file:
    print(f"start: {datetime.datetime.now()}")
    csv_reader = DictReader(csv_file)
    print('Loading Book information...')


    for i, row in enumerate(csv_reader, 0):
        # if i == 20:
        #     break

        new_book = Book.objects.get(
            title = row['Tytuł'].strip(),
            pub_year = row['Rok wydania'].strip(),
            pub_place = row['Miejsce wydania'].strip(),
            editor = row['Wydawnictwo'].strip(),
            )

        new_book.origin_language = new_book.origin_language or row['Język oryginału'].strip()
        new_book.series = new_book.series or row['Nazwa serii'].strip()
        new_book.first_edition = new_book.first_edition or row['rok pierwszego wydania'].strip()
        new_book.periodic_num = new_book.periodic_num or row['Numer czasopisma'].strip()
        new_book.genre = new_book.genre or row['Gatunek '].strip()
        new_book.subject = new_book.subject or row['TEMAT'].strip()
        new_book.precision = new_book.precision or row['Uszczegółowienie'].strip()
        new_book.fiction = new_book.fiction or set_fiction(row['F/NF'])
        new_book.nukat = new_book.nukat or row['tematy NUKAT '].strip()
        new_book.literary_form = new_book.literary_form or set_form(row['Rodzaj'])
        new_book.save()

print(f"End Book information: {datetime.datetime.now()}")
