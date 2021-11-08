import re
import os
import shutil
import time
import gzip
import jsonpickle
from regex import R_TITLE, R_ALT, R_TYPE, R_EN, R_LANG, R_LANG_TERM
from constants import TYPE_FILE, TITLE_FILE, ALT_FILE, NON_TYPES, FREEBASE_DATA, OUTPUT_FILE


def get_non_types():
    """
    Metóda pre uloženie typov, ktoré budeme ignorovať.
    :return: množina typov pre ignorovanie
    """
    file = open(NON_TYPES, 'r', encoding='utf-8')
    lines = set()
    for line in file:
        lines.add(line.strip())
    file.close()

    return lines


def clear_data(directory):
    """
    Metóda pre vymazanie súborov z adresára directory.
    :param directory: adresár, z ktorého budeme vymazávať súbory
    """
    shutil.rmtree(directory)
    try:
        os.mkdir(directory)
    except OSError:
        print("Creation of the directory failed!")


def parse_line(line, fh1, fh2, fh3):
    """
    Metóda určená na parosvanie riadku z Freebase databázy.
    :param line: riadok, z ktorho parsujem dáta
    :param fh1: file handler pre zápis title
    :param fh2: file handler pre zápis type
    :param fh3: file handler pre zápis alt
    """

    # Kontrola, či riadok obsahuje názov
    result = re.search(R_TITLE, line)
    if result:
        fh1.write(result.group(1) + "\t" + result.group(2) + "\n")
        return

    # Kontrola, či riadok obsahuje typ
    result = re.search(R_TYPE, line)
    if result:
        string = re.sub(r"[_\.]", " ", result.group(2))
        fh2.write(result.group(1) + "\t" + string + "\n")

    # Kontrola, či riadok obsahuje alternatívny názov
    result = re.search(R_ALT, line)
    try:
        if result:
            string = re.search(R_LANG_TERM, result.group(2)).group(1)
            fh3.write(result.group(1) + "\t" + string + "\n")
    except Exception:
        print('Riadok: ' + line)
        print(result.group())

    # Kontrola, či riadok obsahuje alternatívny názov v inom jazyku
    result = re.search(R_LANG, line)
    if result:
        string = result.group(2)
        if re.search(R_EN, string):
            return
        try:
            string = re.search(R_LANG_TERM, string).group(1)
            fh3.write(result.group(1) + "\t" + string + "\n")
        except Exception:
            print('Riadok: ' + line)
            print(result.group())


def check_line(file, string, check):
    """
    Metóda na zistenie, či sa daný reťazec nachádza v súbore.
    :param file: súbor, v ktorom hľadáme výskyt reťazca
    :param string: hľadaný reťazec
    :param check: True, ak sa má kontrolovať reťazec, inak False
    :return: True, ak bol nájdený výskyt, inak False
    """
    for line in file:
        if check and string in line.strip():
            return True
    return False


def merge_data():
    """
    Metóda na spojnenie jednotlivých údajov do súborov reprezentujúcich objekty.
    Názov súboru bude vytvorený z ID z Freebase databázy, pričom do súboru sa pridajú údaje ako sú:
       - názov,
       - typy,
       - alternatívne názvy
    """
    print("merger")
    # clear_data(DIRECTORY)

    # vytvorenie jednotlivých súborov pre objekty s pridaním názvov pre tieto objekty
    file = open(TITLE_FILE, 'r', encoding='utf-8')
    # print("nazvy")
    data = dict()
    for line in file:
        (id, title) = line.split("\t")
        if id and title:
            if id not in data.keys():
                data[id] = {'id': id, 'title': title.strip(), 'types': [], 'alts': []}

    file.close()

    # pridanie typov do jednotlivých súborov podľa id objektu
    file = open(TYPE_FILE, 'r', encoding='utf-8')

    # načítanie typov, ktoré budeme ignorovať
    non_types = get_non_types()
    # print("typy")
    for line in file:
        (id, type) = line.split("\t")
        type = type.strip()
        if type.strip() in non_types:
            continue
        if id in data.keys():
            record = data[id]
            if type not in record['types']:
                record['types'].append(type)
                data[id] = record

    file.close()

    # pridanie alternatívnych názvov do jednotlivých súborov podľa id objektu
    file = open(ALT_FILE, 'r', encoding='utf-8')
    # print("aliasy")
    for line in file:
        (id, alt) = line.split("\t")
        alt = alt.strip()
        if id in data.keys():
            record = data[id]
            if alt not in record['alts']:
                record['alts'].append(alt)
                data[id] = record

    file.close()

    output_file = open(OUTPUT_FILE, 'w+', encoding='utf-8')
    for key in data.keys():
        json_data = jsonpickle.encode(data[key], unpicklable=False)
        output_file.write(json_data + "\n")

    output_file.close()


def parse_data(line_num):
    """
    Metóda na parsovanie zadaného počtu riadkov z Freebase databázy.
    :param line_num: počet riadkov, ktoré chceme parsovať
    """

    file_in = gzip.open(FREEBASE_DATA, 'rt', encoding='utf-8')
    # file_in = open(FREEBASE_DATA, 'rt', encoding='utf-8')
    file_title = open(TITLE_FILE, 'w', encoding='utf-8')
    file_type = open(TYPE_FILE, 'w', encoding='utf-8')
    file_alt = open(ALT_FILE, 'w', encoding='utf-8')

    start_time = time.time()
    num = 1
    while True:
        line = file_in.readline()

        if not line or num == line_num:
            break

        if num % 10_000_000 == 0:
            print(num)

        num = num + 1

        parse_line(line, file_title, file_type, file_alt)

    file_in.close()
    file_type.close()
    file_title.close()
    file_alt.close()
    merge_data()
    print("Cas behu pre Parser: " + str((time.time() - start_time)) + " sekund!")


if __name__ == '__main__':
    """
    Metóda pre spustenie parsera ako samostatného programu
    """
    parse_data(100_000_000)
