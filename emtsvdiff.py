#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2019.11.19.

"""
import csv
import sys
import eval
import diff
import agree
import argparse


FIELD_MAP = {
    'form': 'tokendiff',
    'lemma': 'tageval',
    'xpostag': 'tageval',
    'upostag': 'tageval',
    'feats': 'tageval',
    'NP-BIO': 'chunkeval',
    'NER-BIO': 'chunkeval',
    'id': 'depeval',
}


def get_column(header, field):

    return [key for key in header.keys() if (header[key] == field)][0]


def proc_fields(a_fields, b_fields):
    """
    feldolgozza a két fájl fejlécét
    veszi a metszetüket
    eltárolja, hogy hányadik oszlopban vannak az egyes mezők a fájlokban
    :param a_fields:
    :param b_fields:
    :return:
    """

    # közös mezők a fejlécben
    common_fields = set(a_fields.values()) | set(b_fields.values())

    columns = dict()
    for field in common_fields:
        columns[field] = (get_column(a_fields, field), get_column(b_fields, field))

    return columns


def get_tasks(columns):
    """

    :param columns:
    :return:
    """
    # feladatok a mezőknek megfeleltetve
    tasks = dict()
    for field, cols in columns.items():
        if field in FIELD_MAP:
            tasks[cols] = FIELD_MAP[field]

    return tasks


def get_header(infile):

    with open(infile, 'r') as inf:
        header = {i: name for i, name in enumerate(inf.readline().strip().split())}

    return header


def read_file(infile):
    """
    beolvassa a fájl a csv readerrel
    elmenti
    skippeli a mondathatárokat
    TODO mondatonként is el kéne tárolni a dependencia kiértékeléséhez
    :param infile:
    :return:
    """

    lines = list()

    with open(infile, 'r') as inf:

        # itt csak beolvassa a headert de nem menti el (már megvan)
        inf.readline().strip().split()

        reader = csv.reader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) > 1 and '#' not in line[0]:
                lines.append(line)
            # elif len(line) == 0:
            #     lines.append('')
            else:
                pass

    return lines


def main():
    """
    - beolvassa a fájlokat                                                  DONE
    - kiszedi, hogy melyik fájlban melyik mező melyik oszlopban van         DONE
        ha különböző sorrendben vannak, egységesíti                         DONE
    - megállapítja a mezők metszetét                                        DONE
    - megkérdezi a felhasználót, hogy mi a feladat                          HALF DONE
    - a kért feladatot végrehajtja a meglévő mezőkre                        HALF DONE

                        diff            eval            agree
    form                DONE            -               -
    lemma               -               DONE            DONE
    xpostag             -               DONE            DONE
    upostag             -               DONE            DONE
    feats               -               DONE            DONE
    id, head, deprel    -               TODO            TODO
    NP-BIO              -               TODO            TODO
    NER-BIO             -               TODO            TODO

    :return:
    """

    # megkérdezi a felhasználüt, hogy melyik üzemmódot szeretné
    # beszedi a két össszehasonlítandó fájl relatív elérését
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("-m", "--mode", required=True, action="append", help="Select mode! (diff, eval, agree)", default=[])
    parser.add_argument("-f1", "--file1", required=True, type=str, help="File 1")
    parser.add_argument("-f2", "--file2", required=True, type=str, help="File 2")

    args = parser.parse_args()

    mode = args.mode

    filea = args.file1
    fileb = args.file2

    # kinyeri a két fálj fejlécét
    a_fields = get_header(filea)
    b_fields = get_header(fileb)
    # elmenti, hogy a közös mezők melyik oszlopban vannak a fájlokban (lehet, hogy különböznek!)
    columns = proc_fields(a_fields, b_fields)
    print(columns)

    # beolvassa a két fájl
    filea_lines = read_file(filea)
    fileb_lines = read_file(fileb)

    # elkészíti a deltát, ahol meg vannak jelölve a tokenkülönbségek
    # ehhez a 'form' oszlopot használja
    delta = diff.differ(filea_lines, fileb_lines, columns['form'])
    diff.diff_tokens(delta, columns['form'])
    diff.count_token(delta)

    if "diff" in mode:
        pass

    if "eval" in mode:
        # meghatározza, hogy milyen feladatokat kell elvégezni az egyes mezőkkel
        tasks = get_tasks(columns)
        # az egyes feladatokat elvégzi a megfelelő mezőkkel
        for column, task in tasks.items():
            if task == 'tageval':
                # TODO írja ki a mező nevét
                eval.diff_tags(delta, column)

            if task == 'chunkeval':
                # NP-BIO
                # NER-BIO
                eval.diff_chunks(delta, column)

            if task == 'depeval':
                # id        ha van id, akkor indul a depeval
                # head      ezt az oszlopot meg kell keresni
                # deprel    ezt az oszlopot meg kell keresni
                head = columns['head']
                deprel = columns['deprel']
                eval.diff_deps(delta, column, head, deprel)

    if "agree" in mode:
        # agreement a tokenenkénti címkézési feladatokra
        print('agree lemma')
        agree.agree_tags(delta, columns['lemma'])
        print('agree xpostag')
        agree.agree_tags(delta, columns['xpostag'])
        print('agree upostag')
        agree.agree_tags(delta, columns['upostag'])
        print('agree feats')
        agree.agree_tags(delta, columns['feats'])


if __name__ == "__main__":
    main()
