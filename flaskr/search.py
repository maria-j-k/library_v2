from flask import current_app

def create_body(searchable_fields):
    sayt = {"type": "search_as_you_type"}
    body = {
        "mappings":{
            "properties": {
                "id": {"type": "integer"},
            }
        }
    }
    for item in searchable_fields:
        body['mappings']['properties'][item] = sayt
    return body


def create_index(index, model):
    if not current_app.elasticsearch:
        return
    body = create_body(model.__searchable__)
    current_app.elasticsearch.indices.create(index=index, body=body)



def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(index, model)
    body = {}
    for field in model.__searchable__:
        body[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=body)


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
    

def es_fuzzy_search(index, query):
    if not current_app.elasticsearch:
        return [], 0
    search_res = current_app.elasticsearch.search(
            index=index,
            body={
              "_source": False,
              "query": {
                "match": {
                  "name": {
                    "query": query,
                    "operator": "and", 
                    "fuzziness": "auto"
                  }
                }
              }
            })

#    search_res = [(hit['_id'],hit['_source']['name']) for hit in hits]
    print(list(hit['_id'] for hit in search_res['hits']['hits']))
    return  [{'id': hit['_id']} 
            for hit in search_res['hits']['hits']]







