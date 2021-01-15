import re
from itertools import chain


def set_location(location):
    if location in ['słownik', 'słowniki']:
        return 'Słowniki'
    else:
        return location.capitalize().strip()

def parse_location(row):
    if row['MIEJSCE'] == "":
        return None
    return set_location(row['MIEJSCE'])


def set_person(person):
    """Cleaning person's data
    Accepts: string stripped of white spaces
    Returns: person's name, unified spelling of 'anonim', 'antology', 'collective' or None if author is not specified."""
    if person in ['Anonim', 'anonim', 'anonimowy']:
        return "Anonimowy"
    elif person in [
                'zbiorowe', 'zbiorowy', 'Zbiorowy', 'zbiorowa', 'zbirowy',
                'wiele', 'Praca zbiorowa', 'praca zbiorowa', 'Praca Zbiorowa'
        ]:
        return "Praca zbiorowa"
    elif person in ['Antologia', 'antologia']:
        return "Antologia"
    elif person in ['?', '??', '???', '-------', '—', '']:
        return None
    else:
        return person

def parse_person(row):
    authors = [set_person(name.strip())
            for name in re.split(', |/|;', row['Autor/autorka [Nazwisko Imię]'])
            if set_person(name.strip())]
    translation = [set_person(name.strip())
            for name in re.split(', |/|;', row['Tłumacz_ka'])
            if set_person(name.strip())]
    redaction = [set_person(name.strip())
            for name in  re.split(', |/|;', row['Opracowanie, redakcja [Nazwisko Imię]'])
            if set_person(name.strip())]
    intro = [set_person(name.strip())
            for name in re.split(', |/|;', row['Wstęp, posłowie'])
            if set_person(name.strip())]
    return chain(authors, translation, redaction, intro)


def parse_author(row):
    authors = [set_person(name.strip())
            for name in re.split(', |/|;',row['Autor_ka'])
            if set_person(name.strip())]
    return authors

def parse_translator(row):
    creators = [set_person(name.strip())
            for name in re.split(', |/|;', row['Tłumacz_ka'])
            if set_person(name.strip())]
    return creators

def parse_redaction(row):
    creators = [set_person(name.strip())
            for name in  re.split(', |/|;', row['Opracowanie, redakcja'])
            if set_person(name.strip())]
    return creators

def parse_intro(row):
    """Splits the row on different separators, strips trailing spaces, eliminates empty strings.
    Accepts: row form csv.reader iterator
    Returns list of creators"""
    creators = [set_person(name.strip())
            for name in re.split(', |/|;', row['Wstęp, posłowie'])
            if set_person(name.strip())]
    return creators


def set_collection(coll):
    """
    Accepts: value of collection key of a row in csv.dictreader
    Returns: string normalised to unified spelling of collection name
    """
    if coll in ['Jedlickiego', 'jedlickiego',]:
        collection = 'Jedlickiego'
    elif coll in ['WLH', 'wlh',]:
        collection = 'WLH'
    elif coll in ['J. i Z. Baumana', 'bauman']:
        collection = 'J. i Z. Baumana'
    elif coll in ['bibl. IFiS', 'bibl.IFiS', 'Bibl. IFiS', 'Bibl.IFiS']:
        collection = 'Bibl. IFiS'
    elif coll in ['Marcel', 'marcel']:
        collection = 'Marcel'
    elif coll in ['PS', 'Ps', 'ps']:
        collection = 'PS'
    else:
        collection = coll
    return collection

def parse_collection(row):
    """
    Accepts row of csv.reader iterator
    Returns: string representing collection name
    """
    if row['Z tajnych archiwów'] == "":
        return None
    coll = set_collection(row['Z tajnych archiwów'])
    return coll

def parse_publisher(row):
    """
    Accepts row of csv.reader iterator
    Returns: dictionnary containing publisher's name and location and serie if exists in the file.
    """
    if row['Wydawnictwo'] == "":
        return None
    name = row['Wydawnictwo'].strip()
    return name

def parse_city(row):
    if row['Miejsce wydania'] == "":
        return None
    name = row['Miejsce wydania'].strip().title()
    return name


def parse_serie(row):
    if row['Nazwa serii'] == "":
        return None
    serie = row['Nazwa serii'].strip()
    return serie

def set_form(row):
    if row in ['proza narracyjna', 'proza narracyjna ', 'prozs narracyjna ',]:
        return 'PR'
    elif row in ['poezja', 'poezja ',]:
        return 'PO'
    elif row == 'dramat':
        return 'DR'
    else:
        return None

def set_fiction(row):
    if row in ['F', 'F ', ]:
        return True
    elif row in ['NF', 'NF ?',]:
        return False
    else: 
        return None

def parse_book(row):
    book_data = {
            'title': row['Tytuł'].strip(),
            'pub_year': row['Rok wydania'].strip(),
            'origin_language': row['Język oryginału'].strip(),
            'first_edition': row['rok pierwszego wydania'].strip(),
            'fiction': set_fiction(row['F/NF']),
#            'genre': row['Gatunek '].strip(),
            'literary_form': set_form(row['Rodzaj']),
#            'subject': row['TEMAT'].strip(),
            'precision': row['Uszczegółowienie'].strip(),
            'nukat': row['tematy NUKAT '].strip(),
            }
    return book_data

def set_shelf(row):
    if row.lower().strip() == 'x':
        return True
    else:
        return False

def parse_copy(row):
    copy_data = {
            'on_shelf': set_shelf(row['czy jest na półce?']),
            'section': row['Dział'].strip(),
            'remarques': row['Uwagi do książki'].strip(),
            }
    return copy_data

