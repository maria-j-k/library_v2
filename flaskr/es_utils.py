from flask import current_app


####
# create index
curl -XPUT 127.0.0.1:9200/persons -d '
{
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "name": {
                "properties": {
                    "name": {"type": "search_as_you_type"}
                    }
                
            }
        }
    }
'

##
# autocomplete search for person
#
curl  -s --request GET 'http://localhost:9200/person/_search?pretty' --data-raw '{
"size": 5,
"query": {
    "multi_match": {
        "query": "mick",
        "type": "bool_prefix",
        "fileds": [
            "name",
            "name._2gram",
            "name._3gram"
            ]
    }
}
}'


