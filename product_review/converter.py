'''
Created on Mar 15, 2012

@author: yaocheng
'''

import sys
import math
import re
import nltk
from editor import summarize

def read_vocabulary_from_file(src):
    vocabulary = []
    for line in iter(src.readline, ''):
        if line[0] == ';' or line[0] == '\n' or line[0] == '#':
            continue
        else:
            word = line.strip('\n')
            if word in vocabulary:
                continue
            else:
                vocabulary.append(word)
    return vocabulary

def convert_to_weka(src, des, voc):
    stemmer = nltk.LancasterStemmer()
    word_reg = re.compile('[0-9A-Za-z]+')
    
    des.write('@relation review_rate\n')
    des.write('\n')
    
    for word in voc:
        des.write('@attribute ' + word + ' real\n')
    des.write('@attribute rate {s1,s2,s3,s4,s5}\n')
    des.write('\n')
    
    des.write('@data\n')
    for line in iter(src.readline, ''):
        feature_vector = []
        try:
            rate, title, review = [item.strip() for item in line.split('\t')[5:8]]
        except (IndexError, ValueError):
            continue
        ws = set([])
        for w in nltk.wordpunct_tokenize(title + ' ' + review):
            m = word_reg.match(w)
            if m:
                ws.add(stemmer.stem(m.group(0).lower()))
        for w in voc:
            if w in ws:
                feature_vector.append('1')
            else:
                feature_vector.append('0')
        des.write(','.join(feature_vector) + ',' + 's' + str(int(math.ceil(float(rate)))) + '\n')
        
    return

def main():
    with open(sys.argv[1], 'r') as corpus_fp, open(sys.argv[2], 'w') as weka_fp:
        if sys.argv[3]:
            with open(sys.argv[3], 'r') as vocabulary_fp:
                vocabulary = read_vocabulary_from_file(vocabulary_fp)
        else:
            vocabulary = summarize(corpus_fp)
        convert_to_weka(corpus_fp, weka_fp, vocabulary)
    return

if __name__ == '__main__':
    main()