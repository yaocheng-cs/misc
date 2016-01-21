'''
Created on May 20, 2012

@author: yaocheng
'''

import sys
from utility import unpack

def set_attribute_type(src, des, a_name, a_type):
    for line in iter(src.readline, ''):
        if line[:10] != '@attribute':
            des.write(line)
            continue
        items = unpack(line.strip('\n'), ' ')
        try:
            if items[-2] == a_name:
                items[-1] = a_type
                des.write(' '.join(items) + '\n')
            else:
                des.write(line)
        except IndexError:
            des.write(line)
    return

def set_attribute_value(src, des, a_index, new_value, old_value):
    for line in iter(src.readline, ''):
        if line[0] in '@\n':
            des.write(line)
            continue
        items = unpack(line.strip('\n'), ',')
        if not old_value:
            try:
                items[a_index] = new_value
                des.write(','.join(items) + '\n')
            except IndexError:
                des.write(line)
        else:
            try:
                i = old_value.index(items[a_index])
                items[a_index] = new_value[i]
                des.write(','.join(items) + '\n')
            except (IndexError, ValueError):
                des.write(line)
    return

def main():
    with open(sys.argv[1], 'r') as src, open(sys.argv[2], 'w') as des:
        if sys.argv[3] == 't':
            set_attribute_type(src, des, 'rate', '{s1,s3,s5}')
        if sys.argv[3] == 'v':
            set_attribute_value(src, des, -1, ('s1', 's5'), ('s2', 's4'))
    return

if __name__ == '__main__':
    main()