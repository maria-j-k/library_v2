import difflib
import re
from itertools import chain

def single_similar(a, b):
    '''
    Returns if the two strings has the similarity ratio of at least 0.8.
    Accepts: two strings.
    Returns: boolean
    '''
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.8

def similar_to_list(term, lst):
    '''
    Returns if the string matches at least one string of a list.
    Accepts: string and list of strings.
    Returns: boolean
    '''
    return any(difflib.get_close_matches(term, lst))

def valid_chars(char):
    allowed_chars = [' ', '\'', '-']
    return char.isalpha() or char in allowed_chars

def strip_invalid(term):
    if term.count('-'):
        if len(term) == term.count('-'):
            return ''
        elif term.count('-') == 1:
            return ''.join(filter(valid_chars, term)).strip()
        else:
            term = [char for char in term]
            ind = term.index('-')
            while ind+1 < len(term):
                if not term[ind+1].isalpha():
                    del term[ind+1]
                elif term[ind+1].isalpha():
                    try:
                        ind = term.index('-', ind+1)
                    except ValueError:
                        break
    return ''.join(filter(valid_chars, term)).strip()

def set_person(person):
    """Cleaning person's data
    Accepts: string stripped of white spaces
    Returns: person's name, unified spelling of 'anonim', 'antology', 'collective' or None if author is not specified."""
    anonym = 'anonim'
    antology = 'Antologia'
    collective = ['Zbiorowy', 'wiele', 'Praca zbiorowa']
    if single_similar(person, anonym):
        return 'Anonimowy'
    elif single_similar(person, antology):
        return 'Antologia'
    elif similar_to_list(person, collective):
        return 'Praca zbiorowa'
    person = strip_invalid(person)
    return person if person else 'Brak'

def parse_person(row):
    auth =  row['Autor_ka']
    trans =  row['Tłumacz_ka']
    red =  row['Opracowanie, redakcja [Nazwisko Imię]']
    intro =  row['Wstęp, posłowie']
    authors = [set_person(name.strip())
            for name in re.split(', |/|;', auth) if set_person(name.strip())]
    translation = [set_person(name.strip()) 
            for name in re.split(', |/|;', trans) if set_person(name.strip())]
    redaction = [set_person(name.strip())
            for name in  re.split(', |/|;', red) if set_person(name.strip())]
    intro = [set_person(name.strip())
            for name in re.split(', |/|;', intro) if set_person(name.strip())]
    return chain(authors, translation, redaction, intro)


def parse_author(row):
    creators = row['Autor_ka']
    return [set_person(name.strip()) for name in re.split(', |/|;', creators) 
            if set_person(name.strip())]
    
def parse_translator(row):
    creators =  row['Tłumacz_ka']
    return [set_person(name.strip()) for name in re.split(', |/|;', creators)
            if set_person(name.strip())]


def parse_redaction(row):
    creators =  row['Opracowanie, redakcja']
    return [set_person(name.strip()) for name in re.split(', |/|;', creators)
            if set_person(name.strip())]

def parse_intro(row):
    creators =  row['Wstęp, posłowie']
    return [set_person(name.strip()) for name in re.split(', |/|;', creators)
            if set_person(name.strip())]


def parse_room(row):
    term = row['MIEJSCE'] 
    return term.capitalize().strip() if term else 'Brak'

def parse_shelf(row):
    term = row['DZIAŁ'] 
    return term.capitalize().strip() if term else 'Brak'

def set_collection(coll):
    jedlickiego = 'J. Jedlickiego'
    if single_similar(coll.strip(), jedlickiego):
        collection = jedlickiego
    elif coll.strip().lower() == 'wlh':
        collection = coll.strip().capitalize()
    elif coll.strip().lower() == 'ps':
        collection =  coll.strip().capitalize()
    else:
        collection = strip_invalid(coll)
    return collection if collection else 'Brak'

def parse_collection(row):
    """
    Accepts row of csv.reader iterator
    Returns: string representing collection name
    """
    term =  row['Z tajnych archiwów']
    return set_collection(term) 
    

def parse_publisher(row):
    """
    Accepts row of csv.reader iterator
    Returns: publisher's.
    """
    term =row['Wydawnictwo']
    return term.strip() if term else 'Brak'


def parse_city(row):
    term = row['Miejsce wydania']
    return term.strip().title() if term else 'Brak'

def parse_serie(row):
    term = row['Nazwa serii']
    return term.strip() if term else 'Brak'

def set_form(term):
    prose = 'proza narracyjna'
    poetry = 'poezja'
    drama = 'dramat'
    if single_similar(prose, term):
        return 'PR'
    elif single_similar(poetry, term):
        return 'PO'
    elif single_similar(drama, term):
        return 'DR'
    else:
        return None

def set_fiction(term):
    if single_similar(term.lower(), 'f'):
        return True
    elif single_similar(term.lower(), 'nf'):
        return False
    else: 
        return None
    
def parse_book(row):
    title = row['Tytuł'].strip() or 'Brak'
    pub_year = row['Rok wydania'].strip()
    origin_language = row['Język oryginału'].strip()
    first_edition = row['rok pierwszego wydania'].strip()
    literary_form = row['Rodzaj'].strip()
    fict = row['F/NF'].strip()
    precision = row['Uszczegółowienie'].strip()
    nukat = row['tematy NUKAT '].strip()

    book_data = {
            'title': title,
            'pub_year': pub_year,
            'origin_language': origin_language,
            'first_edition': first_edition,
            'literary_form': set_form(literary_form),
            'fiction': set_fiction(fict),
            'precision': precision,
            'nukat': nukat,
            }
    return book_data


def parse_copy(row):
    section = row['DZIAŁ'].strip(),
    ordering = row['układ'].strip(),
    remarques = row['Uwagi do książki'].strip(),
    copy_data = {
            'on_shelf': False,
            'section': section,
            'ordering': ordering,
            'remarques': remarques,
            }
    return copy_data

