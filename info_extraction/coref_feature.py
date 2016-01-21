def m1_noun_type(pair):
    try:
        pos = pair.m1_sent.parse.pos()[pair.m1.span[1] - 1][1]
    except IndexError:
        return
    if pos in ['NN', 'NNS']:
        return 'common'
    elif pos in ['NNP', 'NNPS']:
        return 'proper'
    elif pos in ['PRP', 'PRP$']:
        return 'pro'

def m1_entity_index(pair):
    return str(pair.m1_sent.ems.index(pair.m1))

def m1_is_first(pair):
    index = pair.m1_sent.ems.index(pair.m1)
    if index == 0:
        return 'true'

def m1_is_last(pair):
    index = pair.m1_sent.ems.index(pair.m1)
    if index == len(pair.m1_sent.ems) - 1:
        return 'true'

def m1_is_subject(pair):
    tree = pair.m1_sent.parse
    try:
        posi = list(tree.treeposition_spanning_leaves(pair.m1.span[0], pair.m1.span[1]))
    except IndexError:
        return
    posi.pop()
    while len(posi) > 0:
        if tree[posi].node[0] == 'V':
            return
        posi.pop()
    return 'true'

def m1_is_object(pair):
    tree = pair.m1_sent.parse
    try:
        posi = list(tree.treeposition_spanning_leaves(pair.m1.span[0], pair.m1.span[1]))
    except IndexError:
        return
    posi.pop()
    while len(posi) > 0:
        if tree[posi].node[0] == 'V':
            return 'true'
        posi.pop()

def m1_entity_type(pair):
    return pair.m1.type

def m2_noun_type(pair):
    try:
        pos = pair.m2_sent.parse.pos()[pair.m2.span[1] - 1][1]
    except IndexError:
        return
    if pos in ['NN', 'NNS']:
        return 'common'
    elif pos in ['NNP', 'NNPS']:
        return 'proper'
    elif pos in ['PRP', 'PRP$']:
        return 'pro'

def m2_entity_index(pair):
    return str(pair.m2_sent.ems.index(pair.m2))

def m2_is_first(pair):
    index = pair.m2_sent.ems.index(pair.m2)
    if index == 0:
        return 'true'

def m2_is_last(pair):
    index = pair.m2_sent.ems.index(pair.m2)
    if index == len(pair.m2_sent.ems) - 1:
        return 'true'

def m2_is_subject(pair):
    tree = pair.m2_sent.parse
    try:
        posi = list(tree.treeposition_spanning_leaves(pair.m2.span[0], pair.m2.span[1]))
    except IndexError:
        return
    posi.pop()
    while len(posi) > 0:
        if tree[posi].node[0] == 'V':
            return
        posi.pop()
    return 'true'

def m2_is_object(pair):
    tree = pair.m2_sent.parse
    try:
        posi = list(tree.treeposition_spanning_leaves(pair.m2.span[0], pair.m2.span[1]))
    except IndexError:
        return
    posi.pop()
    while len(posi) > 0:
        if tree[posi].node[0] == 'V':
            return 'true'
        posi.pop()

def m2_entity_type(pair):
    return pair.m2.type

def str_match(pair):
    if pair.m1.form.lower() == pair.m2.form.lower():
        return 'true'

def alias(pair):
    m1a = ''
    for t in pair.m1.form.split('_'):
        m1a += t[0]
    if m1a.lower() == pair.m2.form.lower():
        return 'true'
    m2a = ''
    for t in pair.m2.form.split('_'):
        m2a += t[0]
    if m2a.lower() == pair.m1.form.lower():
        return 'true'

def appositive(pair):
    tree1 = pair.m1_sent.parse
    tree2 = pair.m2_sent.parse
    if tree1 != tree2:
        return
    #m1p = list(tree1.treeposition_spanning_leaves(pair.m1.span[0], pair.m1.span[1]))
    #m2p = list(tree2.treeposition_spanning_leaves(pair.m2.span[0], pair.m2.span[1]))
    # fixme

def same_sent(pair):
    if pair.m1_sent == pair.m2_sent:
        return 'true'

feats = [m1_noun_type, m2_noun_type,
        m1_entity_index, m2_entity_index, 
        m1_is_first, m2_is_first, 
        m1_is_last, m2_is_last, 
        m1_is_subject, m2_is_subject, 
        m1_is_object, m2_is_object, 
        m1_entity_type, m2_entity_type, 
        str_match, 
        alias, 
        appositive, 
        same_sent]
