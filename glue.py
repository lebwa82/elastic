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


input_file = open("spanner.test")


res_list = []
conll = json.load(input_file)
count_sentence = 0
for sentence in conll:
    count_sentence += 1
    if count_sentence %100 == 0:
        print(f'count_sentence = {count_sentence} time = {time.time() - start}')
    # if count_sentence > 500:
    #     break

    span_posLabel = sentence['span_posLabel']
    context = sentence['context']
    max_number = 900
    res1  = context + elastic_more_like_this(context)
    res2 = res1.split(' ')
    if len(res2) > max_number:
        diff = len(res2) - max_number
        for ii in range(diff):
             res2.pop()
    
    if len(res2) > max_number:
         print('error')
         input()
    res2 = list(filter(None, res2))
    # print(res2)
    # input()

    res1 = (' '.join(res2))
    
    dict_sentence = {'context': res1, 'span_posLabel': span_posLabel}
    res_list.append(dict_sentence)
    glue_text.write(f'{res1}\n')
    #input()


with open('spanner_new_new.json', 'w') as fp:
        # Преобразование объектов Python в данные 
        # JSON формата, а так же запись в файл 'data.json'
        json.dump(res_list, fp)
