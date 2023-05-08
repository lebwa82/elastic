
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
import pickle



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


#N_results = 5
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
    res_list = []
    for element in a['hits']['hits']:
        el = element['_source']['text'].strip()
        #отделить знаки препинания от текста
        re_el = re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', r' \g<0> ', el).strip()
        res = f' {re_el} '
        res_list.append(res)

    return res_list


input_file = open("spanner.test")


res_list = []
conll = json.load(input_file)
dop_context_len_list = []
dop_context_plus_res_len_list = []
dict_sentence_with_less_ten_contexts = {}
count_sentence = 0
for sentence in conll:
    count_sentence += 1
    if count_sentence %100 == 0:
        print(f'count_sentence = {count_sentence} time = {time.time() - start}')
        #break

    span_posLabel = sentence['span_posLabel']
    context = sentence['context']
    dop_context_list = elastic_more_like_this(context)


    if len(dop_context_list) == 0:
        dict_sentence_with_less_ten_contexts[context] = dop_context_list
        dop_context_list = [''] * 10
        
        # if 'DOCSTART' not in context:
        #     print(context)
        #input()
    elif len(dop_context_list) < 10:
        #print(f'context = {context}')
        #input()
        # zero = dop_context_list[0]
        # dop_context_list = [zero] * 10
        dict_sentence_with_less_ten_contexts[context] = dop_context_list
        dop_context_list = [''] * 10
    for dop_context in dop_context_list:
        res  = context +' --_-- ' + dop_context
        #print('before = ', res)
        dop_context_len = get_token_len(dop_context)
        dop_context_len_list.append(dop_context_len)
        bef_len = len(res.strip())
        bef_token = get_token_len(res)
        dop_context_plus_res_len_list.append(bef_token)

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


# with open('spanner_new_plus_500_tokens_10_sentense_for_each_first_when_less_10_no_context.json', 'w') as fp:
#         # Преобразование объектов Python в данные 
#         # JSON формата, а так же запись в файл 'data.json'
#         json.dump(res_list, fp)

# with open('dop_context_len_file.pkl', 'wb') as file:
#     pickle.dump(dop_context_len_list, file)

# with open('dop_context_plus_res_len_list.pkl', 'wb') as file:
#     pickle.dump(dop_context_plus_res_len_list, file)

# with open('dict_sentence_with_less_ten_contexts.pkl', 'wb') as file:
#     pickle.dump(dict_sentence_with_less_ten_contexts, file)

# from collections import Counter
# a = dict(Counter(dop_context_len_list))
# print(a)  

# print('\n\n\n\n\n\n\n\n\n')

# a = dict(Counter(dop_context_plus_res_len_list))
# print(a)  

# print('\n\n\n\n\n\n\n\n\n')
# print(dict_sentence_with_less_ten_contexts)