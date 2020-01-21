# emDiff

Az eszköz az [emtsv](https://github.com/dlt-rilmta/emtsv) egyes moduljai által, [xtsv](https://github.com/dlt-rilmta/xtsv) formátumban kibocsátott kimenetek kiértékelésére, illetve a hasonló formátumban készült kézi annotációk összevetésére, annotátorok közötti egyetértés számolására szolgál.

### összevetés

A tokenizált szövegeket a szóalakok mentén veti össze. A kiértékelés és az annotátorok közötti egyetértés számolásakor csak az egyező tokeneket veszi figyelembe. Az összevetést a Python [difflib](https://docs.python.org/3/library/difflib.html) csomagjának segítségével végzi el.

Az összevetés eredménye a `printdiff` mód kiválasztásával elérhető, mely tabulátorral elválasztva tartalmazza az egymás mellé rendelt tokeneket, ahol az első oszlopban az első fájl szóalakja, a második oszlopban a második fájl szóalakja található. Eltérések esetén az első oszlopban megjelenő `+` jel jelzi, hogy a szóalak csak a második fájlban szerepel, a második oszlopban megjelenő '-' jel pedig jelzi, hogy a szóalak csak az első fájlban szerepel.

### kiértékelés

Az `eval` és `zeroeval` módok kiválasztásával különböző kiértékelési feladatok végezhetők el.

#### `eval`

Az `eval` mód kiválasztásával az [emtsv](https://github.com/dlt-rilmta/emtsv) egyes moduljai által kibocsátott mezők tartalmának kiértékelése végezhető el. Az egyes mezőnevek után a kiértékelés mérőszámai olvashatók.

* **lemma**: accuracy
* **xpostag**: accuracy, precision, recall, F-measure
* **upostag**: accuracy, precision, recall, F-measure
* **feats**: accuracy, precision, recall, F-measure
* **NP-BIO**: IOB-accuracy, precision, recall, F-measure (utóbbi három a helyes chunkok alapján, nem a tokenekhez rendelt címkék alapján)
* **NER-BIO**: IOB-accuracy, precision, recall, F-measure (utóbbi három a helyes chunkok alapján, nem a tokenekhez rendelt címkék alapján)
* **id, head, deprel**: LAS (_labeled attachment score_, helyes címke és anyacsomópont) , UAS (_unlabeled attachment score_, helyes anyacsomópont)
* **cons**: accuracy, precision, recall, F-measure

Bizonyos mezők (**xpostag**, **upostag**, **feats**, **cons**) esetében hibamátrixot is kapunk.


    'form': {'tokendiff'},
    'lemma': {'tagacc', 'tagagree'},
    'xpostag': {'tageval', 'confusion', 'tagacc', 'tagagree'},
    'upostag': {'tageval', 'confusion', 'tagacc', 'tagagree'},
    'feats': {'tageval', 'confusion', 'tagacc', 'tagagree'},
    'NP-BIO': {'chunkeval'},
    'NER-BIO': {'chunkeval'},
    'id': {'depeval', 'depagree'},
    'cons': {'tageval', 'confusion', 'tagacc', 'tagagree'}
}

#### `zeroeval`

### annotátorok közötti egyetértés

## használat

függőségek:
* scikit-learn
* nltk
* difflib

futtatás:
```
python3 emtsvdiff.py -m eval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m zeroeval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m agree -f1 afile.xtsv -f2 bfile.xtsv 
```
