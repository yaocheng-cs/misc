'''
Created on Dec 9, 2012

@author: yaocheng
'''

import sys
import os
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
from utility import doc_file
from utility import unpack

'''
class bag_of_word(object): 
    
    @property
    def stemmer(self):
        return self._stemmer
        
    @stemmer.setter
    def stemmer(self, stmr):
        try:
            stmr.stem('dummy_word')
        except AttributeError:
            print 'Specified stemmer is not a recognized nltk stemmer.'
            return
        self._stemmer = stmr
        
    @property
    def word_filter(self):
        return self._word_filter
    
    @word_filter.setter
    def word_filter(self, fltr):
        try:
            fltr('dummy_word')
        except TypeError:
            print 'Need a callable function to be provided as word filter.'
            return
        self._word_filter = fltr
    
    def __init__(self, bag_like_dict=None):
        if bag_like_dict:
            try:
                ' '.join(bag)
        self._bag = {}
        
    def _process(self, candidates):
        if self._stemmer:
            temp = [self._stemmer.stem(c) for c in candidates]
        if self._word_filter:
            pass
        return temp
            
    def collect(self, text):
        #for w in nltk.wordpunct_tokenize(text):
        pass
'''

def to_arff(instances, bag_of_words, arff_path):
    with open(arff_path, 'w') as des:
        des.write('@relation review_product\n')
        des.write('\n')
        
        for w in bag_of_words:
            des.write('@attribute ' + w + ' numeric\n')
        des.write('@attribute product_type {camera, mobile}\n')
        des.write('\n')
        
        des.write('@data\n')
        for inst in instances:
            tokens = inst['tokens']
            label = inst['label']
            feature_vector = []
            for w in bag_of_words:
                if w in tokens:
                    feature_vector.append('1')
                else:
                    feature_vector.append('0')
            des.write(','.join(feature_vector) + ',' + label + '\n')
    return

def read_class_data(path, label=None):
    '''
    Label may come from the data itself, may be assigned at run time
    '''
    if os.path.exists(path):
        if os.path.isdir(path):
            paths = [os.path.join(path, f) for f in os.listdir(path)]
        else:
            paths = [path]
    else:
        print 'Given path does not exist.'
        return
    
    doc = doc_file()
    stemmer = PorterStemmer()
    instances = []
    for p in paths:
        doc.path = p
        for raw_record in doc:
            record = unpack(raw_record, ',')
            text = record[3].strip('"')
            inst = {'tokens': [], 'label': ''}
            for t in wordpunct_tokenize(text):
                stem_t = stemmer.stem(t.lower())
                if stem_t[0].islower():
                    inst['tokens'].append(stem_t)
                else:
                    continue
            inst['label'] = label
            instances.append(inst)
    return instances

def get_word_bag(instances):
    apperance = {}
    for inst in instances:
        for t in inst['tokens']:
            if t in apperance:
                apperance[t] += 1
            else:
                apperance[t] = 1
    bag = []
    for k in apperance.keys():
        if apperance[k] >= 10: #and apperance[k] <= 30:
            bag.append(k)
    print len(bag)
    return bag
        

def main():
    c_insts = read_class_data(sys.argv[1], 'camera')
    m_insts = read_class_data(sys.argv[2], 'mobile')
    insts = c_insts + m_insts
    bag = get_word_bag(insts)
    to_arff(insts, bag, sys.argv[3])
    return

if __name__ == '__main__':
    main()