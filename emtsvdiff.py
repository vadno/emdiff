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
    'head': {'depeval', 'depagree'},
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
    common_fields = set(a_fields.values()) & set(b_fields.values())

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
    parser.add_argument('-m', '--mode', required=True, action='append', help='Select mode! (eval, zeroeval, agree, printdiff)',
                        choices={'eval', 'zeroeval', 'agree', 'printdiff'}, default=[])  # TODO printdiff
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

    if 'printdiff' in mode:
        diff.printdiff(delta, columns['form'])

    if 'eval' in mode:
        # meghatározza, hogy milyen feladatokat kell elvégezni az egyes mezőkkel
        tasks = get_tasks(columns)

        # az egyes feladatokat elvégzi a megfelelő mezőkkel
        for column, task in tasks.items():

            if 'tagacc' in task:
                colname = get_column_name(columns, column)
                tagacc = eval.eval_tags(delta, column)
                filename = 'results/eval/' + colname + '_accuracy.txt'
                with open(filename, 'w') as of:
                    print(tagacc, file=of)

            if 'tageval' in task:
                colname = get_column_name(columns, column)
                filename = 'results/eval/' + colname + '_prec_rec_f1_bytag.txt'
                bytag = eval.eval_tags_bytag(delta, column)
                with open(filename, 'w') as of:
                    print(bytag, file=of)

            if 'confusion' in task:
                colname = get_column_name(columns, column)
                filename = 'results/eval/' + colname + '_confusion.txt'
                confusion = eval.confusion(delta, column)
                with open(filename, 'w') as of:
                    print(confusion, file=of)

            if 'chunkeval' in task:
                colname = get_column_name(columns, column)
                filename = 'results/eval/' + colname + '_prec_rec_f1.txt'
                acc, prec, rec, f1 = eval.eval_chunks(delta, column)
                with open(filename, 'w') as of:
                    print('IOB-accuracy: ', acc, file=of)
                    print('precision: ', prec, file=of)
                    print('recall: ', rec, file=of)
                    print('f-measure: ', f1, file=of)

            if 'depeval' in task:
                # head      ezt az oszlopot meg kell keresni
                # deprel    ezt az oszlopot meg kell keresni
                head = columns['head']
                deprel = columns['deprel']
                filename = 'results/eval/dependency_las_uas.txt'
                las, uas, total, corr, corrl = eval.eval_deps(delta, head, deprel)
                with open(filename, 'w') as of:
                    print('LAS: ', las, file=of)
                    print('UAS: ', uas, file=of)
                    print('TOTAL: ', total, file=of)
                    print('correct head: ', corr, file=of)
                    print('correct head and label: ', corrl, file=of)

    if 'zeroeval' in mode:

        prec, rec, f1 = eval.eval_zero(delta, columns['id'])
        if prec and rec and f1:
            filename = 'results/eval/zero_prec_rec_f1.txt'
            with open(filename, 'w') as of:
                print('precision: ', prec, file=of)
                print('recall: ', rec, file=of)
                print('f-measure: ', f1, file=of)

    if 'agree' in mode:

        # meghatározza, hogy milyen feladatokat kell elvégezni az egyes mezőkkel
        tasks = get_tasks(columns)

        # az egyes feladatokat elvégzi a megfelelő mezőkkel
        for column, task in tasks.items():

            if 'tagagree' in task:
                # agreement a tokenenkénti címkézési feladatokra
                colname = get_column_name(columns, column)
                filename = 'results/agree/' + colname + '_agree.txt'
                agree.agree_tags(delta, column)
                oa, s, pi, kappa, w_kappa, alpha = agree.agree_tags(delta, column)
                with open (filename, 'w') as of:
                    print('observed agreement: ', oa, file=of)
                    print('S: ', s, file=of)
                    print('pi: ', pi, file=of)
                    print('kappa: ', kappa, file=of)
                    print('weigthed kappa: ', w_kappa, file=of)
                    print('alpha: ', alpha, file=of)

            if 'depagree' in task:
                head = columns['head']
                deprel = columns['deprel']
                filename = 'results/agree/dependency_agree.txt'
                uaa, laa, loa = agree.agree_dep(delta, head, deprel)
                with open(filename, 'w') as of:
                    print('UAA: ', uaa, file=of)
                    print('LAA: ', laa, file=of)
                    print('LOA: ', loa, file=of)


if __name__ == '__main__':
    main()
