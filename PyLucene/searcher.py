import lucene
import re
from org.apache.lucene.search import IndexSearcher
from java.nio.file import Paths
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

R_MAX_COUNT = r'(.*) -n\s*([\d]+)'

def search(text, count):
    """
    Metoda urcena pre vyhladavanie v ramci vytvoreneho indexu.
    :param query: dopyt od pouzivatela
    :param count: maximalny pocet zobrazenych vysledkov
    """
    # Zadefinovanie miesta, kde je index ulozeny
    directory = SimpleFSDirectory(Paths.get("myIndex"))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    # Vyhladavanie s vyuzitim default fieldu, StandardAnalyzer-a a dopytu od pouzivatela
    result = re.search('.*(title|type|alternative):.*', text)
    if result:
        query = QueryParser("<default field>", StandardAnalyzer()).parse(text)
    else:
        query = QueryParser("field_content", StandardAnalyzer()).parse(text)
    # V pripade aj je count -1, vtedy pouzivatel nezadal prepinac -n, tak sa vyuziva deafultny pocet, ktory je 50
    # inak sa vuyziva hodnota z prikazu od pouzivatela po azdani prepinaca -n
    if count == -1:
        scoreDocs = searcher.search(query, 50).scoreDocs
    else:
        scoreDocs = searcher.search(query, count).scoreDocs
    # Vypis jednotlivych vysledkov, ktore su zoradene podla skore dokuemntu, ktory vypocital pyLucene
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # Vypis informacii o aktualnom objekte, vypisujeme: nazov, typy a laternativne texty
        print("Nazov:\t\t\t" + doc.get("title"))
        print("Typy:\t\t\t" + "\n\t\t\t".join(doc.get("type").split('\t')))
        print("Alternativy:\t\t" + "\n\t\t\t".join(doc.get("alternative").split('\t')))
        print("\n----------------------------------------------------------------------------------------------------------"
            "-\n")


if __name__ == '__main__':

     # Potrebny riadok kodu pre spustenie pyLucene
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    # Vypis hlavicky programu
    print("-----------------------------------------------------------------------------------------------------------")
    print("                                   System na vyhladanie objektov z Freebase                                ")
    print("-----------------------------------------------------------------------------------------------------------")
    print("\n\nPre moznost vyhladavania zadajte dopyt")
    print("Dopyt povoluje vyhladavanie prostrednictvom fieldov: title, type, alterantive\n")
    print("S prepinacom -n, za ktorym nasleduje cislo udava maximalny pocet zaznamov na vypis. Musi byt uvedeny na "
              "konci dopytu! Priklad: query -n 10")
    print("Pre ukoncenie zadajte -q")
    print("-----------------------------------------------------------------------------------------------------------")

    # While cyklus pre zadavanie prikazov od pouzivatela
    while True:
        # Nacitanie prikazu od pouzivatela z konzoly
        query = input('Zadajte prikaz: ')
        # Kontrola prikazu
        if query == "":
            # V pripade, ak je prikaz prazdny, tak je pouzivatel o tom oboznameny
            print("Zadali ste neplatný dopyt!")
        elif query in ["-q", "-Q"]:
            # V pripade, ak prikaz obsahuje prepinac -q alebo -Q, tak je system ukonceny
            break
        else:
            # Inak sa prikaz skontroluje regexom, ci neobsahuje prepinac -n so zadanou hodnotou
            max_count = -1
            result = re.search(R_MAX_COUNT, query)
            if result:
                # V pripade vyskytu prepinaca -n, je potrebne rodzelit prikaz na samsotny dopyt a hodnotu
                max_count = result.group(2)
                query = result.group(1)
            # Spustenie vyhladanvania s vyuzitim implementovanej metody
            search(query, int(max_count))
