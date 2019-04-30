#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import namedtuple
import difflib


def read_file(filename):

    new_sent = list(' ' * 10)
    conll_line = namedtuple('CoNLL', 'id, form, lemma, upos, xpos, feats, head, deprel, deps, misc')

    lines = list()

    with open(filename, encoding='UTF-8') as inf:
        for line in inf:
            if not line.startswith('#'):
                new_line = line.strip().split()
                if not new_line:
                    new_line = new_sent
                lines.append(conll_line._make(new_line))

    return lines


def diff_inline(conll1, conll2, col):

    tp = 0

    if len(conll1) != len(conll2):
        print('eltérő tokenizálás')
    else:
        for c1, c2 in zip(conll1, conll2):
            val1 = getattr(c1, col)  # TODO: Mivel nincs default megadva lehetne c1.col is! Az olvashatóbb!
            val2 = getattr(c2, col)
            if val1 == val2:
                tp += 1
            # TODO: Esetleg ez? https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html#sklearn.metrics.precision_recall_fscore_support
    return "{:.2%}".format(tp / len(conll1))


def main():
    conll1 = read_file(sys.argv[1])
    conll2 = read_file(sys.argv[2])

    if diff_inline(conll1, conll2, 'id') != 100:
        print('eltérő id probléma')
    else:
        print('id OK')

    if diff_inline(conll1, conll2, 'form') != 100:
        print('eltérő token probléma')
    else:
        print('tokenek OK')

    print('lemma accuracy: ', diff_inline(conll1, conll2, 'lemma'))
    print('upos accuracy: ', diff_inline(conll1, conll2, 'upos'))
    print('xpos accuracy: ', diff_inline(conll1, conll2, 'xpos'))
    print('feats accuracy: ', diff_inline(conll1, conll2, 'feats'))

    # difflib: https://pymotw.com/2/difflib/

    with open('small1.tsv', 'r') as f1:
        f1_lines = []
        for line in f1:
            if not line.startswith('#'):
                f1_lines.append(line.split('\t')[1])

    with open('small2.tsv', 'r') as f2:
        f2_lines = []
        for line in f2:
            if not line.startswith('#'):
                f2_lines.append(line.split('\t')[1])

    d = difflib.Differ()
    diff = d.compare(f1_lines, f2_lines)
    # delta = ''.join(x[2:] for x in diff if x.startswith('+ '))
    # print(delta)

    print('\n'.join(diff))


if __name__ == '__main__':
    main()
