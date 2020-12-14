"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run:
                                1) manage.py shell
                                2) exec(open('catalogue/scripts/collection.py').read())
"""

from csv import DictReader

from catalogue.models import Collection

csvpath = '/home/maria/Downloads/katalogWLH_2VIII2020.csv'
notespath = '/home/maria/Documents/moje/apis/new_wlh/wlh_collection_from_db.txt'


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


with open(csvpath) as csv_file:
    csv_reader = DictReader(csv_file)
    print('Loading collection...')
    created_count = 0
    got_count = 0
    succes_count = 0
    for row in csv_reader:
        collection = set_collection(row['Z tajnych archiwów'])
        # if csvcoll in ['Jedlickiego', 'jedlickiego',]:
        #     collection = 'Jedlickiego'
        # elif csvcoll in ['WLH', 'wlh',]:
        #     collection = 'WLH'
        # elif csvcoll in ['J. i Z. Baumana', 'bauman']:
        #     collection = 'J. i Z. Baumana'
        # elif csvcoll in ['bibl. IFiS', 'bibl.IFiS', 'Bibl. IFiS', 'Bibl.IFiS']:
        #     collection = 'Bibl. IFiS'
        # elif csvcoll in ['Marcel', 'marcel']:
        #     collection = 'Marcel'
        # elif csvcoll in ['PS', 'Ps', 'ps']:
        #     collection = 'PS'
        # else:
        #     collection = csvcoll

        obj, created = Collection.objects.get_or_create(name=collection)

        if created == True:
            created_count += 1
        else:
            got_count += 1
        succes_count += 1
    print(f'{str(succes_count)} inserted successfully! ')
    print(f'{str(created_count)} newly created! ')
    print(f'{str(got_count)} got form db! ')
    print("Done!")

#################
# 8045 inserted successfully! 
# 21 newly created! 
# 8024 got form db! 
# Done!
#################



# collections = Collection.objects.all()
# collection_list = []
# for coll in collections:
#     if coll not in collection_list:
#         collection_list.append(coll.name)


# with open(notespath, 'a+') as infofile:
#     infofile.write('\n')
#     infofile.write('Collection list:')
#     infofile.write('\n')
#     for x in sorted(collection_list):
#         infofile.write(f"'{x}'" )
#         infofile.write('\n')
