'''
Created on Feb 28, 2013

@author: yaocheng
'''

import json
from collections import defaultdict

def dump(json_file, txt_file):
    with open(json_file, 'r') as input, open(txt_file, 'w') as output:
        buss = defaultdict(list)
        for line in input:
            j = json.loads(line)
            if j[u'type'] == u'review':
                buss[j[u'business_id']].append(j)
        rid = 1
        for b in buss.values():
            for r in b:
                try:
                    buf = '\t'.join([str(rid),
                                     str(r[u'business_id']), str(r[u'user_id']), str(r[u'date']), 
                                     str(r[u'stars']), 
                                     str(r[u'votes'][u'useful']), str(r[u'votes'][u'funny']), str(r[u'votes'][u'cool']), 
                                     str(r[u'text']).replace('\r\n', '\n').replace('\n', ' ')])
                    output.write(buf + '\n')
                    rid += 1
                except UnicodeEncodeError:
                    print 'UnicodeEncodeError', r
                except TypeError:
                    print 'TypeError', r
    

if __name__ == '__main__':
    y = dump('/Users/yaocheng/Desktop/review/yelp_dataset/yelp_academic_dataset.json', \
             '/Users/yaocheng/Desktop/review/yelp_dataset/review_ascii.txt')