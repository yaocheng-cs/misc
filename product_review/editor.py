'''
Created on Apr 10, 2012

@author: yaocheng
'''

import sys
import re
import nltk

def summarize(corpus_fp):
    stemmer = nltk.LancasterStemmer()
    word_reg = re.compile('[0-9A-Za-z]+')
    
    apperance = {}
    for line in iter(corpus_fp.readline, ''):
        try:
            title, review = [item.strip() for item in line.split('\t')[6:8]]
        except (IndexError, ValueError):
            continue
        ws = set([])
        for w in nltk.wordpunct_tokenize(title + ' ' + review):
            m = word_reg.match(w)
            if m:
                ws.add(stemmer.stem(m.group(0).lower()))
        for word in ws:
            if word in apperance:
                apperance[word] = apperance[word] + 1
            else:
                apperance[word] = 1
    
    vocabulary = []
    for word in apperance:
        if apperance[word] >= 20:
            vocabulary.append(word)
            
    return vocabulary

def main():
    with open(sys.argv[1], 'r') as corpus_fp, open(sys.argv[2], 'w') as vocabulary_fp:
        vocabulary = summarize(corpus_fp)
        for w in vocabulary:
            vocabulary_fp.write(w + '\n')
    return

if __name__ == '__main__':
    main()