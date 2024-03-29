import os
import time
import json
import jsonpickle
from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex
import pandas as pd


def index_file(file_name, fie_writer):
    """
    Metóda pre zaindexovania údajov z vybraného súboru.
    :param row: riadok, ktorý tokenizujeme
    :return: id objektu
             index pre daný súbor v tvare dictionary
    """
    file_in = open('../files/objects/' + file_name, 'r', encoding='utf8')
    line = file_in.readline()
    file_in.close()
    json_data = jsonpickle.decode(line.strip())
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
        fie_writer.write(token + '\t' + json_data['id'] + "\n")


def index_terms():
    file = open('../files/terms.txt', 'r', encoding='utf-8')
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

    df.to_csv('../files/dataframe.csv', index=False)
    frequency = df.groupby(df.columns.tolist(), as_index=False).size()
    frequency.to_csv('../files/duplicates.csv', index=False)


def create_index():
    """
    Metóda pre vytvorenie celkového indexu pre všetky súbory, ktoré sa nachádzajú v ./files.
    Zoradenie indexu podľa abecedy a aj výpočet váh pomocou logaritmickej škálovatosti - wf-idf.
    """
    start_time = time.time()
    my_index = InvertedIndex()

    print('Index file')

    file_writer = open('../files/terms.txt', 'w', encoding='utf-8')
    for file in os.listdir('../files/objects'):
        index_file(file, file_writer)

    file_writer.close()

    index_terms()

    print("Vytvaranie indexu")
    my_index.create_index('../files/duplicates.csv')
    print("Utriedenie indexu")
    my_index.sort_index()
    print("Vypocet wf_idf")
    my_index.wf_idf()
    print("Ulozenie indexu")
    with open("../files/index.json", "w", encoding='utf-8') as outfile:
        json.dump(my_index.get_index(), outfile)

    print("Cas behu pre Indexer: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    create_index()
