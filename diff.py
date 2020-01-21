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


def count_token(delta):
    """
    megszámolja a tokenszámokat
    :param delta:
    :return:
    """

    filea = len(delta)
    fileb = len(delta)
    for col1, col2 in delta:
        if col1 == '+':
            filea -= 1
        elif col2 == '-':
            fileb -= 1

    print('file_a token number:', filea)
    print('file_b token number:', fileb)


def diff_tokens(delta):
    """
    listázza a csak az egyik vagy csak a másik fájlban szereplő tokeneket
    :param delta:
    :return:
    """

    filea = list()
    fileb = list()

    for col1, col2 in delta:
        if col1 == '+':
            fileb.append(col2[0])
        elif col2 == '-':
            filea.append(col1[0])

    print('file_a tokens', filea)
    print('file_b tokens', fileb)
