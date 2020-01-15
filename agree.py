from nltk.metrics.agreement import AnnotationTask   # https://www.nltk.org/_modules/nltk/metrics/agreement.html


def reverse_tags(delta, column):
    """
    a megfelelő formátumra hozza az annotált adatot, aminek specifikációja a coeff() függvényben van
    :param delta: az összevetett adat
    :param column: az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """

    by_tokens = list()
    for line in delta:
        if line[0] != '+' and line[1] != '-' and 'newsent' not in line[0]:
            by_tokens.append(['g', line[0][0], line[0][column[0]]])
            by_tokens.append(['s', line[0][0], line[1][column[1]]])

    return by_tokens


def reverse_deps(delta, head, deprel):
    """

    :param delta:
    :param head:
    :param deprel:
    :return:
    """

    by_deps = list()
    for line in delta:
        if line[0] != '+' and line[1] != '-' and 'newsent' not in line[0]:
            by_deps.append(((line[0][head[0]], line[0][deprel[0]]), (line[1][head[1]], line[1][deprel[1]])))

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
        if dep[0] == dep[1]:
            la += 1
        if dep[0][0] == dep[1][0]:
            ua += 1
        if dep[0][1] == dep[1][1]:
            lo += 1

    return ua / total, la / total, lo / total


def agree_tags(delta, column):
    """
    egytokenes címkézési feladatokra számol egyetértést
    :param delta:  az összevetett adat
    :param column:  az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """
    by_field = reverse_tags(delta, column)

    task = AnnotationTask(data=by_field )

    oa = task.avg_Ao()      # observed agreement
    s = task.S()            # Bennett, Albert and Goldstein S (1954) all categories are equally likely
    pi = task.pi()          # Scott pi (1955) single distribution
    kappa = task.kappa()    # Cohen kappa (1960) individual coder distribution
    w_kappa = task.weighted_kappa()
    alpha = task.alpha()    # Krippendorff alpha (1980)

    return oa, s, pi, kappa, w_kappa, alpha
