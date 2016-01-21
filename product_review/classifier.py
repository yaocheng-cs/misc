'''
Created on Mar 15, 2012

@author: yaocheng
'''

import sys
from datetime import datetime
import nltk

def process(fp):
    data = []
    for line in iter(fp.readline, ''):
        rate, title, review = line.split('\t')[5:8]
        data.append((rate, title.strip(), review.strip()))
    return data

def count(data):
    rate = [0, 0, 0, 0, 0]
    for record in data:
        index = int(float(record[0])) - 1
        rate[index] = rate[index] + 1
    return rate

def prepare(data):
    
    """
    star_1_words = set([])
    star_2_words = set([])
    star_3_words = set([])
    star_4_words = set([])
    star_5_words = set([])
    """
    stemmer = nltk.LancasterStemmer()
    
    documents = []
    record0 = data[0]
    common_words = set([stemmer.stem(w.strip('()_[]{}<>').lower())
                        for w in nltk.wordpunct_tokenize(record0[1] + ' ' + record0[2])])
    all_words = set([])
    
    for record in data[1:]:
        words = set([stemmer.stem(w.strip('()_[]{}<>').lower())
                     for w in nltk.wordpunct_tokenize(record[1] + ' ' + record[2])])
        star = record[0]
        documents.append((words, star))
        common_words = common_words & words
        all_words = all_words | words
        
    """
        if star == '1.0':
            star_1_words = star_1_words | set(words)
        elif star == '2.0':
            star_2_words = star_2_words | set(words)
        elif star == '3.0':
            star_3_words = star_3_words | set(words)
        elif star == '4.0':
            star_4_words = star_4_words | set(words)
        elif star == '5.0':
            star_5_words = star_5_words | set(words)
    
    common_words = star_1_words & star_2_words & star_3_words & star_4_words & star_5_words
    """
    
    informative_documents = [(words.difference(common_words), rate) 
                             for (words, rate) in documents]
    
    print common_words
    return [informative_documents, all_words]

def get_features(document, vocabulary):
    features = {}
    for word in vocabulary:
        features['contains(%s)' % word] = (word in document)
    return features

def main():
    data = process(sys.argv[1])
    documents, vocabulary = prepare(data)
    feature_sets = [(get_features(doc, vocabulary), star) for (doc, star) in documents]
    num_of_fs = len(feature_sets)
    train_set, test_set = feature_sets[(num_of_fs / 2):], feature_sets[:(num_of_fs / 2)]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    classifier.show_most_informative_features(5)
    print nltk.classify.accuracy(classifier, test_set)
    return

if __name__ == '__main__':
    print sys.version
    print datetime.now()
    main()
    print datetime.now()