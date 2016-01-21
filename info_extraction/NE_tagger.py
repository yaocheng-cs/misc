'''
Created on Feb 8, 2013

@author: yaocheng
'''

import os
from project_path import *
from bio2crff import convert
from NE_feature import feats

def learn(train_crff, model):
    os.system(os.path.join(crfsuite_bin, 'crfsuite learn') + \
              ' -m ' + model + \
              ' ' + train_crff)

def tag(test_crff, model, label):
    os.system(os.path.join(crfsuite_bin, 'crfsuite tag') + \
              ' -r ' + \
              ' -m ' + model + \
              ' ' + test_crff + \
              ' 1> ' + label)
    
def combine(test_raw, label, test_tagged):
    try:
        with open(test_raw, 'r') as raw, open(label, 'r') as label, open(test_tagged, 'w') as tagged:
            for x, y in zip(raw, label):
                if x == '\n' and y == '\n':
                    tagged_line = '\n'
                else:
                    tagged_line = x.strip() + '\t' + y.strip().split()[1] + '\n'
                    #tagged_line = x.strip() + '\t' + y.strip() + '\n'
                tagged.write(tagged_line)
    except IOError:
        print 'IOError'
        return
    
def print_mismatch(tagged, missed):
    with open(tagged, 'r') as input, open(missed, 'w') as output:
        for line in input:
            items = line.split()
            try:
                if items[-1] != items[-2]:
                    output.write(line)
            except IndexError:
                continue

def main():
    
    convert(NE_train_gold, NE_train_crff, feats)
    learn(NE_train_crff, NE_model)
    convert(NE_dev_gold, NE_dev_crff, feats)
    tag(NE_dev_crff, NE_model, NE_dev_label)
    combine(NE_dev_raw, NE_dev_label, NE_dev_tagged)
    print_mismatch(NE_dev_tagged, NE_dev_missed)
    
    convert(NE_test_raw, NE_test_crff, feats, labeled=False)
    tag(NE_test_crff, NE_model, NE_test_label)
    combine(NE_test_raw, NE_test_label, NE_test_tagged)
    
if __name__ == '__main__':
    main()