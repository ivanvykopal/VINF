import json
from search_engine import search
from regex import R_MAX_COUNT
from inverted_index import InvertedIndex
import re


def read_index():
    """
    Metóda pre načítanie indexu zo súboru.
    :return: načítaný index
    """
    with open("../files/index.json") as jsonFile:
        index = json.load(jsonFile)

    return index


if __name__ == '__main__':
    print("-----------------------------------------------------------------------------------------------------------")
    print("                                   System na vyhladanie objektov z Freebase                                ")
    print("-----------------------------------------------------------------------------------------------------------")

    my_index = InvertedIndex()
    my_index.set_index(read_index())
    while True:
        print("\n\nPre moznost vyhladavania zadajte dopyt")
        print("S prepinacom -n, za ktorym nasleduje cislo udate maximalny pocet zaznamov na vypis. Musi byt uvedeny na "
              "konci dopytu! Priklad: query -n 10")
        print("Pre ukoncenie zadajte -q")
        query = input("Vasa moznost: ")
        if query == "":
            print("Zadali ste neplatný dopyt!")
        elif query in ["-q", "-Q"]:
            break
        else:
            max_count = -1
            result = re.search(R_MAX_COUNT, query)
            if result:
                max_count = result.group(2)
                query = result.group(1)
            search(query, my_index, int(max_count))
