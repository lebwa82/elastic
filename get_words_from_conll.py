import json

conll_words_set = set()
def get_conll_words_set():
    file = open("spanner.test")
    conll = json.load(file)
    for sentence in conll:
        span_posLabel = sentence['span_posLabel']
        context = sentence['context'].split(' ')
        #print(context)
        for substance in span_posLabel.keys():
            if len(substance) > 1:
                chunks = substance.split(';')
                #print(chunks)
                start = int(chunks[0])
                end = int(chunks[1])
                # print(start, end)
                full_word = ''
                for i in range(start, end+1):
                    full_word += f'{context[i]} '
                full_word = full_word[:-1]
                # print(full_word)
                conll_words_set.add(full_word)
        # print(conll_words_set)
        # input()
    print(f'len(conll_words_set) = {len(conll_words_set)}')
    # print(conll_words_set)
    return conll_words_set

if __name__ == '__main__':
    get_conll_words_set()
