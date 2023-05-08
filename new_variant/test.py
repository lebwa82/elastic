import pickle
# data.xml-2569.txt_24683
# data.xml-2569.txt_24661
# data.xml-2569.txt_24585
dict_conll = 0
wiki_lines_dict = 0

with open('dict_conll.pkl', 'rb') as f:
    dict_conll = pickle.load(f)

with open('wiki_lines_dict.pkl', 'rb') as f:
    wiki_lines_dict = pickle.load(f)

print(wiki_lines_dict['data.xml-2569.txt_24683'])
print(wiki_lines_dict['data.xml-2569.txt_24661'])
print(wiki_lines_dict['data.xml-2569.txt_24585'])


print(dict_conll['175'])