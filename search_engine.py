from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex
from regex import R_FILE_ALT, R_FILE_TYPE, R_FILE_TITLE
import re
from constants import DIRECTORY, ID


def print_info(file_name, score):
    """
    Metóda pre vypísanie informácie o vybranom dokumente.
    :param file_name: názov súboru
    :param score: skóre dokumentu
    """
    file = open(DIRECTORY + file_name, 'r', encoding='utf-8')
    title = None
    types = list()
    alts = list()
    for line in file:
        line = line.strip()

        result = re.search(R_FILE_TITLE, line)
        if result:
            title = result.group(1)
            continue

        result = re.search(R_FILE_TYPE, line)
        if result:
            types.append(result.group(1))
            continue

        result = re.search(R_FILE_ALT, line)
        if result:
            alts.append(result.group(1))
            continue

    file.close()

    print("Nazov:\t\t\t" + title)
    print("ID:\t\t\t\t" + file_name)
    print("Skóre:\t\t\t" + str(score))
    print("Typy:\t\t\t" + "\n\t\t\t\t".join(types))
    print("Alternativy:\t" + "\n\t\t\t\t".join(alts))
    print("\n----------------------------------------------------------------------------------------------------------"
          "-\n")


def search(query, my_index, max_count):
    """
    Metóda pre vyhľadanie dopytu prostredníctvom indexu.
    :param max_count: maximálny počet záznamov, ktoré bude parsovať
    :param query: hľadaný dopyt
    :param my_index: index
    """
    # tokenizácia dopytu
    tokens = tokenize(query)

    # odstránenie stop slov a prázdnych reťazcov z pomedzi tokenov
    tokens = remove_stop_words(tokens)

    # vytvorenie objektu pre invertovaný index pre dopyt
    query_index = InvertedIndex()
    index = dict()
    for token in tokens:
        if token in index:
            index[token] = index[token] + 1
        else:
            index[token] = 1

    for key in index.keys():
        query_index.add_term(key, index[key], 'query')

    # zoradenie indexu abecedne
    query_index.sort_index()

    # výpočet skóre jednotlivých dokumentov
    scores = dict()
    for key in query_index.get_index().keys():
        # získanie tf-idf pre term
        tf_idf = query_index.tf_idf(key, 0)
        # získanie posting listu pre term
        appearances = my_index.get_appearances(key)
        if not appearances:
            continue
        # výpočet skóre na základe daného termu
        for index, app in enumerate(appearances):
            file_id = app[ID]
            wf_idf = my_index.wf_idf(key, index)
            score = tf_idf * wf_idf
            if file_id in scores:
                scores[file_id] = scores[file_id] + score
            else:
                scores[file_id] = score

    # zoradnie dokumentov podľa skóre od najväčšieho po najmenšie
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    # print(sorted_scores)
    if len(sorted_scores) == 0:
        print("\nNeboli najdene ziadne zaznamy!\n\n")

    # vypísanie info pre jednotlivé dokumenty
    i = 1
    for key in sorted_scores.keys():
        print_info(key, sorted_scores[key])
        i = i + 1
        if max_count != -1 and i > max_count:
            break
