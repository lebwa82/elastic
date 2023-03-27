
import os
import get_words_from_conll
import time
from elasticsearch7 import Elasticsearch
from elasticsearch7 import helpers
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
start = time.time()
i = 1
while True:
    res = es.get(index="bulk1", id=i)
    i += 1
    #print(i)
    #print(res['_source'])
    if i > 1063933:
        break
    if i%50000 == 0:
        print(f'i = {i}, time = {time.time() - start}')
    #input()
print(f'i = {i}')  