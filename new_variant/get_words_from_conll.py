import json




def get_conll_words_set():
    conll_words_set = set()
    dict_conll = {}
    dict_word_to_id_dict_conll = {}
    id = 0
    file = open("spanner.test")
    conll = json.load(file)
    for sentence in conll:
        span_posLabel = sentence['span_posLabel']
        context = sentence['context'].split(' ')
        #print(context)
        sentence_ners = []
        id += 1
        dict_conll[str(id)] = {'id': id, 'sentence': sentence['context'], 'ners': []}

        for substance in span_posLabel.keys():
            if len(substance) > 1:
                chunks = substance.split(';')
                start = int(chunks[0])
                end = int(chunks[1])

                full_word = ''
                for i in range(start, end+1):
                    full_word += f'{context[i]} '
                full_word = full_word[:-1]#обрезать последний пробел
                
                #sentence_ners.append(full_word)
                if full_word not in conll_words_set:
                    dict_word_to_id_dict_conll[full_word] = [str(id)]
                else:
                    dict_word_to_id_dict_conll[full_word].append(str(id))
                conll_words_set.add(full_word)
                
                dict_conll[str(id)]['ners'].append({'ner': full_word, 'wiki_paragraphs_id': []})
                
        # print(conll_words_set)
        # input()
    print(f'len(conll_words_set) = {len(conll_words_set)}')
    # print(conll_words_set)
    return dict_conll, conll_words_set, dict_word_to_id_dict_conll

if __name__ == '__main__':
    dict_conll, conll_words_set, dict_word_to_id_dict_conll = get_conll_words_set()
    #for id in range(1,10):
        #print(dict_conll[str(id)])
    print(dict_word_to_id_dict_conll)
