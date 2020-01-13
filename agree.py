from nltk.metrics.agreement import AnnotationTask   # https://www.nltk.org/_modules/nltk/metrics/agreement.html


def coeff(annot_data):
    """
    az nltk.metrics.agreement-ben elérhető egyetértési metrikákkal számol
    :param annot_data: a megfelelő formátumban megkapott adat, ami:
    az annotálandó elemek listája, ahol az egyes elemek
    háromelemű listák, ahol
        az első elem az annotátor azonosítója
        a második elem a szóalak
        a harmadik elem a címke
    :return:
    """
    print(annot_data)

    task = AnnotationTask(data=annot_data)
    print('percentage of agreement, observed agreement')
    print(task.avg_Ao())

    print('chance-corrected coefficients')
    print('Bennett, Albert and Goldstein S (1954)\n(all categories are equally likely): ', task.S())
    print('Scott pi (1955)\n(single distribution): ', task.pi())
    print('Cohen kappa (1960)\n(individual coder distribution): ', task.kappa())
    print('weighted kappa: ', task.weighted_kappa())


def reverse_data(delta, column):
    """
    a megfelelő formátumra hozza az annotált adatot, aminek specifikációja a coeff() függvényben van
    :param delta: az összevetett adat
    :param column: az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """

    by_tokens = list()
    for line in delta:
        if line[0] != '+' and line[1] != '-':
            by_tokens.append(['g', line[0][0], line[0][column[0]]])
            by_tokens.append(['s', line[0][0], line[1][column[1]]])

    return by_tokens


def agree_tags(delta, column):
    """
    egytokenes címkézési feladatokra számol egyetértést
    :param delta:  az összevetett adat
    :param column:  az az oszlop, amelyre egyetértést akarunk számolni
    :return:
    """
    by_field = reverse_data(delta, column)
    coeff(by_field)
