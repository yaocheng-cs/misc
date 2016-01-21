'''
Created on Jan 27, 2013

@author: yaocheng
'''

#usage: python2.7 ace2bio.py [ace_folder][bio_folder]

import os
import sys
import re
from nltk.tokenize import WordPunctTokenizer
from nltk.tag import pos_tag
from lxml import etree

class token(object):
    pass

def get_init_offset(sgm_path):
    try:
        with open(sgm_path, 'r') as fp:
            raw = fp.read()
            text_tag = raw.index('<TEXT>')
            init = raw[:text_tag + len('<TEXT>\n')]
            tag = re.compile(r'\<\/?[^\<\>]+\>')
            init = tag.sub('', init)
            return len(init)
    except IOError:
        print 'Something wrong when opening the sgm file'

def convert(sgm_path, apf_path, bio_path=None):
    xml_parser = etree.XMLParser(recover=True)
    try:
        sgm_tree = etree.parse(sgm_path, xml_parser)
        apf_tree = etree.parse(apf_path, xml_parser)
        if not bio_path:
            bio_path = os.path.commonprefix([sgm_path, apf_path]) + 'bio'
        output = open(bio_path, 'w')
    except:
        print 'Something wrong when opening/parsing xml file, or opening output file'
        return
    
    init_offset = get_init_offset(sgm_path)
    text = sgm_tree.xpath('/DOC/BODY/TEXT')[0].text.strip('\n')
    
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(text)
    spans = list(tokenizer.span_tokenize(text))
    pos = pos_tag(tokens)
    
    ts = []
    for i in range(len(tokens)):
        t = token()
        t.text = tokens[i]
        t.pos = pos[i][1]
        t.span = (spans[i][0] + init_offset, spans[i][1] - 1 + init_offset)
        t.bio = 'O'
        ts.append(t)
        
    entits = apf_tree.xpath('/source_file/document/entity')
    for enty in entits:
        enty_type = enty.get('TYPE')
        mentions = enty.xpath('entity_mention')
        for m in mentions:
            head = m.xpath('head')[0]
            span = (int(head[0].get('START')), int(head[0].get('END')))
            found = False
            for t in ts:
                if t.span[0] == span[0]:
                    t.bio = 'B-' + enty_type
                    found = True
                if t.span[0] > span[0] and t.span[1] <= span[1]:
                    t.bio = 'I-' + enty_type
                    found = True
            if not found:
                print 'entity mention head span not found', span, apf_path
    
    for t in ts:
        #print t.text, t.span
        output.write('\t'.join([t.text, t.pos, t.bio]) + '\n')
    output.close()
    

#usage: python2.7 ace2bio.py [ace_folder][bio_folder]
def main():
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    if os.path.isdir(input_folder):
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        fns = os.listdir(input_folder)
        bns = []
        for fn in fns:
            if fn.endswith('.sgm'):
                bns.append(fn.replace('.sgm', ''))
        for bn in bns:
            print bn
            convert(os.path.join(input_folder, bn + '.sgm'), 
                    os.path.join(input_folder, bn + '.apf.xml'), 
                    os.path.join(output_folder, bn + '.bio'))
    else:
        return

if __name__ == '__main__':
    main()