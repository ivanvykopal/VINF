import re
from constants import STOP_WORDS
from regex import R_DIGIT_WORD


def get_stop_words():
    """
    Metoda pre ulozenie stop slov zo suboru do setu.
    :return: mnozina stop slov
    """
    # Otvorenie suboru obsahujuceho anglicke stop slova
    file = open(STOP_WORDS, 'r', encoding='utf-8')
    lines = set()
    # Pridavanie stop slov do setu
    for line in file:
        lines.add(line.strip())
    file.close()

    return lines


def tokenize(line):
    """
    Metoda pre tokenizaciu riadku.
    :param line: riadok zo suboru
    :return: list s jednotlivymi tokenmi
    """
    line = line.strip().lower()
    # Rozdelenie riadku prostrednictvom azdefinovaneho regularneho vyrazu
    tokens = re.split(R_DIGIT_WORD, line)
    return tokens


def remove_stop_words(tokens):
    """
    Metoda pre odstranenie stop slov a prazdnych retazcov zo zoznamu tokenov.
    :param tokens: list tokenov
    :return: upraveny list tokenov
    """
    # Nacitanie stop slov vyuzitim implementovanej funkcie
    stop_words = get_stop_words()
    i = 0
    # Postupne prechadzanie tokenov a odstranovanie stop slov a prazdnych tokenov
    while i < len(tokens):
        if tokens[i] in stop_words:
            del tokens[i]
            i = i - 1
        if i >= 0 and tokens[i] == "":
            del tokens[i]
            i = i - 1
        i = i + 1

    return tokens
