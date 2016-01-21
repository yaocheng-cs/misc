'''
Created on Oct 16, 2009

@author: yao
'''

print "Hello World!"

import os
import re
from PIL import Image

ID = '46L200'
Z = 2

BASEFOLDER = '/Users/yaocheng/Desktop/'
IMGFOLDER = BASEFOLDER + ID + '/'
TXTFOLDER = IMGFOLDER + 'txt/'
MASKFOLDER = IMGFOLDER + 'mask/'
print TXTFOLDER
COUNT = BASEFOLDER + ID + '_count.txt'
print COUNT

count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]

section = re.compile('section_[0-9]{3}')

list = os.listdir(TXTFOLDER)
for txtname in list:
    print txtname
    if not ID in txtname:
        continue
    
    maskname = txtname.replace('analysis.txt', 'detected2.jpg')
    print maskname
    im = Image.open(MASKFOLDER + maskname)
    dx = (11250 - im.size[0]) / 2
    dy = (6375 - im.size[1]) / 2
    
    match = section.search(txtname)
    num = int(match.group(0).split('_')[1])
    print 'section num:', num
    n_str = str(num * Z - 1)
    while len(n_str) < 3:
        n_str = '0' + n_str
    print 'label num:', n_str
    im = Image.open(IMGFOLDER + 's-' + n_str + '.tif')
    pix = im.load()
    
    fp = open(TXTFOLDER + txtname, 'r')
    for buf in fp.readlines():
        line = buf.split('\t')
        if len(line) < 14:
            continue
        if line[1] == 'reason':
            continue
        if line[1] != '0':
            continue 
        x = (float(line[8]) + dx) * 0.03
        y = (float(line[9]) + dy) * 0.03
        print x, y, pix[x,y]
        count[pix[x, y]] = count[pix[x, y]] + 1
    
fp.close()


fp = open(COUNT, 'w')
for i in count:
    fp.write(str(i) + '\t')
    
fp.close()    