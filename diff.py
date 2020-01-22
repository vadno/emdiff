#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib


def differ(filea, fileb, column):
    """
    a difflib segítségével összeveti a két fájl a tokenek mentén
    ebből készít egy összefésült eredményt, amiben tárolja a + és - jelöléseket
    a későbbi feladatokban a + és - jelölésű tokenek kimaradnak majd
    :param filea:
    :param fileb:
    :param column:
    :return:
    """

    delta = difflib.Differ()

    result = list(delta.compare([line[column[0]] for line in filea], [line[column[1]] for line in fileb]))

    zipped = list()
    r = 0
    a = 0
    b = 0
    zipline = tuple()

    while r < len(result):

        if result[r].startswith('+ '):
            zipline = ('+', fileb[b])
            b += 1
        elif result[r].startswith('- '):
            zipline = (filea[a], '-')
            a += 1
        elif result[r].startswith('? '):
            pass
        else:
            zipline = (filea[a], fileb[b])
            a += 1
            b += 1

        zipped.append(zipline)
        r += 1

    return zipped


def printdiff(delta, column):

    with open('results/diff.tsv', 'w') as of:

        for col1, col2 in delta:
            if col1 == '+':
                print('+', col2[column[1]], sep='\t', file=of)
            elif col2 == '-':
                print(col1[column[0]], '-', sep='\t', file=of)
            elif 'newsent' in col1:
                print('', file=of)
            else:
                print(col1[column[0]], col2[column[1]], sep='\t', file=of)
