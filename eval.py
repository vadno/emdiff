from sklearn import metrics


def eval_tags_bytag(delta, column):

    gold = list()
    pred = list()

    for line in delta:
        if line[0] != '+' and line[1] != '-':
            gold.append(line[0][column[0]])
            pred.append(line[1][column[1]])

    print(metrics.classification_report(gold, pred))


def eval_tags(delta, column):
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

    # accuracy = num_tokens_correct / total_num_tokens_from_gold
    return tp/total


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
    reca = tp / fn + tp
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

    for line in delta:
        # csak az egyforma tokenizalasu sorokat nezzuk
        if line[0] != '+' and line[1] != '-':
            total_tok += 1
            # egyforma cimke tokenenkent az accuracy-hoz
            if line[0][column[0]] == line[1][column[1]]:
                tp_tok += 1

            # egyelemu chunkok
            if line[0][column[0]].startswith('1-') and line[1][column[1]].startswith('1-'):
                tp_chunk.append(line[0][column[0]].split('-')[1])
            elif line[0][column[0]].startswith('1-') and not line[1][column[1]].startswith('1-'):
                fn_chunk.append(line[0][column[0]].split('-')[1])
            elif not line[0][column[0]].startswith('1-') and line[1][column[1]].startswith('1-'):
                fp_chunk.append(line[1][column[1]].split('-')[1])

            # tobbelemu chunkok eleje
            elif line[0][column[0]].startswith('B-') and line[1][column[1]].startswith('B-'):
                further = True
            elif line[0][column[0]].startswith('B-') and not line[1][column[1]].startswith('B-'):
                fn_chunk.append(line[0][column[0]].split('-')[1])

            # tobbelemu chunkok kozepe
            elif line[0][column[0]].startswith('I-') and line[1][column[1]].startswith('I-') and further:
                further = True
            elif line[0][column[0]].startswith('I-') and not line[1][column[1]].startswith('I-'):
                fn_chunk.append(line[0][column[0]].split('-')[1])

            # tobbelemu chunkok vege
            elif line[0][column[0]].startswith('E-') and line[1][column[1]].startswith('E-') and further:
                further = False
                tp_chunk.append(line[0][column[0]].split('-')[1])
            elif line[0][column[0]].startswith('E-') and not line[1][column[1]].startswith('E-') and further:
                further = False
                fp_chunk.append(line[0][column[0]].split('-')[1])
            elif not line[0][column[0]].startswith('E-') and line[1][column[1]].startswith('E-') and further:
                fn_chunk.append(line[0][column[0]].split('-')[1])
                further = False

    prec = None
    rec = None
    f1 = None

    acc = tp_tok/total_tok

    if tp_chunk:
        prec = len(tp_chunk) / (len(fp_chunk) + len(tp_chunk))
        rec = len(tp_chunk) / (len(fn_chunk) + len(tp_chunk))
        f1 = 2 * (prec * rec / (prec + rec))

    return acc, prec, rec, f1


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

    return corrl / total, corr / total


def eval_deps(delta, column, head, deprel):
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
        las, uas = process_sentence(sent, head, deprel)

    return las, uas
