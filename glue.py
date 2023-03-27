import time
from elasticsearch7 import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import json
import time
import re


N_results = 5
def elastic_more_like_this(sentence):
    res  = ""
    a = es.search(index='bulk1', query = {
        "more_like_this" : {
            "fields" : ['text'],
            "like" : f"{sentence}",
            "min_term_freq" : 1,
            "max_query_terms" : 12
            }
        }
    )
    count = 0
    for element in a['hits']['hits']:
        el = element['_source']['text'].strip()
        res += f' ++++++++++++++++++++++++++++++++ {el}'
        count += 1
        if count > 5:
            break
    return res


file = open("spanner.test")
conll = json.load(file)
for sentence in conll:
    span_posLabel = sentence['span_posLabel']
    context = sentence['context']
    res1  = context + elastic_more_like_this(context)
    #отделить знаки препинания от текста
    res2 = re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', r' \g<0> ', res1).strip()
    print(f'context = {context}\n res = {res2}\n')
    input()
