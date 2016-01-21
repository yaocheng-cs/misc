'''
Created on Feb 8, 2013

@author: yaocheng
'''

#usage: python2.7 bio2crff.py [bio_path][crff_path]

import re
from utility import doc_file

def is_sent(buf):
    if re.search(r'\n\n$', buf):
        return True
    else:
        return False

def convert(bio_path, crff_path, feats, labeled=True, fmt='crfsuite'):
    try:
        output = open(crff_path, 'w')
    except IOError:
        print 'cannot open crff file'
        return
    df = doc_file(bio_path, is_sent)
    for s in df:
        sent = [t.split() for t in s.strip().split('\n')]
        if not labeled:
            for t in sent:
                t.append('empty')
        for token in sent:
            label = token[-1]
            if fmt == 'crfsuite':
                crff_line = label + '\t' + '\t'.join([f.func_name + '=' + str(f(token, sent)) for f in feats if f(token, sent)])
            if fmt == 'mallet':
                crff_line = ' '.join([f.func_name + '=' + str(f(token, sent)) for f in feats if f(token, sent)]) + ' ' + label
            output.write(crff_line + '\n')
        output.write('\n')
    df.close()
    output.close()
    