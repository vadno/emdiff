#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def iszero(dep_id):

    if '.' in dep_id and dep_id.split('.')[1] in ('SUBJ', 'OBJ', 'POSS'):
        return True


def get_dep_type(dep_id):

    return dep_id.split('.')[1]


def eval_zero(delta, column):

    tp = 0
    fp = 0
    fn = 0
    fp_hits = list()
    fn_hits = list()

    for line in delta:
        if line[0] != '+' and line[1] != '-':
            if iszero(line[0][column[0]]) and iszero(line[1][column[1]]):
                gold_type = get_dep_type(line[0][column[0]])
                sys_type = get_dep_type(line[1][column[1]])
                if gold_type and sys_type and gold_type == sys_type:
                    tp += 1
        elif line[0] == '+' and iszero(line[1][column[1]]):
            fp += 1
            fp_hits.append(line)
        elif line[1] == '-' and iszero(line[0][column[0]]):
            fn += 1
            fn_hits.append(line)

    prec = None
    rec = None
    f1 = None

    print(tp, fp, fn)

    if tp:
        prec = tp/(tp+fp)
        rec = tp/(tp+fn)
        f1 = 2*(prec*rec/(prec+rec))

    return prec, rec, f1
