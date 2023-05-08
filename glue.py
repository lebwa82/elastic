
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
from elasticsearch7 import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import json
import time
import re
glue_text = open('glue_text.txt', 'w')
start = time.time()
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')




def get_token_len(text123):
    encoded_input = tokenizer(text123, return_tensors='tf')
    res = encoded_input.input_ids.shape[1]
    return res

def cut_text(text123, max_len = 500):
    while get_token_len(text123) > max_len:
        #print(get_token_len(text123))
        chunks = text123.split(' ')
        for i in range(10):
            chunks.pop()
        text123 = ' '.join(chunks)
    return text123


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
        res += f' {re_el} '
        count += 1
        if count > 3:
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
        #break

    span_posLabel = sentence['span_posLabel']
    context = sentence['context']
    res  = context +' --_-- ' + elastic_more_like_this(context)
    #print('before = ', res)
    bef_len = len(res.strip())
    bef_token = get_token_len(res)

    res = cut_text(res)
    # while "  " in res:
    #     res = res.replace("  ", " ")
    
    res = res.encode('ascii', 'ignore').decode()
    res = res.replace("\t", "")
    while "  " in res:
        res = res.replace("  ", " ")
    
    
    
    dict_sentence = {'context': res, 'span_posLabel': span_posLabel}
    res_list.append(dict_sentence)
    glue_text.write(f'{res}\n')
    # if count_sentence > 50:
    #     break


with open('spanner_new_plus_500.json', 'w') as fp:
        # Преобразование объектов Python в данные 
        # JSON формата, а так же запись в файл 'data.json'
        json.dump(res_list, fp)
