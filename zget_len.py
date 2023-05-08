import json
span_file = open('/home/dima/SpanNER/data/conll03/spanner_old.test', 'r', encoding='utf-8')
digit_file = open('/home/dima/SpanNER/data/conll03/digit.txt', 'w', encoding='utf-8')
count_my_words_file = open('/home/dima/SpanNER/data/conll03/count_my_words_file.txt', 'w', encoding='utf-8')
conll = json.load(span_file)
count_sentence = 0
for sentence in conll:	
    count_sentence += 1

    context = sentence['context']
    words = context.split(' ')
    len_words = len(words)
    count_my_words_file.write(f'{len_words}\n')
    count = 0
    if len_words == 1:
        count = 1
    elif len_words == 2:
        count = 3
    elif len_words == 3: 
        count = 6
    else: 
        for i in range(4):
            count += len_words
            len_words -= 1
    digit_file.write(f'{count}\n')
    
