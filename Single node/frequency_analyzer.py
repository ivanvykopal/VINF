from constants import TYPE_FILE
import json


def analyze():
    """
    Metoda urcena pre analyzovanie frekvencie typov. Pomocou tejto metody identifikujeme, ktore typy budeme ignorovat.
    """
    file = open(TYPE_FILE, 'r', encoding='utf-8')
    index = dict()
    num = 1
    # Prechadzanie suboru po riadkoch
    for line in file:
        #if num % 100_000 == 0:
        #    print(num)
        num = num + 1
        # rozdelenie riadku na ID a TYP
        (id, type) = line.split("\t")
        type = type.strip()
        # Pocitanie vyskutu typov v subore
        if type in index:
            index[type] = index[type] + 1
        else:
            index[type] = 1
    file.close()
    print("tokens created")

    # Utriedenie typov podla poctu vyskytov
    index = {k: v for k, v in sorted(index.items(), key=lambda item: item[1])}
    # Zapisanie 
    with open("json-frequency.txt", "w") as outfile:
        json.dump(index, outfile)


if __name__ == '__main__':

    analyze()
