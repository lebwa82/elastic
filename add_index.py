
import time
from elasticsearch7 import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import get_words_from_conll
import os

conll_words_set = get_words_from_conll.get_conll_words_set()

start = time.time()

dict_conll_words = dict()
for word in conll_words_set:
    dict_conll_words[word] = 0

es.indices.delete(index="wiki2")
es.indices.create(index="wiki2")  

# file = open('data.xml-0001.txt', 'r')
list_files = os.listdir('/home/dima/wiki/text/text')
path_dir = '/home/dima/wiki/text/text'
count_added_lines = 0
count_all_lines = 0
count_files = 0
line_list = []
id = 1
for filename in list_files:
    file = open(f'{path_dir}/{filename}', 'r')
    count_files += 1
    # if count_files%100 == 0:
    print(f'count_files = {count_files}, time = {time.time() - start} count_added_lines = {count_added_lines}')
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
                    dict_conll_words[word] +=1
                    count_added_lines += 1
                    flag = True
                break
                
        if flag:
            # pass
            #count_added_lines += 1
            #line_list.append(line)

            doc = {'text': line}
            es.index(index="wiki2", doc_type="1", id=id, body=doc)
            id += 1

end = time.time()
print(end - start) 

print(f'line_list = {len(line_list)}')
print(f'count_all_lines = {count_all_lines}')