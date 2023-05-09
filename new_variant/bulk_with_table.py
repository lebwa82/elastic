
import os
import get_words_from_conll
import time
import pickle
from elasticsearch7 import Elasticsearch
from elasticsearch7 import helpers
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

dict_conll, conll_words_set, dict_word_to_id_dict_conll = get_words_from_conll.get_conll_words_set()

start = time.time()

dict_conll_words = dict()
for word in conll_words_set:
    dict_conll_words[word] = 0


# name_index= 'wiki_test'
# es.indices.create(index=name_index)
dict_sentense_conll_ner_wiki_paragraph = {}
dict_id_wiki_paragraph = {}

# file = open('data.xml-0001.txt', 'r')
list_files = os.listdir('/home/dima/wiki/text/text')
path_dir = '/home/dima/wiki/text/text'
count_added_lines = 0
count_all_lines_all_files = 0

count_files = 0
line_list = []
wiki_lines_dict = {}
actions = []

#list_files = ['data.xml-0001.txt']#поработаем пока с одним файлом

for filename in list_files:
    file = open(os.path.join(path_dir,filename), 'r')
    count_all_lines_in_file = 0
    count_files += 1
    # if count_files > 2:
    #     break
   
    if count_files%10 == 0:
        print(f'count_files = {count_files}, time = {time.time() - start} count_added_lines = {count_added_lines}')
    

    while True:
        count_all_lines_in_file += 1
        count_all_lines_all_files += 1
        try:
            line = file.readline()
        except Exception:
            continue
        #print(line)
        
        if not line:
            break
        if not line[0].isalpha():
            continue
        

        flag = False
        word_in_line = None
        for word in conll_words_set:
            if word in line:
                if dict_conll_words[word] == 1000:
                    conll_words_set.discard(word)
                elif dict_conll_words[word] < 1000:
                    dict_conll_words[word] += 1
                    #count_added_lines += 1
                    flag = True
                    word_in_line = word
                break

        if flag:
            wiki_line_id = f'{filename}_{count_all_lines_in_file}'
            wiki_lines_dict[wiki_line_id] = {'line': line, 'dict_conll_ids': dict_word_to_id_dict_conll[word_in_line]}
            for id in dict_word_to_id_dict_conll[word_in_line]:
                for ner_dict in dict_conll[id]['ners']:#ner_dict лежат в листе
                    ner_word = ner_dict['ner']
                    if word_in_line == ner_word:#значит надо добавить в этот NER доп контент
                        ner_dict['wiki_paragraphs_id'] = wiki_line_id
                        #ner_dict['count_wiki_paragraphs'] += 1


            count_added_lines += 1



            # actions.append(
            #     {
            #         "_index": name_index,
            #         #"_type": "1",
            #         "_id": id,
            #         "_source": {
            #             "text": line,
            #         }
            #     }
            # )

    # if count_files > 300:
    #     break

# for i in actions:
#     print(i)
#     input()


# with open('dict_conll.pkl', 'wb') as file:
#     pickle.dump(dict_conll, file)

# with open('wiki_lines_dict.pkl', 'wb') as file:
#     pickle.dump(wiki_lines_dict, file)




# print(f'count_added_lines = {count_added_lines}')
# print(f'len(actions)  = {len(actions)}')
# # input()
# end = time.time()
# print(end - start)
# #helpers.bulk(es, actions)
# end = time.time()
# print(end - start)


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