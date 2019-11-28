import nltk.chunk
import nltk.parse.evaluate


def diff_tags(delta, column):
    """
    lemma
    xpostag
    upostag
    feats

    :param delta:
    :param column:
    :return:
    """
    total = 0
    tp = 0

    for line in delta:
        if line[0] != '+' and line[1] != '-':
            if line[0][column[0]] == line[1][column[1]]:
                tp += 1
            total += 1

    print('accuracy: {0:.2%}'.format(tp/total))


def diff_chunks(delta, column):
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
    :param delta:
    :param column:
    :return:
    """

    for line in delta:
        if line[0] != '+' and line[1] != '-':
            if line[0][column[0]] == line[1][column[1]]:
                pass


def diff_deps(delta, column, head, deprel):
    """
    kiértékeli a függőségi elemzést
    :param delta:
    :param column:
    :param head:
    :param deprel:
    :return:
    """

    # for line in delta:
    #     print(line[0][column[0]], line[1][column[1]])
    #     print(line[0][head[0]], line[1][head[1]])
    #     print(line[0][deprel[0]], line[1][deprel[1]])

