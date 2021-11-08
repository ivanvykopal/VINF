import re
import time
import json
import jsonpickle
from constants import OUTPUT_FILE
from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex
import pandas as pd


def index_file(row, file):
    """
    Metóda pre zaindexovania údajov z vybraného súboru.
    :param row: riadok, ktorý tokenizujeme
    :return: id objektu
             index pre daný súbor v tvare dictionary
    """
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
        file.write(token + '\t' + json_data['id'] + "\n")


def index_terms():
    file = open('./files/terms.txt', 'r', encoding='utf-8')
    terms = list()
    ids = list()
    for i, line in enumerate(file):
        term, id = line.strip().split('\t')
        terms.append(term)
        ids.append(id)

    file.close()
    data = {'terms': terms, 'ids': ids}
    df = pd.DataFrame(data=data)
    df = df.sort_values(['terms', 'ids'], ascending=[True, True])

    df.to_csv('./files/dataframe.csv', index=False)
    frequency = df.groupby(df.columns.tolist(), as_index=False).size()
    frequency.to_csv('./files/duplicates.csv', index=False)


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
    file_writer = open('./files/terms.txt', 'w', encoding='utf-8')
    while True:
        line = file.readline()
        i = i + 1
        if not line:
            break
        #if i % 100000 == 0:
        #    print(i)

        index_file(line, file_writer)

    file_writer.close()
    file.close()

    index_terms()

    print("Vytvaranie indexu")
    my_index.create_index('./files/duplicates.csv')
    print("Utriedenie indexu")
    my_index.sort_index()
    print("Vypocet wf_idf")
    my_index.wf_idf()
    print("Ulozenie indexu")
    with open("index.json", "w", encoding='utf-8') as outfile:
        json.dump(my_index.get_index(), outfile)

    print("Cas behu pre Indexer: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    create_index()
