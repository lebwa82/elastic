import time
from elasticsearch7 import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import json
import time
import re
glue_text = open('glue_text.txt', 'w')
start = time.time()

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
        #отделить знаки препинания от текста
        re_el = re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', r' \g<0> ', el).strip()
        res += f' ++++++++++++++++++++++++++++++++ {re_el}'
        count += 1
        if count > 5:
            break
    return res


file = open("spanner.test")
conll = json.load(file)
count_sentence = 0
for sentence in conll:
    count_sentence += 1
    if count_sentence %100 == 0:
        print(f'count_sentence = {count_sentence} time = {time.time() - start}')
    span_posLabel = sentence['span_posLabel']
    context = sentence['context']
    res1  = context + elastic_more_like_this(context)
    #отделить знаки препинания от текста
    #res2 = re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', r' \g<0> ', res1).strip()
    #print(f'context = {context}\n res = {res2}\n')
    glue_text.write(f'{res1}\n')
    #input()
