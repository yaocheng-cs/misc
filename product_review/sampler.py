'''
Created on Mar 15, 2012

@author: yaocheng
'''

import sys
import math
from utility import unpack

def get_first_n_sample(src, des, n):
    i = 0
    while i < n:
        line = src.readline()
        des.write(line)
        i = i + 1
    return

def get_product_id(src, des):
    for line in iter(src.readline, ''):
        product_id = line.split('\t')[1]
        des.write(product_id + '\n')
    return

def get_n_each_sample(src, des, n):
    c = [0, 0, 0, 0, 0]
    while c[0] < n or c[1] < n or c[2] < n or c[3] < n or c[4] < n:
        line = src.readline()
        try:
            rate = int(math.ceil(float(unpack(line, '\t')[5])))
            index = rate - 1
            if c[index] < n:
                des.write(line)
                c[index] = c[index] + 1
        except IndexError:
            continue
    return

def get_one_product_review(src, des, pid):
    for line in iter(src.readline, ''):
        items = unpack(line, '\t')
        try:
            product_id = items[1]
            title = items[-2]
            review = items[-1]
        except IndexError:
            continue
        if product_id == pid:
            des.write(title + '\n' + review + '\n')
    return

def main():
    with open(sys.argv[1], 'r') as src, \
         open(sys.argv[2], 'w') as des1, open(sys.argv[3], 'w')  as des2:
        #get_first_n_sample(src, des, 100)
        #get_product_id(src, des)
        get_n_each_sample(src, des1, 100)
        get_n_each_sample(src, des2, 100)
        #get_one_product_review(src, des, 'B0007RT9LC')
    return
    
if __name__ == '__main__':
    main()
        