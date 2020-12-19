from flask import current_app

'''
3 metody create body dla każego typu wyszukiwania.
autocomplete może być tylko dla jednego pola, 
dla reszty - loop

metodę fts przemianować na search_index i body tworzyć odsyłając do odpowiedniej metody create_body. Metoda, pola i model musi być przesyłane w widoku
'''


def create_body(searchable_fields):
    pass

def fts(index, q_term, fields):
    if not current_app.elasticsearch:
        return [], 0
    search_res = current_app.elasticsearch.search(
            index = index
            )
    pass


#
#def autocomplete(index, query):
#    if not current_app.elasticsearch:
#        return [], 0
#    search_res = current_app.elasticsearch.search(
#            index=index,
#            body={'query': 
#                {'multi_match': 
#                    {'query': query, 
#                    'type': 'bool_prefix', 
#                    'fields': ['*']}
#                    }, 'size': 100})
#
##    search_res = [(hit['_id'],hit['_source']['name']) for hit in hits]
#    return  [{'value': hit['_id'], 'label': hit['_source']['name']} 
#            for hit in search_res['hits']['hits']]
#    
#
#def autocomplete_title(index, query):
#    if not current_app.elasticsearch:
#        return [], 0
#    search_res = current_app.elasticsearch.search(
#            index=index,
#            body={'query': 
#                {'multi_match': 
#                    {'query': query, 
#                    'type': 'bool_prefix', 
#                    'fields': ['*']}
#                    }, 'size': 100})
#
##    search_res = [(hit['_id'],hit['_source']['name']) for hit in hits]
#    return  [{'value': hit['_id'], 'label': hit['_source']['title']} 
#            for hit in search_res['hits']['hits']]
#
#
#
#def create_index(index, model):
#    if not current_app.elasticsearch:
#        return
#    body = create_body(model.__searchable__)
#    current_app.elasticsearch.indices.create(index=index, body=body)
#
#
#
#def add_to_index(index, model):
#    if not current_app.elasticsearch:
#        return
#    if not current_app.elasticsearch.indices.exists(index=index):
#        create_index(index, model)
#    body = {}
#    for field in model.__searchable__:
#        body[field] = getattr(model, field)
#    current_app.elasticsearch.index(index=index, id=model.id, body=body)
#
#
#def remove_from_index(index, model):
#    if not current_app.elasticsearch:
#        return
#    current_app.elasticsearch.delete(index=index, id=model.id)
#
#
#
