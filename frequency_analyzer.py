from constants import TYPE_FILE
from analyzer import tokenize, remove_stop_words
import json


def analyze():
    """
    Metóda určená pre analyzovanie frekvencie typov. Pomocou tejto metódy identifikujeme, ktoré typy budeme ignorovať.
    """
    file = open(TYPE_FILE, 'r', encoding='utf-8')
    index = dict()
    num = 1
    for line in file:
        if num % 100_000 == 0:
            print(num)
        num = num + 1
        (id, type) = line.split("\t")
        type = type.strip()
        if type in index:
            index[type] = index[type] + 1
        else:
            index[type] = 1
    file.close()
    print("tokens created")

    index = {k: v for k, v in sorted(index.items(), key=lambda item: item[1])}
    with open("json-frequency.txt", "w") as outfile:
        json.dump(index, outfile)


if __name__ == '__main__':
    """
    Metóda pre spustenie frekvenčného analyzátora ako samostatného programu
    """
    analyze()
