#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2019.10.09.

"""
import csv
import sys
import difflib


def differ(filea, fileb):

    diff = difflib.Differ()
    # TODO nem biztos, hogy az [1] oszlopban van a form! a fájlbeolvasásnál kellene csekkolni
    result = list(diff.compare([line[1] for line in filea], [line[1] for line in fileb]))

    zipped = list()
    r = 0
    a = 0
    b = 0

    while r < len(result):

        if result[r].startswith('+ '):
            zipline = ('+', fileb[b])
            b += 1
        elif result[r].startswith('- '):
            zipline = (filea[a], '-')
            a += 1
        else:
            zipline = (filea[a], fileb[b])
            a += 1
            b += 1

        zipped.append(zipline)
        r += 1

    return zipped


def read_file(infile):

    lines = list()

    with open(infile) as inf:
        reader = csv.reader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) > 1 and '#' not in line[0]:
                lines.append(line)
            elif len(line) == 0:
                lines.append('')
            else:
                pass

    return lines


def count_token(diff):

    filea = len(diff)
    fileb = len(diff)
    for line in diff:
        if line[0] == '+':
            filea -= 1
        elif line[1] == '-':
            fileb -= 1

    print('file_a token number', filea)
    print('file_b token number', fileb)


def diff_tokens(diff):

    filea = list()
    fileb = list()

    for line in diff:
        if line[0] == '+':
            fileb.append(line[1][1])
        elif line[1] == '-':
            filea.append(line[0][1])

    print('file_a tokens', filea)
    print('file_b tokens', fileb)


def diff_tags(diff):
    # TODO itt csak kitesztelem a szófajcímkét, de legyen dinamikus az oszlop

    total = 0
    tp = 0

    for line in diff:
        if line[0] != '+' and line[1] != '-':
            if line[0][3] == line[1][3]:
                tp += 1
            total += 1

    print('POS accuracy: {0:.2%}'.format(tp/total))

    """
    teszt FEATS
    """

    total = 0
    tp = 0

    for line in diff:
        if line[0] != '+' and line[1] != '-':
            if line[0][5] == line[1][5]:
                tp += 1
            total += 1

    print('FEATS accuracy: {0:.2%}'.format(tp / total))


def print_stats(diff):

    count_token(diff)
    diff_tokens(diff)
    diff_tags(diff)


def main():

    filea = sys.argv[1]
    fileb = sys.argv[2]

    filea_lines = read_file(filea)
    fileb_lines = read_file(fileb)

    diff = differ(filea_lines, fileb_lines)

    print_stats(diff)


if __name__ == "__main__":
    main()
