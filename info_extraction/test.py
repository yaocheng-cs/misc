import os
#from ie import coref, coref_feature
from ie import relation

os.chdir('/Users/yaocheng/Desktop/Information_Extraction/proj4')
#os.chdir('/Users/yaocheng/Desktop/Information_Extraction/proj4/hi')

#pairs = coref.load_pair('coref-trainset.gold', 'parsed-files')
#coref.generate_feature_file(pairs, coref_feature.feats, 'coref-trainset-features.txt')

def train():
    print 'Training...'
    trainset = relation.load_relation('rel-trainset.gold', 'parsed-files')
    for label in relation.LABELS:
        print label
        relation.generate_svmtk_file('train', label, trainset)
        relation.call_svm_light_tk('learn', 'train.' + label + '.txt', label + '.model')

def test():
    print 'Testing...'
    devset = relation.load_relation('rel-testset.gold', 'parsed-files')
    for label in relation.LABELS:
        print label
        relation.generate_svmtk_file('test', label, devset)
        relation.call_svm_light_tk('classify', 'test.' + label + '.txt', label + '.model')

"""
def train2():
    print 'Training...'
    trainset = relation.load_relation('../rel-trainset.gold', '../parsed-files')
    relation.generate_svmtk_file2(trainset, 'train.no_rel.txt', 'multi_labels.txt')
    relation.call_svm_light_tk('learn', 'train.no_rel.txt', 'no_rel.model')
    for label in relation.LABELS:
        with open('multi_labels.txt', 'r') as in_fp:
            with open('trian.' + label + '.txt', 'w') as out_fp:
                for line in in_fp:
                    line = line.split('\t')
                    if line[0] == label:
                        line[0] = '+1'
                    else:
                        line[0] = '-1'
                    line = ' '.join(line)
                    out_fp.write(line)
        relation.call_svm_light_tk('learn', 'train.' + label + '.txt', label + '.model')

def test2():
    print 'Testing...'
    devset = relation.load_relation('../rel-devset.gold', '../parsed-files')
    relation.generate_svmtk_file('dev', 'no_rel', devset, 'dev.no_rel.txt')
    relation.call_svm_light_tk('classify', 'dev.no_rel.txt', 'no_rel.model')
    with open('dev.no_rel.txt.output', 'r') as in_fp:
        with open('dev.no_rel.labeled', 'w') as out_fp:
            line_num = []
            counter = 0
            for line in in_fp:
                margin = float(line.strip())
                if margin > 0:
                    out_fp.write('+1 \n')
                else:
                    out_fp.write('-1 \n')
                    line_num.append(counter)
                counter += 1
"""


#train()
#test()
relation.combine_result('test', relation.LABELS, 'rel-testset.labeled')