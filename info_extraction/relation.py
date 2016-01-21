import os
import sys
import itertools
from nltk.tree import Tree
from collections import defaultdict

def load_parse_doc(parse_path):
    parse_path = os.path.abspath(parse_path)
    parses = []
    with open(parse_path, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line == '':
                continue
            parse = Tree.parse(line)
            parses.append(parse)
    return parses

def get_all_rel_type(gold_path):
    rel_types = set([])
    ne_types = set([])
    within_num = 0
    between_num = 0
    singl_num = 0
    multi_num = 0
    with open(gold_path, 'r') as fp:
        for line in fp:
            attrs = line.strip().split()
            rel_types.add(attrs[0])
            ne_types.add(attrs[5])
            ne_types.add(attrs[11])
            if int(attrs[2]) == int(attrs[8]):
                within_num += 1
            else:
                between_num += 1
            if int(attrs[4]) - int(attrs[3]) > 1 or int(attrs[10]) - int(attrs[9]) > 1:
                multi_num += 1
            else:
                singl_num += 1
    print within_num, between_num, singl_num, multi_num
    print rel_types, len(rel_types)
    print ne_types, len(ne_types)
    return rel_types

class Entity(object):
    """docstring for Entity"""
    def __init__(self):
        super(Entity, self).__init__()
        self.form = None
        self.ne_type = None
        self.span = None
        self.coref_id = None

class Relation(object):
    """docstring for Relation"""

    def __init__(self):
        super(Relation, self).__init__()
        self.doc_id = None
        self.e1 = None
        self.e2 = None
        self.sent_num = None
        self.sent_parse = None
        self.label = None
        
def load_relation(relation_path, parse_doc_folder):
    relation_path = os.path.abspath(relation_path)
    es = defaultdict(Entity)
    relations = []
    current_doc_id = None
    current_doc_parse = None
    with open(relation_path, 'r') as in_fp:
        for line in in_fp:
            attrs = line.strip().split()
            rel = Relation()
            if len(attrs) == 14:
                rel.label = attrs.pop(0)
            rel.doc_id = attrs[0]
            rel.sent_num = int(attrs[1])
            e1_id = '_'.join([rel.doc_id, attrs[1], attrs[2], attrs[3]])
            #if e1_id not in es:
            #    es[e1_id] = Entity()
            rel.e1 = es[e1_id]
            rel.e1.span = (int(attrs[2]), int(attrs[3]))
            rel.e1.ne_type = attrs[4]
            rel.e1.coref_id = attrs[5]
            rel.e1.form = attrs[6]
            e2_id = '_'.join([rel.doc_id, attrs[7], attrs[8], attrs[9]])
            #if e2_id not in es:
            #    es[e2_id] = Entity()
            rel.e2 = es[e2_id]
            rel.e2.span = (int(attrs[8]), int(attrs[9]))
            rel.e2.ne_type = attrs[10]
            rel.e2.coref_id = attrs[11]
            rel.e2.form = attrs[12]

            if current_doc_id != rel.doc_id:
                current_doc_id = rel.doc_id
                current_doc_parse = load_parse_doc(os.path.join(parse_doc_folder, rel.doc_id + '.head.rel.tokenized.raw.parse'))
            #try:
            rel.sent_parse = current_doc_parse[rel.sent_num]
            #except IndexError:
            #    continue
            relations.append(rel)
    return relations

LABELS =   ['ART.Inventor-or-Manufacturer', 'ART.Other.reverse', 'ART.User-or-Owner', 'ART.User-or-Owner.reverse', 
            'DISC.UNDEF', 'DISC.UNDEF.reverse', 
            'EMP-ORG.Employ-Executive', 'EMP-ORG.Employ-Executive.reverse', 'EMP-ORG.Employ-Staff', 'EMP-ORG.Employ-Staff.reverse', 'EMP-ORG.Employ-Undetermined', 'EMP-ORG.Employ-Undetermined.reverse', 
            'EMP-ORG.Member-of-Group', 'EMP-ORG.Member-of-Group.reverse', 'EMP-ORG.Other', 'EMP-ORG.Other.reverse', 'EMP-ORG.Partner', 'EMP-ORG.Partner.reverse', 'EMP-ORG.Subsidiary', 'EMP-ORG.Subsidiary.reverse', 
            'GPE-AFF.Based-In', 'GPE-AFF.Based-In.reverse', 'GPE-AFF.Citizen-or-Resident', 'GPE-AFF.Citizen-or-Resident.reverse', 'GPE-AFF.Other', 'GPE-AFF.Other.reverse', 'OTHER-AFF.Ethnic.reverse', 
            'OTHER-AFF.Ideology', 'OTHER-AFF.Ideology.reverse', 'OTHER-AFF.Other', 'OTHER-AFF.Other.reverse', 
            'PER-SOC.Business', 'PER-SOC.Business.reverse', 'PER-SOC.Family', 'PER-SOC.Family.reverse', 'PER-SOC.Other', 'PER-SOC.Other.reverse', 
            'PHYS.Located', 'PHYS.Located.reverse', 'PHYS.Near', 'PHYS.Near.reverse', 'PHYS.Part-Whole', 'PHYS.Part-Whole.reverse', 
            'no_rel']

NE_TYPES = ['LOC', 'WEA', 'GPE', 'PER', 'FAC', 'ORG', 'VEH']
NE_TYPE_PAIRS = list(itertools.product(NE_TYPES, repeat=2))

def get_path_enclosed_tree(i, j, tree):
    # "lca" stands for "least common ancestor"
    # using treeposition_spanning_leaves(self, start, end) is like accessing list[start:end],
    # it tries to find the subtree that at least cover tokens (leaves) whose indices range from "start" to "end - 1"
    lca = tree[tree.treeposition_spanning_leaves(i, j + 1)].copy(deep=True)
    i_lca_pos = lca.leaf_treeposition(lca.leaves().index(tree.leaves()[i]))
    pos = list(i_lca_pos)
    while pos != []:
        if pos[-1] > 0:
            counter = pos[-1]
            temp = pos[:-1]
            temp.append(0)
            while counter > 0:
                del lca[temp]
                counter -= 1
        pos.pop()
    j_lca_pos = lca.leaf_treeposition(lca.leaves().index(tree.leaves()[j]))
    pos = list(j_lca_pos)
    while pos != []:
        pos[-1] += 1
        while True:
            try:
                del lca[pos]
            except IndexError:
                break
        pos.pop()
    return lca

def generate_svmtk_file(prefix, label, relations, output_path=None):
    if not output_path:
        output_path = prefix + '.' + label + '.txt'
        print output_path
    with open(output_path, 'w') as fp:
        for rel in relations:
            if rel.label == label:
                target_part = '+1'
            else:
                target_part = '-1'
            i = rel.e1.span[0]
            j = rel.e2.span[-1] - 1
            pe_tree = get_path_enclosed_tree(i, j, rel.sent_parse)
            #tree_part = ' '.join(['|BT|', ' '.join(str(pe_tree).replace('\n', ' ').split()), '|ET|'])
            tree_part = ' '.join(['|BT|', pe_tree.pprint(margin=sys.maxint), '|ET|'])
            vector_part = ' '.join(['1:' + str(NE_TYPE_PAIRS.index((rel.e1.ne_type, rel.e2.ne_type))),
                                    '2:' + str(1 if rel.e1.coref_id.split('-')[0] == rel.e2.coref_id.split('-')[0] else 0),
                                    '|EV|'])
            line = ' '.join([target_part, tree_part, vector_part]) + '\n'
            fp.write(line)

def generate_svmtk_file2(relations, binary_path, multi_path):
    with open(binary_path, 'w') as fp1:
        with open(multi_path, 'w') as fp2:
            for rel in relations:
                if rel.label == 'no_rel':
                    target_part = '+1'
                else:
                    target_part = '-1'
                    multi_target = rel.label
                pe_tree = get_path_enclosed_tree(rel.e1.span[0], rel.e2.span[1] - 1, rel.sent_parse)
                #tree_part = ' '.join(['|BT|', ' '.join(str(pe_tree).replace('\n', ' ').split()), '|ET|'])
                tree_part = ' '.join(['|BT|', pe_tree.pprint(margin=sys.maxint), '|ET|'])
                vector_part = ' '.join(['1:' + str(NE_TYPE_PAIRS.index((rel.e1.ne_type, rel.e2.ne_type))),
                                        '2:' + str(1 if rel.e1.coref_id.split('-')[0] == rel.e2.coref_id.split('-')[0] else 0),
                                        '|EV|'])
                line1 = ' '.join([target_part, tree_part, vector_part]) + '\n'
                fp1.write(line1)
                if target_part == '-1':
                    line2 = multi_target + '\t' + ' '.join([tree_part, vector_part]) + '\n'
                    fp2.write(line2)

def call_svm_light_tk(cmd_type, feat_path, model_path):
    feat_path = os.path.abspath(feat_path)
    model_path = os.path.abspath(model_path)
    cmd = ''
    if cmd_type == 'learn':
        cmd = '/Users/yaocheng/Packages/site-packages/svm-light-TK/svm-light-TK-1.2.1/svm_learn -t 5 -C + %(feat)s %(model)s' % \
                {'feat': feat_path, 'model': model_path}
    if cmd_type == 'classify':
        cmd = '/Users/yaocheng/Packages/site-packages/svm-light-TK/svm-light-TK-1.2.1/svm_classify %(feat)s %(model)s %(output)s' % \
                {'feat': feat_path, 'model': model_path, 'output': feat_path + '.output'}
    os.system(cmd)

def combine_result(prefix, labels, output_path):
    print labels
    with open(output_path, 'w') as out_fp:
        fps = [open(prefix + '.' + label + '.txt.output', 'r') for label in labels]
        results = zip(*[fp.readlines() for fp in fps])
        for res in results:
            res = [float(r.strip()) for r in res]
            temp = sorted(res[:])
            #print temp
            m = temp[-1]
            m2 = temp[-2]
            i = res.index(m)
            i2 = res.index(m2)
            if labels[i] == 'no_rel':
                if m < 0.72:
                    out_fp.write(' '.join([labels[i2], str(m2)]) + '\n')
                    continue
            out_fp.write(' '.join([labels[i], str(m)]) + '\n')







