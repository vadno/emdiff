#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nltk.metrics.agreement import AnnotationTask   # https://www.nltk.org/_modules/nltk/metrics/agreement.html


def reverse_tags(delta, column):
    """
    a megfelelő formátumra hozza az annotált adatot, ami:
    az annotálandó elemek listája, ahol az egyes elemek
    háromelemű listák, ahol
        az első elem az annotátor azonosítója
        a második elem a szóalak (ennek egyeznie kell, ezért a gold szóalakját vesszük)
        a harmadik elem a címke
    :param delta: az összevetett adat
    :param column: az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """

    by_tokens = list()
    for col1, col2 in delta:
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            by_tokens.append(['g', col1[0], col1[column[0]]])
            by_tokens.append(['s', col2[0], col2[column[1]]])

    return by_tokens


def reverse_deps(delta, head, deprel):
    """

    :param delta:
    :param head:
    :param deprel:
    :return:
    """

    by_deps = list()
    for col1, col2 in delta:
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            by_deps.append(((col1[head[0]], col1[deprel[0]]), (col2[head[1]], col2[deprel[1]])))

    return by_deps


def agree_dep(delta, head, deprel):
    """

    :param delta:
    :param head:
    :param deprel:
    :return:
    """

    by_dep = reverse_deps(delta, head, deprel)

    ua = 0  # unlabeled attachment
    la = 0  # labeled attachment
    lo = 0  # label only
    total = 0

    for dep in by_dep:
        total += 1
        la += int(dep[0] == dep[1])
        ua += int(dep[0][0] == dep[1][0])
        lo += int(dep[0][1] == dep[1][1])

    return ua / total, la / total, lo / total


def agree_tags(delta, column):
    """
    egytokenes címkézési feladatokra számol egyetértést
    :param delta:  az összevetett adat
    :param column:  az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """
    by_field = reverse_tags(delta, column)

    task = AnnotationTask(data=by_field)

    oa = task.avg_Ao()      # observed agreement
    s = task.S()            # Bennett, Albert and Goldstein S (1954) all categories are equally likely
    pi = task.pi()          # Scott pi (1955) single distribution
    kappa = task.kappa()    # Cohen kappa (1960) individual coder distribution
    w_kappa = task.weighted_kappa()
    alpha = task.alpha()    # Krippendorff alpha (1980)

    return oa, s, pi, kappa, w_kappa, alpha
