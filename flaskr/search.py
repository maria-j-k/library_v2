from flask import current_app



def create_index():
    """można przekazywać model 
            indeks wyciągać z model.__tablename__
            zrobić klucz properties i dic comp dla każego pola z searchable
            """
    if not current_app.elasticsearch:
        return
    index = 'person'
    body = {
        "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
        "mappings":{
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "search_as_you_type"}
            }
        }
}
    current_app.elasticsearch.indices.create(index=index, body=body)


def add_to_index(obj):
    if not current_app.elasticsearch:
        return
    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(obj)
    index = 'person'
    body = {'id': obj.id, 'name': obj.name}
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def autocomplete(index, query):
    if not current_app.elasticsearch:
        return [], 0
    search_res = current_app.elasticsearch.search(
            index=index,
            body={'query': 
                {'multi_match': 
                    {'query': query, 
                    'type': 'bool_prefix', 
                    'fields': ['*']}
                    }, 'size': 100})

#    search_res = [(hit['_id'],hit['_source']['name']) for hit in hits]
    return  [{'value': hit['_id'], 'label': hit['_source']['name']} 
            for hit in search_res['hits']['hits']]
    




