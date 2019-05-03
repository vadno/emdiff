#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import namedtuple
import difflib  # difflib: https://pymotw.com/2/difflib/

conll_line = namedtuple('CoNLL', 'id, form, lemma, upos, xpos, feats, head, deprel, deps, misc')


def read_file(filename):

    lines = list()
    new_sent = list([' '] * 10)

    with open(filename, encoding='UTF-8') as inf:
        for line in inf:
            if not line.startswith('#'):
                new_line = line.strip().split()
                if not new_line:
                    new_line = new_sent
                lines.append(conll_line._make(new_line))

    return lines


def align(delta, conll1, conll2):

    dummy = list(['DUMMY'] * 10)
    i = 0
    plus = 0
    minus = 0

    while i < len(conll1) and i < len(conll2):

        if delta[i].startswith('+'):
            plus += 1
            conll1.insert(i, conll_line._make(dummy))
        elif delta[i].startswith('-'):
            minus += 1
            conll2.insert(i, conll_line._make(dummy))

        i += 1

    return plus, minus


def diff_texts(conll1, conll2):

    conll1_tok = [conll.form for conll in conll1]
    conll2_tok = [conll.form for conll in conll2]

    differ = difflib.Differ()

    return list(differ.compare(conll1_tok, conll2_tok))


def diff_inline(conll1, conll2, col):

    total = 0
    tp = 0
    for c1, c2 in zip(conll1, conll2):
        val1 = getattr(c1, col)  # TODO: Mivel nincs default megadva lehetne c1.col is! Az olvashatóbb!
        val2 = getattr(c2, col)
        if val1 != 'DUMMY' and val2 != 'DUMMY':
            if val1 == val2:
                tp += 1
            total += 1

    return tp / total


def main():
    conll1 = read_file(sys.argv[1])
    conll2 = read_file(sys.argv[2])

    orig_token_1 = len(conll1)
    orig_token_2 = len(conll2)

    delta = diff_texts(conll1, conll2)

    plus, minus = align(delta, conll1, conll2)

    print('eltero tokenizalas')
    print('eredeti tokenszam file1: ', orig_token_1)
    print('eredeti tokenszam file2: ', orig_token_2)
    print('csak a file1-ben elofordulo tokenek: ', minus)
    print('csak a file2-ben elofordulo tokenek: ', plus)
    print('file1 elterese a file2-tol: ', "{:.2%}".format(minus/orig_token_1))
    print('file2 elterese a file1-tol: ', "{:.2%}".format(plus/orig_token_2))

    print('lemma accuracy: ', "{:.2%}".format(diff_inline(conll1, conll2, 'lemma')))
    print('upos accuracy: ', "{:.2%}".format(diff_inline(conll1, conll2, 'upos')))
    print('xpos accuracy: ', "{:.2%}".format(diff_inline(conll1, conll2, 'xpos')))
    print('feats accuracy: ', "{:.2%}".format(diff_inline(conll1, conll2, 'feats')))


if __name__ == '__main__':
    main()
