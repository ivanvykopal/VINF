import re
import time
import json
import jsonpickle
from constants import OUTPUT_FILE
from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex


def index_file(row):
    """
    Metóda pre zaindexovania údajov z vybraného súboru.
    :param row: riadok, ktorý tokenizujeme
    :return: id objektu
             index pre daný súbor v tvare dictionary
    """
    index = dict()
    json_data = jsonpickle.decode(row.strip())
    string = json_data['title']
    if json_data['types']:
        string = string + ' ' + ' '.join(json_data['types'])

    if json_data['alts']:
        string = string + ' ' + ' '.join(json_data['alts'])

    # tokenizácia reťazca
    tokens = tokenize(string)

    # odstránenie stop slov a prázdnych reťazcov z pomedzi tokenov
    tokens = remove_stop_words(tokens)
    for token in tokens:
        if token in index:
            index[token] = index[token] + 1
        else:
            index[token] = 1
    # print(index)
    return json_data['id'], index


def create_index():
    """
    Metóda pre vytvorenie celkového indexu pre všetky súbory, ktoré sa nachádzajú v ./files.
    Zoradenie indexu podľa abecedy a aj výpočet váh pomocou logaritmickej škálovatosti - wf-idf.
    """
    start_time = time.time()
    my_index = InvertedIndex()

    print('Index file')
    file = open(OUTPUT_FILE, 'r', encoding='utf-8')
    i = 0
    while True:
        line = file.readline()
        i = i + 1
        if not line:
            break
        if i % 1000 == 0:
            print(i)

        file_id, index = index_file(line)
        for key in index.keys():
            my_index.add_term(key, index[key], file_id)

    file.close()
    my_index.sort_index()
    with open("index.json", "w", encoding='utf-8') as outfile:
        json.dump(my_index.get_index(), outfile)

    print("Cas behu pre Indexer: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    create_index()
