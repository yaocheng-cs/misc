'''
Created on Mar 18, 2013

@author: yaocheng
'''

import sys
import os
import os.path
#import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
#from nltk.tag import pos_tag
#from nltk.chunk import RegexpParser
#from utility import doc_file


class Product(object):
    
    def __init__(self):
        self.id_ = None
        self.name = None
        
        
class Instance(object):
    
    def __init__(self):
        self.id_ = None
        self.feats = []
        self.label = None
        
        
class Review(Instance):
    
    def __init__(self):
        super(Review, self).__init__()
        self.product = None


def to_arff(insts, bag, label_set):
    buf = '@relation product_review\n\n'
    for feat in bag:
        buf += "@attribute '" + str(feat).replace("'", "\\'") + "' numeric\n"
    buf += '@attribute INSTANCE_LABEL {' + ','.join(label_set) + '}\n\n'
    buf += '@data\n'
    for inst in insts:
        vec = vectorize(inst, bag)
        vec.append(inst.label)
        buf += ','.join(vec) + '\n'
    return buf


def get_baseNP(sent):
    """
    NPPattern used by regular expression chunking
    
    NPPattern = '''
                NP: {<DT|PP\$>?<JJ>*<NN>}
                    {<NNP>+}
                    {<NN>+}
                '''
    NPChunker = RegexpParser(NPPattern)
    """
    NPs = []
    for n in sent:
        try:
            if n.node == 'NP':
                NPs.append(n)
        except AttributeError:
            continue
    return NPs


def load_review(path, label):
    paths = get_path(path)
    product2reviews = {}
    stemer = PorterStemmer()
    for p in paths:
        lines = open(p, 'r').readlines()
        product = Product()
        product.id_ = os.path.basename(p).split('.')[0]
        product.name = lines[3].strip()
        reviews = []
        r_counter = 0
        for line in lines[4::5]:
            review = Review()
            review.id_ = '_'.join([label, product.id_, str(r_counter)])
            review.feats = [stemer.stem(t) for t in wordpunct_tokenize(line.strip())]
            temp = review.feats[:]
            for i in range(len(temp) - 1):
                review.feats.append('_'.join([temp[i], temp[i+1]]))
            for i in range(len(temp) - 2):
                review.feats.append('_'.join([temp[i], temp[i+1], temp[i+2]]))
            review.label = label
            review.product = product
            reviews.append(review)
            r_counter += 1
        product2reviews[product] = reviews
    return product2reviews


def get_feat_bag(instances):
    bag = {}
    for inst in instances:
        for feat in inst.feats:
            if feat in bag:
                bag[feat] += 1
            else:
                bag[feat] = 1
    
    for feat in bag.keys():
        if bag[feat] < 5 or bag[feat] > len(instances):
            bag.pop(feat)
    
    print len(bag)
    return bag


def vectorize(inst, bag):
    vector = []
    for feat in bag:
        if feat in inst.feats:
            vector.append('1')
        else:
            vector.append('0')
    return vector
        
            
def get_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return [os.path.join(path, f) for f in os.listdir(path)]
        else:
            return [path]
    else:
        print 'Given path does not exist.'
        return
    
    
def main():
    reviews = load_review(sys.argv[1], 'camera')
    reviews.update(load_review(sys.argv[2], 'mobile'))
    insts = []
    for r in reviews.values():
        insts.extend(r)
    bag = get_feat_bag(insts)
    buf = to_arff(insts, bag, ['camera', 'mobile'])
    with open(sys.argv[3], 'w') as fp:
        fp.write(buf)
    return

if __name__ == '__main__':
    main()