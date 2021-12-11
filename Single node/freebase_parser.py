import re
import time
import gzip
import jsonpickle
from regex import R_TITLE, R_ALT, R_TYPE, R_EN, R_LANG, R_LANG_TERM
from constants import TYPE_FILE, TITLE_FILE, ALT_FILE, NON_TYPES, FREEBASE_DATA


def get_non_types():
    """
    Metoda pre ulozenie typov, ktore budeme ignorovat.
    :return: mnozina typov pre ignorovanie
    """
    # Otvorenie suboru s typmi, ktore budeme ignorovat na zaklade frekvencnej analyzy 100 milionov riadkov
    file = open(NON_TYPES, 'r', encoding='utf-8')
    lines = set()
    # Ulozenie jednotlivých typov do setu
    for line in file:
        lines.add(line.strip())
    file.close()

    return lines


def parse_line(line, fh_title, fh_type, fh_alt):
    """
    Metoda urcena na parsovanie riadku z Freebase databazy.
    :param line: riadok, z ktoreho parsujem data
    :param fh_title: file handler pre zapis title
    :param fh_type: file handler pre zapis type
    :param fh_alt: file handler pre zapis alt
    """

    # Kontrola, ci riadok obsahuje nazov
    result = re.search(R_TITLE, line)
    if result:
        fh_title.write(result.group(1) + "\t" + result.group(2) + "\n")
        return

    # Kontrola, ci riadok obsahuje typ
    result = re.search(R_TYPE, line)
    if result:
        string = re.sub(r"[_\.]", " ", result.group(2))
        fh_type.write(result.group(1) + "\t" + string + "\n")

    # Kontrola, ci riadok obsahuje alternativny nazov
    result = re.search(R_ALT, line)
    try:
        if result:
            string = re.search(R_LANG_TERM, result.group(2)).group(1)
            fh_alt.write(result.group(1) + "\t" + string + "\n")
    except Exception:
        print('Riadok: ' + line)
        print(result.group())

    # Kontrola, ci riadok obsahuje alternativny nazov v inom jazyku
    result = re.search(R_LANG, line)
    if result:
        string = result.group(2)
        if re.search(R_EN, string):
            return
        try:
            string = re.search(R_LANG_TERM, string).group(1)
            fh_alt.write(result.group(1) + "\t" + string + "\n")
        except Exception:
            print('Riadok: ' + line)
            print(result.group())


def check_line(file, string, check):
    """
    Metoda na zistenie, ci sa dany retazec nachadza v subore.
    :param file: subor, v ktorom hladame vyskyt retazca
    :param string: hladany retazec
    :param check: True, ak sa ma kontrolovat retazec, inak False
    :return: True, ak bol najdeny vyskyt, inak False
    """
    for line in file:
        if check and string in line.strip():
            return True
    return False


def merge_data():
    """
    Metoda na spojenie jednotlivych udajov do suborov reprezentujucich objekty.
    Nazov suboru bude vytvoreny z ID z Freebase databazy, pricom do suboru sa pridaju udaje ako su:
       - nazov,
       - typy,
       - alternativne nazvy
    Do suboru sa ukladaju data v podobe JSON, pre lepsiu a lahsiu pracu pri nacitanie.
    """
    print("merger")

    # Vytvorenie jednotlivych suborov pre objekty s pridanim nazvov pre tieto objekty
    file = open(TITLE_FILE, 'r', encoding='utf-8')
    # print("nazvy")
    data = dict()
    for line in file:
        (id, title) = line.split("\t")
        if id and title:
            if id not in data.keys():
                data[id] = {'id': id, 'title': title.strip(), 'types': [], 'alts': []}

    file.close()

    # Pridanie typov do jednotlivych suborov podla id objektu
    file = open(TYPE_FILE, 'r', encoding='utf-8')

    # nacitanie typov, ktore budeme ignorovat
    non_types = get_non_types()
    # print("typy")
    for line in file:
        (id, type) = line.split("\t")
        type = type.strip()
        # ak sa typ nachadza medzi ignorovanymi pokracujeme na dalsi typ
        if type.strip() in non_types:
            continue
        # Identifikacia, ci id sa uz v dictionary nachadza, ak ano pridame mu typ
        if id in data.keys():
            record = data[id]
            if type not in record['types']:
                record['types'].append(type)
                data[id] = record

    file.close()

    # Pridanie alternativnych nazvov do jednotlivych suborov podla id objektu
    file = open(ALT_FILE, 'r', encoding='utf-8')
    # print("aliasy")
    for line in file:
        (id, alt) = line.split("\t")
        alt = alt.strip()
        # Identifikacia, ci id sa uz v dictionary nachadza, ak ano pridame mu alternativny text
        if id in data.keys():
            record = data[id]
            if alt not in record['alts']:
                record['alts'].append(alt)
                data[id] = record

    file.close()

    # Ulozenie objektov do jednotlivych suborov
    for key in data.keys():
        output_file = open('../files/objects/' + key + '.txt', 'w', encoding='utf-8')
        json_data = jsonpickle.encode(data[key], unpicklable=False)
        output_file.write(json_data + "\n")
        output_file.close()


def parse_data(line_num):
    """
    Metoda na parsovanie zadaneho poctu riadkov z Freebase databazy.
    :param line_num: pocet riadkov, ktore chceme parsovať
    """
    # Otvorenie suboru obsahujuceho freebase data
    file_in = gzip.open(FREEBASE_DATA, 'rt', encoding='utf-8')
    # file_in = open(FREEBASE_DATA, 'rt', encoding='utf-8')
    # Otvorenie suborov pre zapis nazvov, typov a alternativnych nazvov
    file_title = open(TITLE_FILE, 'w', encoding='utf-8')
    file_type = open(TYPE_FILE, 'w', encoding='utf-8')
    file_alt = open(ALT_FILE, 'w', encoding='utf-8')

    start_time = time.time()
    num = 1
    # Postupne prechadzanie Freebase databazy po riadkoch
    while True:
        line = file_in.readline()

        if not line or num == line_num:
            break

        if num % 10_000_000 == 0:
            print(num)

        num = num + 1
        # Parsovanie riadku
        parse_line(line, file_title, file_type, file_alt)

    file_in.close()
    file_type.close()
    file_title.close()
    file_alt.close()
    merge_data()
    print("Cas behu pre Parser: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    
    parse_data(100_000_000)
