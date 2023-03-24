
import os
import get_words_from_conll
import time
from elasticsearch7 import Elasticsearch
from elasticsearch7 import helpers
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

conll_words_set = get_words_from_conll.get_conll_words_set()

start = time.time()

dict_conll_words = dict()
for word in conll_words_set:
    dict_conll_words[word] = 0

es.indices.delete(index="bulk1")
es.indices.create(index="bulk1")

# file = open('data.xml-0001.txt', 'r')
list_files = os.listdir('/home/dima/wiki/text/text')
path_dir = '/home/dima/wiki/text/text'
count_added_lines = 0
count_all_lines = 0
count_files = 0
line_list = []
id = 1
actions = []
for filename in list_files:
    file = open(f'{path_dir}/{filename}', 'r')
    count_files += 1
    # if count_files%100 == 0:
    #print(
    #    f'count_files = {count_files}, time = {time.time() - start} count_added_lines = {count_added_lines}')
    while True:
        line = file.readline()
        if not line:
            break
        if not line[0].isalpha():
            continue

        flag = False
        for word in conll_words_set:
            if word in line:
                if dict_conll_words[word] == 1000:
                    conll_words_set.discard(word)
                elif dict_conll_words[word] < 1000:
                    dict_conll_words[word] += 1
                    #count_added_lines += 1
                    flag = True
                break

        if flag:
            # pass
            count_added_lines += 1
            # line_list.append(line)
            actions.append(
                {
                    "_index": "bulk1",
                    #"_type": "1",
                    "_id": id,
                    "_source": {
                        "text": line,
                    }
                }
            )

            #doc = {'text': line}

            # es.index(index="wiki2", doc_type="1", id=id, body=doc)
            id += 1
    if count_files > 300:
        break

# for i in actions:
#     print(i)
#     input()
print(f'count_added_lines = {count_added_lines}')
print(f'len(actions)  = {len(actions)}')
# input()
end = time.time()
print(end - start)
helpers.bulk(es, actions)
end = time.time()
print(end - start)


# i = 1
# while True:
#     res = es.get(index="bulk1", id=i)
#     i += 1
#     #print(i)
#     #print(res['_source'])
#     if i > count_added_lines:
#         break
#     #input()
# print(f'i = {i}')    

# end = time.time()
# print(end - start)