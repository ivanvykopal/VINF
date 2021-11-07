import re
from constants import STOP_WORDS
from regex import R_DIGIT_WORD


def get_stop_words():
    """
    Metóda pre uloženie stop slov zo súboru do setu.
    :return: množina stop slov
    """
    file = open(STOP_WORDS, 'r', encoding='utf-8')
    lines = set()
    for line in file:
        lines.add(line.strip())
    file.close()

    return lines


def tokenize(line):
    """
    Metóda pre tokenizáciu riadku.
    :param line: riadok zo súboru
    :return: list s jednotlivými tokenmi
    """
    line = line.strip().lower()
    tokens = re.split(R_DIGIT_WORD, line)
    return tokens


def remove_stop_words(tokens):
    """
    Metóda pre odstránenie stop slov a prázdnych reťazcov zo zoznamu tokenov.
    :param tokens: list tokenov
    :return: upravený list tokenov
    """
    stop_words = get_stop_words()
    i = 0
    while i < len(tokens):
        if tokens[i] in stop_words:
            del tokens[i]
            i = i - 1
        if i >= 0 and tokens[i] == "":
            del tokens[i]
            i = i - 1
        i = i + 1

    return tokens
