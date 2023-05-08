import pickle
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
# Open the file in binary mode
with open('dop_context_plus_res_len_list.pkl', 'rb') as file:
      
    # Call load method to deserialze
    myvar = pickle.load(file)
  
    print(myvar)
    a = dict(Counter(myvar))
    #print(a)  

    fig = plt.figure(figsize = (5, 5))
    width = 1.0 
    keys = a.keys()
    values = a.values()
    print(max(keys), max(values))
    plt.bar(a.keys(), a.values(), width, color='g')
    plt.title("Длина обогащения плюс исходный текст")
    plt.xlabel("количество раз")
    plt.ylabel("длина в токенах")
    plt.show()
    count = 0
    for var in myvar:
        if var > 500:
            count += 1
    print(count)