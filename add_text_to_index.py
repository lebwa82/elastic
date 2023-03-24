import string
import time


start = time.time()
from elasticsearch7 import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

print(es)
print(es.info())

file = open('data.xml-0001.txt', 'r')

es.indices.delete(index="wiki1")
es.indices.create(index="wiki1")  

id = 1
while True:
    line = file.readline()
    if not line:
        break
    if not line[0].isalpha():
        continue

    doc = {'text': line}
    es.index(index="wiki1", doc_type="1", id=id, body=doc)
    id += 1

end = time.time()
print(end - start) 