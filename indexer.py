import re
import time
import json
import os
from regex import R_ATTRIBUTE, R_ID
from constants import DIRECTORY
from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex


def read_index():
    """
    Metóda pre načítanie indexu zo súboru.
    :return: načítaný index
    """
    with open("index.json") as jsonFile:
        index = json.load(jsonFile)

    return index


def index_file(file_name):
    """
    Metóda pre zaindexovania údajov z vybraného súboru.
    :param file_name: názov súboru, ktorý budeme indexovať
    :return: id objektu
             index pre daný súbor v tvare dictionary
    """
    file = open(file_name, 'r', encoding='utf-8')
    index = dict()
    for line in file:
        result = re.search(R_ATTRIBUTE, line.strip())
        string = result.group(2)

        # tokenizácia reťazca
        tokens = tokenize(string)

        # odstránenie stop slov a prázdnych reťazcov z pomedzi tokenov
        tokens = remove_stop_words(tokens)
        for token in tokens:
            if token in index:
                index[token] = index[token] + 1
            else:
                index[token] = 1

    file.close()

    return re.search(R_ID, file_name).group(1), index


def create_index():
    """
    Metóda pre vytvorenie celkového indexu pre všetky súbory, ktoré sa nachádzajú v ./files.
    Zoradenie indexu podľa abecedy a aj výpočet váh pomocou logaritmickej škálovatosti - wf-idf.
    """
    start_time = time.time()
    my_index = InvertedIndex()
    for file in os.listdir(DIRECTORY):
        file_id, index = index_file(DIRECTORY + file)
        for key in index.keys():
            my_index.add_term(key, index[key], file_id)

    my_index.sort_index()
    with open("index.json", "w", encoding='utf-8') as outfile:
        json.dump(my_index.get_index(), outfile)

    print("Cas behu pre Indexer: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    create_index()
