#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import namedtuple


def read_file(filename):

    new_sent = list(' ' * 10)
    conll_line = namedtuple('CoNLL', 'id, form, lemma, upos, xpos, feats, head, deprel, deps, misc')

    lines = list()

    with open(filename, 'r') as inf:
        for line in inf:
            if not line.startswith('#'):
                new_line = line.split()
                if not new_line:
                    add_line = conll_line._make(new_sent)
                else:
                    add_line = conll_line._make(new_line)
                lines.append(add_line)

    return lines


def diff_inline(conll1, conll2, col):

    tp = 0

    if len(conll1) != len(conll2):
        print('eltérő tokenizálás')
    else:
        for c1, c2 in zip(conll1, conll2):
            val1 = getattr(c1, col)
            val2 = getattr(c2, col)
            if val1 == val2:
                tp += 1

    print(tp)
    print((tp / len(conll1)) * 100)


def main():
    conll1 = read_file(sys.argv[1])
    conll2 = read_file(sys.argv[2])

    diff_inline(conll1, conll2, 'id')
    diff_inline(conll1, conll2, 'form')
    diff_inline(conll1, conll2, 'lemma')
    diff_inline(conll1, conll2, 'upos')
    diff_inline(conll1, conll2, 'xpos')
    diff_inline(conll1, conll2, 'feats')


if __name__ == "__main__":
    main()
