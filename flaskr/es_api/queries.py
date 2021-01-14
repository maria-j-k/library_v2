from flask import current_app


def ac_person(query):
    if not current_app.elasticsearch:
        return [], 0
    search_res = current_app.elasticsearch.search(index='person',
            body={
                'query': {
                    'multi_match': {
                        'query': query, 
                        'type': 'bool_prefix', 
                        'fields': ['*'],
                        'operator': 'and',
                        }
                    }, 
                'size': 10})

    return  [{'value': hit['_id'], 'label': hit['_source']['name']} 
            for hit in search_res['hits']['hits']]
    

def ac_serie(query, publisher=None):
    body =  {
      "query": {
        "bool": {
          "must": [
            {
              "multi_match": {
                 "query": query,
                 "type": "bool_prefix",
                 "fields": ["name"]
               }
            },
            {
              "match": {
                 "publisher_id": publisher
               }
            }
          ]
        }
      }
    }

    search_res = current_app.elasticsearch.search(index = 'serie', body = body)
    return [{'value': hit['_id'], 'label': hit['_source']['name']}
            for hit in search_res['hits']['hits']]

def ac_publisher(query):
    body = {
            'query': {
                'multi_match': {
                    'query': query, 
                    'type': 'bool_prefix', 
                    'fields': ['name']
                    }
                }, 
            'size': 10}

    search_res = current_app.elasticsearch.search(index = 'publisher', body = body)
    return [{'value': hit['_id'], 'label': hit['_source']['name']}
            for hit in search_res['hits']['hits']]

def ac_city(query):
    body = {
            'query': {
                'multi_match': {
                    'query': query, 
                    'type': 'bool_prefix', 
                    'fields': ['name']
                    }
                }, 
            'size': 10}

    search_res = current_app.elasticsearch.search(index = 'city', body = body)
    return [{'value': hit['_id'], 'label': hit['_source']['name']}
            for hit in search_res['hits']['hits']]
