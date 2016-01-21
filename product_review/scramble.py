'''
Created on Dec 21, 2012

@author: yaocheng
'''

import sys
import random

def scramble(src, des):
    i = 0
    new_lines = []
    for line in src.readlines():
        new_line = str(i) + ',' + line
        new_lines.append(new_line)
        i += 1
    random.shuffle(new_lines)
    des.write(''.join(new_lines))

def main():
    try:
        with open(sys.argv[1], 'r') as src, open(sys.argv[2], 'w') as des:
            scramble(src, des)
    except IOError:
        print 'Something wrong when open/close the file'

if __name__ == '__main__':
    main()