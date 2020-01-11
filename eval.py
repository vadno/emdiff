import nltk.chunk
import nltk.parse.evaluate
import nltk.chunk.util

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
            elif line[0][column[0]] != line[1][column[1]]:
                pass
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
                print(line[0][column[0]])


def process_sentence(sent, head, deprel):

    # Percentage of words that get the correct head and label
    # LAS
    # Percentage of words that get the correct head
    # UAS

    corr = 0
    corrl = 0
    total = 0

    # TODO 0 hosszú mondatokra (mondatzáró)
    # TODO kitesztelni a függőségit!

    for line in sent:
        total += 1
        if line[0][head[0]] == line[1][head[1]]:
            corr += 1
            if line[0][deprel[0]] == line[1][deprel[1]]:
                corrl += 1

    print('LAS: ', str(corrl/total))
    print('UAS: ', str(corr/total))


def diff_deps(delta, column, head, deprel):
    """
    kiértékeli a függőségi elemzést
    :param delta:
    :param column:
    :param head:
    :param deprel:
    :return:
    """
    #
    # for line in delta:
    #     print(line[0][column[0]], line[1][column[1]])
    #     print(line[0][head[0]], line[1][head[1]])
    #     print(line[0][deprel[0]], line[1][deprel[1]])

    sent = list()
    tokenerror = False

    for line in delta:

        if 'newsent' not in line[0]:

            # TODO kivenni a nem egyformán tokenizált mondatokat
            if line[0] == '+' or line[1] == '-':
                tokenerror = True

            if line[0] != '+' and line[1] != '-':
                sent.append(line)

        elif 'newsent' in line[0]:
            process_sentence(sent, head, deprel)
            tokenerror = False
            sent = list()

    if sent:
        process_sentence(sent, head, deprel)