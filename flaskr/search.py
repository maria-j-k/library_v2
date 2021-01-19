from flask import current_app

def create_body(sayt_field):
    field = {"type": "text",
            "analyzer": "ascii_analyzer",
            "fields": {"keyword": {"type": "keyword"},
              "sayt": {"type": "search_as_you_type"}
            }}

    body = {
          "settings": {
            "analysis": {
              "analyzer": {
                "ascii_analyzer":{
                  "type": "custom",
                  "char_filter": ["html_strip"],
                  "tokenizer": "standard",
                  "filter": [
                    "lowercase",
                    "asciifolding"]
                }
              }
            }
          },
        "mappings":{
            "properties": {
            }
        }
    }
    body['mappings']['properties'][sayt_field] = field
    return body


def create_index(index, model):
    if not current_app.elasticsearch:
        return
    body = create_body(model.__sayt__)
    current_app.elasticsearch.indices.create(index=index, body=body)



def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(index, model)
    field = model.__sayt__
    body = {field: getattr(model, field)}
    current_app.elasticsearch.index(index=index, id=model.id, body=body)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def es_fuzzy_search(index, field, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search_res = current_app.elasticsearch.search(
            index=index,
            body={
              "query": {
                "match": {
                  field: {
                    "query": query,
                    "operator": "or", 
                    "fuzziness": "auto"
                  }
                }
              },
              'from': (page - 1) * per_page, 
              'size': per_page
            })

    ids = [int(hit['_id']) for hit in search_res['hits']['hits']]
    return ids, search_res['hits']['total']['value']

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





