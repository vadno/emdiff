#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2020.01.15.

"""
import csv
import eval
import diff
import agree
import argparse


FIELD_MAP = {
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


def get_column(header, field):

    return next(key for key in header.keys() if (header[key] == field))


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

    columns = {field: (get_column(a_fields, field), get_column(b_fields, field)) for field in common_fields}

    return columns


def get_tasks(columns):
    """

    :param columns:
    :return:
    """
    # feladatok a mezőknek megfeleltetve
    tasks = {cols: FIELD_MAP[field] for field, cols in columns.items() if field in FIELD_MAP}

    return tasks


def get_header(infile):

    with open(infile, encoding='utf-8') as inf:
        header = {i: name for i, name in enumerate(inf.readline().strip().split())}

    return header, len(header)


def read_file(infile, length):
    """
    beolvassa a fájl a csv readerrel
    elmenti
    a mondathatárokra 'newsent'-ek listáját teszi
    :param infile:
    :param length
    :return:
    """

    lines = list()

    with open(infile, encoding='utf-8') as inf:

        # itt csak beolvassa a headert de nem menti el (már megvan)
        inf.readline().strip().split()

        reader = csv.reader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) > 1 and '#' not in line[0]:
                lines.append(line)
            elif len(line) == 0:
                # egy csupa 'newsent'-et tartalmazo lista hatarolja a mondatokat
                lines.append(['newsent'] * length)
            else:
                pass

    return lines


def get_column_name(columns, key):

    return list(columns.keys())[list(columns.values()).index(key)]


def main():
    """
    - beolvassa a fájlokat
    - kiszedi, hogy melyik fájlban melyik mező melyik oszlopban van
        ha különböző sorrendben vannak, egységesíti
    - megállapítja a mezők metszetét
    - megkérdezi a felhasználót, hogy mi a feladat
    - a kért feladatot végrehajtja a meglévő mezőkre

    :return:
    """

    # megkérdezi a felhasználót, hogy melyik üzemmódot szeretné
    # beszedi a két össszehasonlítandó fájl relatív elérését
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', required=True, action='append', help='Select mode! (eval, zeroeval, agree)',
                        choices={'eval', 'zeroeval', 'agree'}, default=[])
    parser.add_argument('-f1', '--file1', required=True, type=str, help='File 1 (gold/annotator1)')
    parser.add_argument('-f2', '--file2', required=True, type=str, help='File 2 (to evaluate/annotator2)')

    args = parser.parse_args()
    mode = args.mode
    filea = args.file1
    fileb = args.file2

    # kinyeri a két fálj fejlécét
    a_fields, a_length = get_header(filea)
    b_fields, b_length = get_header(fileb)
    # elmenti, hogy a közös mezők melyik oszlopban vannak a fájlokban (lehet, hogy különböző oszlopban vannak!)
    columns = proc_fields(a_fields, b_fields)
    # print(columns)

    # beolvassa a két fájl
    filea_lines = read_file(filea, a_length)
    fileb_lines = read_file(fileb, b_length)

    # elkészíti a deltát, ahol meg vannak jelölve a tokenkülönbségek
    # ehhez a 'form' oszlopot használja
    delta = diff.differ(filea_lines, fileb_lines, columns['form'])
    # diff.count_token(delta)
    # diff.diff_tokens(delta)

    if 'eval' in mode:
        # meghatározza, hogy milyen feladatokat kell elvégezni az egyes mezőkkel
        tasks = get_tasks(columns)

        # az egyes feladatokat elvégzi a megfelelő mezőkkel
        for column, task in tasks.items():

            if 'tagacc' in task:
                colname = get_column_name(columns, column)
                tagacc = eval.eval_tags(delta, column)
                print(colname, 'accuracy: {0:.2%}'.format(tagacc))

            if 'tageval' in task:
                print(get_column_name(columns, column))
                eval.eval_tags_bytag(delta, column)

            if 'confusion' in task:
                print('{} confusion matrix'.format(get_column_name(columns, column)))
                print(eval.confusion(delta, column))

            if 'chunkeval' in task:
                colname = get_column_name(columns, column)
                acc, prec, rec, f1 = eval.eval_chunks(delta, column)
                print(colname, 'IOB-accuracy: {0:.2%}'.format(acc))
                print(colname, 'precision: {0:.2%}'.format(prec))
                print(colname, 'recall: {0:.2%}'.format(rec))
                print(colname, 'f-measure: {0:.2%}'.format(f1))

            if 'depeval' in task:
                # head      ezt az oszlopot meg kell keresni
                # deprel    ezt az oszlopot meg kell keresni
                head = columns['head']
                deprel = columns['deprel']
                las, uas = eval.eval_deps(delta, head, deprel)
                print('dependency evaluation')
                print('LAS: {0:.2%}'.format(las))
                print('UAS: {0:.2%}'.format(uas))

    if 'zeroeval' in mode:

        prec, rec, f1 = eval.eval_zero(delta, columns['id'])
        if prec and rec and f1:
            print('precision: {0:.2%}'.format(prec))
            print('recall: {0:.2%}'.format(rec))
            print('f-measure: {0:.2%}'.format(f1))
        else:
            print('hiányzó érték')

    if 'agree' in mode:

        # meghatározza, hogy milyen feladatokat kell elvégezni az egyes mezőkkel
        tasks = get_tasks(columns)

        # az egyes feladatokat elvégzi a megfelelő mezőkkel
        for column, task in tasks.items():

            if 'tagagree' in task:
                # agreement a tokenenkénti címkézési feladatokra
                print('{} agreement'.format(get_column_name(columns, column)))
                agree.agree_tags(delta, column)
                oa, s, pi, kappa, w_kappa, alpha = agree.agree_tags(delta, column)
                print('observed agreement: {0:.2%}'.format(oa))
                print('S: {0:.2%}'.format(s))
                print('pi: {0:.2%}'.format(pi))
                print('kappa: {0:.2%}'.format(kappa))
                print('weigthed kappa: {0:.2%}'.format(w_kappa))
                print('alpha: {0:.2%}'.format(alpha))

            if 'depagree' in task:
                print('dependency agreement')
                head = columns['head']
                deprel = columns['deprel']
                uaa, laa, loa = agree.agree_dep(delta, head, deprel)
                print('UAA (unlabeled attachment agreement): {0:.2%}'.format(uaa))
                print('LAA (labeled attachment agreement): {0:.2%}'.format(laa))
                print('LOA (label only agreement): {0:.2%}'.format(loa))


if __name__ == '__main__':
    main()
