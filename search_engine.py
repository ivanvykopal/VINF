from analyzer import tokenize, remove_stop_words
from inverted_index import InvertedIndex
from constants import OUTPUT_FILE
import jsonpickle


def find_intersection_documents(posting_lists):
    # final_documents bude na konci obsahovať zoznam dokumentov, v ktorých sa vyskytujú všetky slová z dopytu
    final_documents = []
    if len(posting_lists) == 1:
        final_documents = list(posting_lists[0])
    elif len(posting_lists) == 2:
        final_documents = list(posting_lists[0].intersection(posting_lists[1]))
    elif len(posting_lists) > 2:
        current_set = posting_lists[0].intersection(posting_lists[1])
        length = len(posting_lists)
        for x in range(3, length):
            current_set = current_set.intersection(posting_lists[x])
        final_documents = list(current_set)

    return final_documents


def print_info(file_name, score):
    """
    Metóda pre vypísanie informácie o vybranom dokumente.
    :param file_name: názov súboru
    :param score: skóre dokumentu
    """
    file = open('./files/objects/' + file_name + '.txt', 'r', encoding='utf-8')
    line = file.readline()
    file.close()
    json_data = jsonpickle.decode(line.strip())
    title = json_data['title']
    types = json_data['types']
    alts = json_data['alts']

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
    posting_lists = []
    for token in tokens:
        docs = my_index.get_appearances(token)
        if docs is None:
            print("\n Reťazec " + token + " sa v indexe nenachádza!\n")
            return
        help_set = set()
        for doc in docs:
            help_set.add(doc['id'])
        posting_lists.append(help_set)

    # final_documents bude na konci obsahovať zoznam dokumentov, v ktorých sa vyskytujú všetky slová z dopytu
    final_documents = find_intersection_documents(posting_lists)

    print("\nCelkový počet dokumentov, v ktorých sa dopyt nachádza: " + str(len(final_documents)) + "\n")

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
    # výpočet tf_idf
    query_index.tf_idf(1)

    # výpočet skóre jednotlivých dokumentov
    scores = dict()
    for key in query_index.get_index().keys():
        # získanie tf-idf pre term
        tf_idf = float(query_index.get_appearances(key)[0]['tf_idf'])
        # získanie posting listu pre term
        appearances = my_index.get_appearances(key)
        if not appearances:
            continue
        # výpočet skóre na základe daného termu
        for index, app in enumerate(appearances):
            file_id = app['id']
            # kontrola, či daný dokument je v prieniku => vykonávame AND operáciu
            if file_id not in final_documents:
                continue
            wf_idf = app['wf_idf']
            score = tf_idf * wf_idf
            if file_id in scores:
                scores[file_id] = scores[file_id] + score
            else:
                scores[file_id] = score

    print("Skóre je vypočítané, hľadajú sa dokumenty!\n")
    # zoradnie dokumentov podľa skóre od najväčšieho po najmenšie
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    # print(sorted_scores)
    if len(sorted_scores) == 0:
        print("\nNeboli najdene ziadne zaznamy!\n\n")
        return

    # vypísanie info pre jednotlivé dokumenty
    i = 1
    for key in sorted_scores.keys():
        print_info(key, sorted_scores[key])
        i = i + 1
        if max_count != -1 and i > max_count:
            break
