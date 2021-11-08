import math
import os
from constants import OUTPUT_FILE


class InvertedIndex:
    """
    Trieda obsahujúca index a metódy, určené pre prácu s indexom.
    """
    def __init__(self):
        """
        Inicializácia indexu ako dictionary.
        """
        self._index = dict()


    def create_index(self, file_name):
        file = open(file_name, 'r', encoding='utf8')
        first_line = True
        prev_term = None
        for i, line in enumerate(file):
            if first_line:
                first_line = False
                continue
            #if i % 100_000 == 0:
            #    print(i)
            term, document, freq = line.strip().split(',')
            if prev_term is None or prev_term != term:
                self._index[term] = [{'id': document, 'freq': freq}]
                prev_term = term
            else:
                self._index[term].append({'id': document, 'freq': freq})

        file.close()

    def add_term(self, term, frequency, file_id):
        """
        Metóda pre pridanie termu do indexu spolu s frekvenciou daného termu v súbore spolu s názvom súboru.
        :param term: term
        :param frequency: freknvecia termu v zadanom súbore
        :param file_id: názov súboru
        """
        if term in self._index:
            self._index[term].append({'id': file_id, 'freq': frequency})
        else:
            self._index[term] = [{'id': file_id, 'freq': frequency}]

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

    def tf_idf(self, n=None):
        """
        Metóda na výpočet tf-idf pre zadaný term a súbor.
        :param n: počet dokumentov
        :return: hodnotu tf-idf pre daný term
        """
        if n is None:
            n = len(os.listdir('./files/objects'))

        for term in self._index.keys():
            values = self._index[term]
            df = len(values)
            idf = math.log(n / df, 10)
            for index in range(0, df):
                value = values[index]
                tf = float(value['freq'])
                tf_idf = tf * idf
                value['tf_idf'] = tf_idf
                values[index] = value

            self._index[term] = values

    def wf_idf(self, n=None):
        """
        Metóda na výpočet wf-idf pre zadný term a index. Wf-idf predstavuje logaritmické škálovanie.
        :param term: hľadaný term
        :param index: index dokumentu
        :param n: počet dokumentov
        :return: hodnotu wf-idf pre daný term
        """
        if n is None:
            n = len(os.listdir('./files/objects'))

        for term in self._index.keys():
            values = self._index[term]
            df = len(values)
            idf = math.log(n / df, 10)
            for index in range(0, df):
                value = values[index]
                tf = float(value['freq'])
                wtf = 1 + math.log(tf, 10)
                wf_idf = wtf * idf
                value['wf_idf'] = wf_idf
                values[index] = value

            self._index[term] = values
