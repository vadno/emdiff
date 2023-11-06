# emDiff

**emDiff** can compare and evaluate the output of certain modules of [emtsv](https://github.com/dlt-rilmta/emtsv) and it provides interannotator agreement scores for annotations in the format of [xtsv](https://github.com/dlt-rilmta/xtsv).

### comparison

The tokenized texts are compared by the tokens. Only identical tokens are taken into account at the evaluation and calculating agreement. Comparison is done by the package of [difflib](https://docs.python.org/3/library/difflib.html).

After the comparison it applies the chosen task all the possible fields represented in both of the files. The user needs to look up the required result in the output.

The result of the comparion can be required by chosing `printdiff` mode. The output is a `tsv` file. The first column contains the tokens of the first file, the second column contains the tokens of the second file. In the case of bias `+` in the first column indicates that the token presents only in the second file, `-` indicates that the token presents only in the first file.

### evaluation

`eval` and `zeroeval` modes are for evaluation tasks.

#### `eval`

With chosing `eval` mode the output of certain modules of [emtsv](https://github.com/dlt-rilmta/emtsv) can be evaluated. The following scores are applied to the certain fields:

* **lemma**: accuracy
* **xpostag**: accuracy, precision, recall, F-measure
* **upostag**: accuracy, precision, recall, F-measure
* **feats**: accuracy, precision, recall, F-measure
* **NP-BIO**: IOB-accuracy (by token), precision, recall, F-measure (by chunk)
* **NER-BIO**: IOB-accuracy (by token), precision, recall, F-measure (by chunk)
* **id, head, deprel** (dependency parsing): LAS (_labeled attachment score_) , UAS (_unlabeled attachment score_)
* **cons**: accuracy, precision, recall, F-measure

Confusion matrix is available to certain fields (**xpostag**, **upostag**, **feats**, **cons**).

#### `zeroeval`

`zeroeval` mode is for evaluating the performance of [emZero](https://github.com/vadno/emzero), a module of [emtsv](https://github.com/dlt-rilmta/emtsv) that inserts zero pronouns into the text. This mode uses the following measures: precision, recall, F-measure.

### interannotator agreement

By choosing `agree` mode interannotator agreement is calculable for certain tagging tasks of the following fields:

* **lemma**
* **xpostag**
* **upostag**
* **feats**
* **cons**

Interannotator agreement scores are provided by the package of [nltk.metrics.agreement](https://www.nltk.org/_modules/nltk/metrics/agreement.html):

* observed agreement
* S
* Pi
* Kappa
* weighted Kappa
* Alpha

Find a detailed description of the interannotator agreement scores: [Artstein-Poesio: Survey Article: Inter-Coder Agreement for Computational Linguistics](https://www.aclweb.org/anthology/J08-4004/).

Interannotator agreement in dependency parsing is calculable with the following scores:

* UAA (_unlabeled attachment agreement_)
* LAA (_labeled attachment agreement_)
* LOA (_label only agreement_)

## Usage

```
python3 emtsvdiff.py -m printdiff -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m eval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m zeroeval -f1 afile.xtsv -f2 bfile.xtsv 
python3 emtsvdiff.py -m agree -f1 afile.xtsv -f2 bfile.xtsv 
```

## Citing and License

**emDiff** is licensed under the GPL 3.0 license.

Please, cite this article:

```
@inproceedings{emtsv3,
    author = {Simon, Eszter and Indig, Balázs and Kalivoda, Ágnes and Mittelholcz, Iván and Sass, Bálint and Vadász, Noémi},
    title = {Újabb fejlemények az e-magyar háza táján},
    booktitle = {{XVI}. {M}agyar {S}zámítógépes {N}yelvészeti {K}onferencia ({MSZNY} 2020)},
    editor = {Berend, Gábor and Gosztolya, Gábor and Vincze, Veronika},
    pages = {29--42},
    publisher = {Szegedi Tudományegyetem, TTIK, Informatikai Intézet},
    address = {Szeged},
    year = {2020}
}
```
