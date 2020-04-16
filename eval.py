#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn import metrics
from nltk.metrics import ConfusionMatrix


def measures(tp, fp, fn, weight):

    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = weight * (prec * rec / (prec + rec))

    return prec, rec, f1


def eval_tags_bytag(delta, column):

    gold = list()
    test = list()

    for col1, col2 in delta:
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            gold.append(col1[column[0]])
            test.append(col2[column[1]])

    return metrics.classification_report(gold, test)


def confusion(delta, column):

    gold = list()
    test = list()
    for col1, col2 in delta:
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            gold.append(col1[column[0]])
            test.append(col2[column[1]])

    cm = ConfusionMatrix(gold, test)
    return cm


def eval_tags(delta, column):
    """
    :param delta:
    :param column:
    :return:
    """
    total = 0
    tp = 0

    for col1, col2 in delta:
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            tp += int(col1[column[0]] == col2[column[1]])
            total += 1

    return tp/total     # accuracy = num_tokens_correct / total_num_tokens_from_gold


def eval_chunks(delta, column):
    """
    emNer címkék:
        B begin
        E end
        I in
        1 egyelemű
        O out
        -
        PER person
        ORG organization
        LOC
        MISC

    emChunk címkék:
        B-NP begin
        E-NP end
        I-NP in
        1-NP egyelemű
        O-NP out

    chunker-evaluation: IOB-accuracy, prec, rec, f1

    accuracy: the total number of tokens (NOT CHUNKS!!) that are guessed correctly with the POS tags and IOB tags,
    then divided by the total number of tokens in the gold sentence
    accuracy = num_tokens_correct / total_num_tokens_from_gold

    TP: the number of chunks (NOT TOKENS!!!) that are guessed correctly
    FP: the number of chunks (NOT TOKENS!!!) that are guessed but they are wrong
    TN: the number of chunks (NOT TOKENS!!!) that are not guessed by the system
    prec = tp / fp + tp
    rec = tp / fn + tp
    f1 = 2 * (prec * rec / (prec + rec))

    :param delta:
    :param column:
    :return:
    """

    # meroszamok
    total_tok = 0
    tp_tok = 0
    # azert listak, hogy tipusonkent is meg lehessen szamolni a NER-t
    tp_chunk = list()
    fn_chunk = list()
    fp_chunk = list()
    # lepteto a tobbelemu chunkokhoz
    further = False

    for col1, col2 in delta:
        # csak az egyforma tokenizalasu sorokat nezzuk
        if col1 != '+' and col2 != '-' and 'newsent' not in col1:
            total_tok += 1
            # egyforma cimke tokenenkent az accuracy-hoz
            tp_tok += int(col1[column[0]] == col2[column[1]])

            # egyelemu chunkok
            if col1[column[0]].startswith('1-') and col2[column[1]].startswith('1-'):
                tp_chunk.append(col1[column[0]].split('-')[1])
            elif col1[column[0]].startswith('1-') and not col2[column[1]].startswith('1-'):
                fn_chunk.append(col1[column[0]].split('-')[1])
            elif not col1[column[0]].startswith('1-') and col2[column[1]].startswith('1-'):
                fp_chunk.append(col2[column[1]].split('-')[1])

            # tobbelemu chunkok eleje
            elif col1[column[0]].startswith('B-') and col2[column[1]].startswith('B-'):
                further = True
            elif col1[column[0]].startswith('B-') and not col2[column[1]].startswith('B-'):
                fn_chunk.append(col1[column[0]].split('-')[1])

            # tobbelemu chunkok kozepe
            elif col1[column[0]].startswith('I-') and col2[column[1]].startswith('I-') and further:
                further = True
            elif col1[column[0]].startswith('I-') and not col2[column[1]].startswith('I-'):
                fn_chunk.append(col1[column[0]].split('-')[1])

            # tobbelemu chunkok vege
            elif col1[column[0]].startswith('E-') and col2[column[1]].startswith('E-') and further:
                further = False
                tp_chunk.append(col1[column[0]].split('-')[1])
            elif col1[column[0]].startswith('E-') and not col2[column[1]].startswith('E-') and further:
                further = False
                fp_chunk.append(col1[column[0]].split('-')[1])
            elif not col1[column[0]].startswith('E-') and col2[column[1]].startswith('E-') and further:
                fn_chunk.append(col1[column[0]].split('-')[1])
                further = False

    prec = None
    rec = None
    f1 = None

    acc = tp_tok/total_tok

    if tp_chunk:
        prec, rec, f1 = measures(len(tp_chunk), len(fp_chunk), len(fn_chunk), 2)

    return acc, prec, rec, f1


def process_sentence(sent, head, deprel):
    """
    LAS: Percentage of words that get the correct head and label
    UAS: Percentage of words that get the correct head

    :param sent:
    :param head:
    :param deprel:
    :return:
    """

    corr = 0
    corrl = 0
    total = 0

    for col1, col2 in sent:
        if 'newsent' not in col1:
            total += 1
            if col1[head[0]] == col2[head[1]]:
                corr += 1
                corrl += int(col1[deprel[0]] == col2[deprel[1]])

    return corrl / total, corr / total


def eval_deps(delta, head, deprel):
    """
    kiértékeli a függőségi elemzést
    :param delta:
    :param head:
    :param deprel:
    :return:
    """

    sent = list()
    las = None
    uas = None

    for col1, col2 in delta:
        if 'newsent' not in col1 and col1 != '+' and col2 != '-':
            sent.append([col1, col2])

        elif 'newsent' in col1:
            las, uas = process_sentence(sent, head, deprel)
            sent = list()

    if sent:
        las, uas = process_sentence(sent, head, deprel)

    return las, uas


def iszero(dep_id):

    return '.' in dep_id and dep_id.split('.')[1] in ('SUBJ', 'OBJ', 'POSS')


def get_dep_type(dep_id):

    return dep_id.split('.')[1]


def eval_zero(delta, column):

    tp = 0
    fp = 0
    fn = 0
    fp_hits = list()
    fn_hits = list()

    for col1, col2 in delta:
        if 'newsent' not in col1:
            if col1 != '+' and col2 != '-':
                if iszero(col1[column[0]]) and iszero(col2[column[1]]):
                    gold_type = get_dep_type(col1[column[0]])
                    test_type = get_dep_type(col2[column[1]])
                    tp += int(gold_type and test_type and gold_type == test_type)
            elif col1 == '+' and iszero(col2[column[1]]):
                fp += 1
                fp_hits.append([col1, col2])
            elif col2 == '-' and iszero(col1[column[0]]):
                fn += 1
                fn_hits.append([col1, col2])

    prec = None
    rec = None
    f1 = None

    if tp:
        prec, rec, f1 = measures(tp, fp, fn, 2)

    return prec, rec, f1
