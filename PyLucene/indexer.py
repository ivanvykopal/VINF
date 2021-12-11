import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
import os
import re
import time

DIRECTORY = './vykopal'
REGEX = r'(.*)\sTYPES\s(.*)\sALTS\s(.*)\n'

def create_index():
    """
    Metoda pre zaindexovanie objektov vyextrahovanych z Freebase.
    """
    # Zadefinovanie, kde sa bude index ukladat
    store = SimpleFSDirectory(Paths.get("myIndex"))
    # Konfiguracia indexu s vyuzitim StandardAnalyzer - pozostava z tokenizacie a odstranovania stop slov
    config = IndexWriterConfig(StandardAnalyzer())
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    # Zadefinovanie indexu
    writer = IndexWriter(store, config)

    # Vytvorenie listu so subormi, ktore sa nachadzaju v adresari obsahujuceho subory pre zaindexovanie 
    files = os.listdir(DIRECTORY)

    # V ramci cyklu postupne prechadzame vsetky subory a riadky, ktore indexujeme
    for fname in files:
        with open(DIRECTORY + '/' + fname, 'r', encoding='utf8') as file:
            line = file.readline()
            # Postupne nacitanie vsetkych riadkov aktualneho suboru
            while line:
                # Aplikacia regexu na riadok
                result = re.search(REGEX, line)
                if result:
                    # Vytiahnutie informacii z vysledku regularneho vyrazu: nazov, typy a alternativne texty
                    title = result.group(1)
                    types = result.group(2)
                    alts = result.group(3)
                    # Vytvorenie dokumentu a jeho nasledne naplnenie do jednotlivych fieldov
                    doc = Document()
                    doc.add(Field("title", title, TextField.TYPE_STORED))
                    doc.add(Field("type", types, TextField.TYPE_STORED))
                    doc.add(Field("alternative", alts, TextField.TYPE_STORED))
                    doc.add(Field("field_content", title + "\t" + types + "\t" + alts, TextField.TYPE_NOT_STORED))
                    # Zapisanie dokumentu do indexu
                    writer.addDocument(doc)
                line = file.readline()
    
    # Vykonaie commit operacie a uzatvorenie indexu
    writer.commit()
    writer.close()


if __name__ == '__main__':

    # Potrebny riadok kodu pre spustenie pyLucene
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    start_time = time.time()
    create_index()
    print("Cas behu pre Indexer: " + str((time.time() - start_time)) + " sekund!")
