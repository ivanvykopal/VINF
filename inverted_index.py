import os
import math
from constants import DIRECTORY, ID, FREQUENCY


class InvertedIndex:
    """
    Trieda obsahujúca index a metódy, určené pre prácu s indexom.
    """
    def __init__(self):
        """
        Inicializácia indexu ako dictionary.
        """
        self._index = dict()

    def add_term(self, term, frequency, file_id):
        """
        Metóda pre pridanie termu do indexu spolu s frekvenciou daného termu v súbore spolu s názvom súboru.
        :param term: term
        :param frequency: freknvecia termu v zadanom súbore
        :param file_id: názov súboru
        """
        if term in self._index:
            self._index[term] = self._index[term] + [(file_id, frequency)]
        else:
            self._index[term] = [(file_id, frequency)]

    def get_appearances(self, term):
        """
        Metóda pre vrátenie posting listu.
        :param term: term, pre ktorý hľadáme posting list
        :return: postiing list, pre zadaný term, inak None
        """
        if term in self._index:
            return self._index[term]
        return None

    def get_index(self):
        """
        Metóda pre vrátenie indexu.
        :return: index
        """
        return self._index

    def set_index(self, index):
        """
        Metóda pre nastavenie indexu.
        :param index: index
        """
        self._index = index

    def sort_index(self):
        """
        Metóda pre usporiadanie indexu abecedne.
        """
        self._index = dict(sorted(self._index.items()))

    def tf_idf(self, term, index):
        """
        Metóda na výpočet tf-idf pre zadaný term a súbor.
        :param term: hľadaný term
        :param index: index dokumentu
        :return: hodnotu tf-idf pre daný term
        """
        n = len(os.listdir(DIRECTORY))
        values = self._index[term]
        df = len(values)
        idf = math.log(n / df, 10)
        value = values[index]
        tf = value[FREQUENCY]
        tf_idf = tf * idf
        return tf_idf

    def wf_idf(self, term, index):
        """
        Metóda na výpočet wf-idf pre zadný term a index. Wf-idf predstavuje logaritmické škálovanie.
        :param term: hľadaný term
        :param index: index dokumentu
        :return: hodnotu wf-idf pre daný term
        """
        n = len(os.listdir(DIRECTORY))
        values = self._index[term]
        df = len(values)
        idf = math.log(n / df, 10)
        value = values[index]
        tf = value[FREQUENCY]
        wtf = 1 + math.log(tf, 10)
        wf_idf = wtf * idf
        return wf_idf
