# wczytać wszystkie osoby z pól autor, tłumacz, red, wstęp
# dopisać odpowiednim daty urodzenia

"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run:
                                1) manage.py shell
                                2) exec(open('staff_zone/scripts/person.py').read())
"""

from csv import DictReader

from staff_zone.models import Person


notespath = '/home/maria/Documents/moje/apis/new_wlh/wlh_born.txt'
csvpath = '/home/maria/Downloads/katalogWLH_2VIII2020.csv'
row_count = 0
created_count = 0
got_count = 0
born_count = 0


# Create Person:
with open(csvpath) as csv_file:
    csv_reader = DictReader(csv_file)
    print('Loading ...')
    for row in csv_reader:
        print(row['Autor/autorka [Nazwisko Imię]'])
#        print(row['Tłumacz_ka'])
#        print(row['Opracowanie, redakcja [Nazwisko Imię]'])
#        print(row['Wstęp, posłowie'])
        authors = parse_author(row)
#        print(list(authors))
        creators = parse_person(row)
        print("***")
#        authors = re.split(', |/|;', row['Autor/autorka [Nazwisko Imię]'])
#        translators = re.split(', |/|;', row['Tłumacz_ka'])
#        redactors = re.split(', |/|;', row['Opracowanie, redakcja [Nazwisko Imię]'])
#        introductors = re.split(', |/|;', row['Wstęp, posłowie'])
#        creators = [name.strip() for name in chain(authors, translators, redactors, introductors) if name.strip()]
        for creator in creators:
            person, created = create_person(set_author(creator))
            if created == True:V
                created_count += 1
            else:
                got_count += 1
        for author in authors:
            print(f'line 87: {author}')
            person = create_person(set_author(author))
#            creator = set_author(creator)
#            if creator:
#                obj, created = Person.objects.get_or_create(name=creator)
#                if created == True:
#                    created_count += 1
#                else:
#                    got_count += 1
        row_count += 1
        if row_count >2:
            break
    print(f'{str(row_count)} inserted successfully! ')
    print(f'{str(created_count)} newly created! ')
    print(f'{str(got_count)} got form db! ')

#############

# 8045 inserted successfully! 
# 5271 newly created! 
# 6408 got form db! 


# Add year of birth:
#with open(csvpath) as csv_file:
#    csv_reader = DictReader(csv_file)
#    print('Loading creators...')
#    for row in csv_reader:
#        if row['rok urodzenia autora_ki'] and row['rok urodzenia autora_ki'] not in strange_borns and 'wyd' not in row['rok urodzenia autora_ki']:
#            authors = re.split(', |/|;', row['Autor/autorka [Nazwisko Imię]'])
#            for author in authors:
#                author = set_author(author)
#                if author:
#                    obj = Person.objects.get(name=author)
#                    obj.born = row['rok urodzenia autora_ki']
#                    obj.save()
#                    born_count += 1
#            row_count += 1
#    print(f'{str(row_count)} inserted successfully!')
#    print(f'{str(born_count)} newly created!')
#
# 4656 inserted successfully!
# 4752 newly created!


#########
# get list of possibly wrong born dates
#########
# strange_borns = []

# with open(csvpath) as csv_file:
#     csv_reader = DictReader(csv_file)
#     print('Loading creators...')
#     for row in csv_reader:
#         if row['rok urodzenia autora_ki']:
#             try:
#                 int(row['rok urodzenia autora_ki'])
#             except ValueError:
#                 if row['rok urodzenia autora_ki'] not in strange_borns:
#                     strange_borns.append(row['rok urodzenia autora_ki'])

#     with open(notespath, 'a+') as infofile:
#         infofile.write('\n')
#         infofile.write('Strange borns')
#         infofile.write('\n')
#         for x in sorted(strange_borns):
#             infofile.write(f"'{x}'")
#             infofile.write('\n')
