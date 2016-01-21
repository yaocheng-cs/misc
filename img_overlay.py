'''
Created on Sep 7, 2011

@author: yaocheng
'''

import os
import re
from PIL import Image

ID = '46L200'
Z = 2

BASEFOLDER = '/Users/yaocheng/Desktop/workshop/'
NISSLFOLDER = BASEFOLDER + ID + '_nissl/'
LABELFOLDER = BASEFOLDER + ID + '_label/'
OVERLAYFOLDER = BASEFOLDER + ID + '_overlay/'
print NISSLFOLDER
print LABELFOLDER

mask = Image.new('L', (5625, 3188), 100)
section = re.compile('section_[0-9]{3}')

list = os.listdir(NISSLFOLDER)
for fname in list:
    print fname
    match = section.search(fname)
    sn = int(match.group(0).split('_')[1])
    print sn
    
    num = str(sn * Z - 1)
    im1 = Image.open(NISSLFOLDER + fname)
    while len(num) < 4:
        num = '0' + num
    print num
    im2 = Image.open(LABELFOLDER + 'axial_slice_' + num + '.tif')
    
    im1 = im1.resize((5625, 3188))
    im2 = im2.resize((5625, 3188))
    
    im1.paste(im2, None, mask)
    ovl_small = im1.resize((338, 191))
    im1.save(OVERLAYFOLDER + 'overlay_' + str(sn) + '.jpg')
    ovl_small.save(OVERLAYFOLDER + 'overlay_' + str(sn) + '_small.jpg')
    