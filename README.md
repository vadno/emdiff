# emDiff

Az eszköz az [emtsv](https://github.com/dlt-rilmta/emtsv) egyes moduljai által, [xtsv](https://github.com/dlt-rilmta/xtsv) formátumban kibocsátott kimenetek kiértékelésére, illetve a hasonló formátumban készült kézi annotációk összevetésére, annotátorok közötti egyetértés számolására szolgál.

### összevetés

A tokenizált szövegeket a szóalakok mentén veti össze. A kiértékelés és az annotátorok közötti egyetértés számolásakor csak az egyező tokeneket veszi figyelembe. Az összevetést a Python [difflib](https://docs.python.org/3/library/difflib.html) csomagjának segítségével végzi el.

Az összevetés után megvizsgálja, hogy melyen azok a mezők, amelyek mindkét fájlban szerepelnek és azokra a mezőkre elvégzi a kiválasztott feladatot. A felhasználónak a kimenetben kell megkeresnie a kívánt eredményt.

Az összevetés eredménye a `printdiff` mód kiválasztásával elérhető, mely tabulátorral elválasztva tartalmazza az egymás mellé rendelt tokeneket, ahol az első oszlopban az első fájl szóalakja, a második oszlopban a második fájl szóalakja található. Eltérések esetén az első oszlopban megjelenő `+` jelzi, hogy a szóalak csak a második fájlban szerepel, a második oszlopban megjelenő `-` pedig jelzi, hogy a szóalak csak az első fájlban szerepel.

### kiértékelés

Az `eval` és `zeroeval` módok kiválasztásával különböző kiértékelési feladatok végezhetők el.

#### `eval`

Az `eval` mód kiválasztásával az [emtsv](https://github.com/dlt-rilmta/emtsv) egyes moduljai által kibocsátott mezők tartalmának kiértékelése végezhető el. Az egyes mezőnevek után a kiértékelés mérőszámai olvashatók.

* **lemma**: accuracy
* **xpostag**: accuracy, precision, recall, F-measure
* **upostag**: accuracy, precision, recall, F-measure
* **feats**: accuracy, precision, recall, F-measure
* **NP-BIO**: IOB-accuracy, precision, recall, F-measure (előbbi a tokenekhez rendelt címkék alapján, utóbbi három a chunkok alapján)
* **NER-BIO**: IOB-accuracy, precision, recall, F-measure (előbbi a tokenekhez rendelt címkék alapján, utóbbi három a chunkok alapján)
* **id, head, deprel** (dependenciaelemzés): LAS (_labeled attachment score_, helyes címke és anyacsomópont) , UAS (_unlabeled attachment score_, helyes anyacsomópont)
* **cons**: accuracy, precision, recall, F-measure

Bizonyos mezők (**xpostag**, **upostag**, **feats**, **cons**) esetében hibamátrixot is kapunk.

#### `zeroeval`

A `zeroeval` mód kiválasztásával az [emtsv](https://github.com/dlt-rilmta/emtsv) zérónévmásbeillesztő modulja, az [emZero](https://github.com/vadno/emzero) által produkált kimenet értékelhető ki. A kiértékelés mérőszámai: precision, recall, F-measure.

### annotátorok közötti egyetértés

A `agree` mód kiválasztásával két annotátor által végzett címkézési feladat összevetése történik annotátorok közötti egyetértés mérésére alkalmas mérőszámok segítségével a következő mezőkre:

* **lemma**
* **xpostag**
* **upostag**
* **feats**
* **cons**

A fenti címkézési feladatok esetében a [nltk.metrics.agreement](https://www.nltk.org/_modules/nltk/metrics/agreement.html) csomag által biztosított mérőszámokat kapjuk:

* observed agreement
* S
* Pi
* Kappa
* weighted Kappa
* Alpha

A mérőszámokkal kapcsolatban az alábbi összefoglaló cikkben érdekes tájékozódni: [Artstein-Poesio: Survey Article: Inter-Coder Agreement for Computational Linguistics](https://www.aclweb.org/anthology/J08-4004/).

Annotátorok közötti egyetértést a dependenciaelemzés vonatkozásában az alábbi mérőszámokkal végezhetünk:

* UAA (_unlabeled attachment agreement_, csak anyacsomópont)
* LAA (_labeled attachment agreement_, anyacsomópont és címke)
* LOA (_label only agreement_, csak címke)

## használat

```
python3 emtsvdiff.py -m printdiff -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m eval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m zeroeval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m agree -f1 afile.xtsv -f2 bfile.xtsv 
```
