#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from itertools import repeat
from operator import itemgetter
from collections import namedtuple
from difflib import SequenceMatcher  # difflib: https://pymotw.com/2/difflib/
from enum import Enum


class CoNLLDiff:
    """
    Diff and evaulate two CoNLL-U formatted inputs with similar API to Python's difflib.SequenceMatcher()
    """
    conll_line = namedtuple('CoNLL', 'id, form, lemma, upos, xpos, feats, head, deprel, deps, misc')
    extremal = Enum('Extremal', 'SENT_SEP DUMMY')  # Non-conll_line type elements

    def __init__(self, a=None, b=None):
        self.a = self.b = None
        self.plus = self.minus = 0
        self._orig_token1 = self._orig_token2 = 0
        self.aligned_a = self.aligned_b = []
        self.matching_blocks = self.opcodes = None
        self._ratio = None
        self.set_seqs(a, b)

    def set_seqs(self, a, b):
        """Set the two sequences to be compared."""

        self.set_seq1(a)
        self.set_seq2(b)

    def set_seq1(self, a):
        """Set the first sequence to be compared."""

        if a is self.a:
            return
        if isinstance(a, list):
            self.a = a
        elif isinstance(a, str):
            self.a = self._read_file(a)
        else:
            raise TypeError('Input A must be a prepared list or filename got {0}!'.format(type(a)))
        self.matching_blocks = self.opcodes = None
        self._orig_token1 = len(self.a)

    def set_seq2(self, b):
        """Set the second sequence to be compared."""

        if b is self.b:
            return
        if isinstance(b, list):
            self.b = b
        elif isinstance(b, str):
            self.b = self._read_file(b)
        else:
            raise TypeError('Input B must be a prepared list or filename got {0}!'.format(type(b)))
        self.matching_blocks = self.opcodes = None
        self._orig_token2 = len(self.b)

    def _read_file(self, filename):
        lines = []

        with open(filename, encoding='UTF-8') as inf:
            for line in inf:
                if not line.startswith('#'):
                    new_line = line.strip().split()
                    if len(new_line) > 0:
                        new_line = self.conll_line._make(new_line)
                    else:
                        new_line = self.extremal.SENT_SEP
                    lines.append(new_line)

        return lines

    def get_matching_blocks(self, alo=0, ahi=None, blo=0, bhi=None):
        if self.matching_blocks is not None:
            return self.matching_blocks

        self.matching_blocks = []
        for tag, i1, i2, j1, j2 in self.get_opcodes(alo, ahi, blo, bhi):
            if tag == 'equal':
                if i1 == i2:
                    i2 += 1
                n = i2 - i1
                self.matching_blocks.append((i1, j1, n))

    def find_longest_match(self, alo=0, ahi=None, blo=0, bhi=None):
        return max((m for m in self.get_matching_blocks(alo, ahi, blo, bhi)), key=lambda x: itemgetter(2))

    def ratio(self):
        if self.opcodes is None:
            self.get_opcodes()
        return self._ratio

    def get_grouped_opcodes(self, n=3, alo=0, ahi=None, blo=0, bhi=None):
        raise NotImplementedError  # TODO implement if reasonable...

    def get_opcodes(self, alo=0, ahi=None, blo=0, bhi=None):
        if self.opcodes is not None:
            return self.opcodes

        conll1_tok = [getattr(line, 'form', line) for line in self.a[alo:ahi]]  # form or SENT_SEP
        conll2_tok = [getattr(line, 'form', line) for line in self.b[blo:bhi]]

        matcher = SequenceMatcher(a=conll1_tok, b=conll2_tok)
        self.opcodes = matcher.get_opcodes()
        self._ratio = matcher.ratio()
        return self.opcodes

    def align(self, alo=0, ahi=None, blo=0, bhi=None):
        self.get_opcodes(alo, ahi, blo, bhi)
        aligned = zip(*self._align_gen(self.a[alo:ahi], self.b[blo:bhi]))  # Align by the opcodes gained on form
        self.aligned_a, self.aligned_b = aligned
        return aligned

    def _align_gen(self, conll1, conll2):
        dummy = self.extremal.DUMMY
        self.plus = 0
        self.minus = 0

        for tag, i1, i2, j1, j2 in self.opcodes:
            if i1 == i2:  # Trick Python ranges...
                i2 += 1
            if j1 == j2:
                j2 += 1
            if tag == 'equal':
                yield from zip(conll1[i1:i2], conll2[j1:j2])
            elif tag == 'insert':  # Insert N piece of DUMMY to the FIRST
                yield from zip(repeat(dummy), conll2[j1:j2])
                self.plus += j2-j1
            elif tag == 'delete':  # Insert N piece of DUMMY to the SECOND
                yield from zip(conll1[i1:i2], repeat(dummy))
                self.minus += i2-i1
            elif tag == 'replace':  # Insert N piece of DUMMY to BOTH
                yield from zip(conll1[i1:i2], repeat(dummy))
                self.minus += i2-i1
                yield from zip(repeat(dummy), conll2[j1:j2])
                self.plus += j2-j1
            else:
                raise TypeError('Something bad happened!')

        return

    def _diff_inline(self, col):
        dummy = self.extremal.DUMMY
        total = 0
        tp = 0
        for c1, c2 in zip(self.aligned_a, self.aligned_b):
            val1 = getattr(c1, col, c1)  # col is dynamically specified (see function parameters)
            val2 = getattr(c2, col, c2)
            if val1 != dummy and val2 != dummy:
                if val1 == val2:
                    tp += 1
                total += 1

        return tp / total

    def print_stats(self, alo=0, ahi=None, blo=0, bhi=None):
        self.align(alo, ahi, blo, bhi)
        len_a = len(self.a[alo:ahi])
        len_b = len(self.b[blo:bhi])
        print('eltero tokenizalas')
        print('eredeti tokenszam file1: ', len_a)
        print('eredeti tokenszam file2: ', len_b)
        print('csak a file1-ben elofordulo tokenek: ', self.minus)
        print('csak a file2-ben elofordulo tokenek: ', self.plus)
        print('file1 elterese a file2-tol: ', "{0:.2%}".format(self.minus / len_a))
        print('file2 elterese a file1-tol: ', "{0:.2%}".format(self.plus / len_b))

        for col in ('lemma', 'upos', 'xpos', 'feats'):
            print('{0} accuracy: {1:.2%}'.format(col, self._diff_inline(col)))


def main():
    cls = CoNLLDiff(sys.argv[1], sys.argv[2])
    cls.print_stats()


if __name__ == '__main__':
    main()
