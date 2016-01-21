'''
Created on Feb 8, 2013

@author: yaocheng
'''

def c_w(t, s):
    return t[1]

def pre1_w(t, s):
    i = int(t[0]) - 1
    if i >= 0:
        pre1 = s[i]
        return pre1[1]
    
def pre2_w(t, s):
    i = int(t[0]) - 2
    if i >= 0:
        pre2 = s[i]
        return pre2[1]
    
def nxt1_w(t, s):
    i = int(t[0]) + 1
    if i < len(s):
        nxt1 = s[i]
        return nxt1[1]
    
def nxt2_w(t, s):
    i = int(t[0]) + 2
    if i < len(s):
        nxt2 = s[i]
        return nxt2[1]
    
def pre2_pre1_w(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    if p2w and p1w:
        return p2w + '_' + p1w
    
def pre1_c_w(t, s):
    p1w = pre1_w(t, s)
    if p1w:
        return p1w + '_' + c_w(t, s)
    
def c_nxt1_w(t, s):
    n1w = nxt1_w(t, s)
    if n1w:
        return c_w(t, s) + '_' + n1w
    
def nxt1_nxt2_w(t, s):
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if n1w and n2w:
        return n1w + '_' + n2w
    
def pre2_pre1_c_w(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p2w and p1w and cw:
        return p2w + '_' + p1w + '_' + cw
    
def pre1_c_nxt1_w(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if p1w and cw and n1w:
        return p1w + '_' + cw + '_' + n1w
    
def c_nxt1_nxt2_w(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if cw and n1w and n2w:
        return cw + '_' + n1w + '_' + n2w
    
def c_pos(t, s):
    return t[2]
    
def pre1_pos(t, s):
    i = int(t[0]) - 1
    if i >= 0:
        pre1 = s[i]
        return pre1[2]
    
def pre2_pos(t, s):
    i = int(t[0]) - 2
    if i >= 0:
        pre2 = s[i]
        return pre2[2]
    
def nxt1_pos(t, s):
    i = int(t[0]) + 1
    if i < len(s):
        nxt1 = s[i]
        return nxt1[2]
    
def nxt2_pos(t, s):
    i = int(t[0]) + 2
    if i < len(s):
        nxt2 = s[i]
        return nxt2[2]
    
def pre2_pre1_pos(t, s):
    p2p = pre2_pos(t, s)
    p1p = pre1_pos(t, s)
    if p2p and p1p:
        return p2p + '_' + p1p

def pre1_c_pos(t, s):
    p1p = pre1_pos(t, s)
    if p1p:
        return p1p + '_' + c_pos(t, s)
    
def c_nxt1_pos(t, s):
    n1p = nxt1_pos(t, s)
    if n1p:
        return c_pos(t, s) + '_' + n1p
    
def nxt1_nxt2_pos(t, s):
    n1p = nxt1_pos(t, s)
    n2p = nxt2_pos(t, s)
    if n1p and n2p:
        return n1p + '_' + n2p
    
def pre2_pre1_c_pos(t, s):
    p2p = pre2_pos(t, s)
    p1p = pre1_pos(t, s)
    if p2p and p1p:
        return p2p + '_' + p1p + '_' + c_pos(t, s)
    
def pre1_c_nxt1_pos(t, s):
    p1p = pre1_pos(t, s)
    n1p = nxt1_pos(t, s)
    if p1p and n1p:
        return p1p + '_' + c_pos(t, s) + '_' + n1p
    
def c_nxt1_nxt2_pos(t, s):
    n1p = nxt1_pos(t, s)
    n2p = nxt2_pos(t, s)
    if n1p and n2p:
        return c_pos(t, s) + '_' + n1p + '_' + n2p
    
def bos(t, s):
    return int(t[0]) == 0
    
def eos(t, s):
    return int(t[0]) == len(s) - 1
    
def c_cap(t, s):
    return t[1].istitle()

def c_low(t, s):
    return t[1].islower()

def c_up(t, s):
    return t[1].isupper()

def pre1_cap(t, s):
    i = int(t[0]) - 1
    if i >= 0:
        pre1 = s[i]
        return pre1[1].istitle()

def pre1_low(t, s):
    i = int(t[0]) - 1
    if i >= 0:
        pre1 = s[i]
        return pre1[1].islower()

def pre1_up(t, s):
    i = int(t[0]) - 1
    if i >= 0:
        pre1 = s[i]
        return pre1[1].isupper()
    
def pre2_cap(t, s):
    i = int(t[0]) - 2
    if i >= 0:
        pre2 = s[i]
        return pre2[1].istitle()

def pre2_low(t, s):
    i = int(t[0]) - 2
    if i >= 0:
        pre2 = s[i]
        return pre2[1].islower()

def pre2_up(t, s):
    i = int(t[0]) - 2
    if i >= 0:
        pre2 = s[i]
        return pre2[1].isupper()
    
def nxt1_cap(t, s):
    i = int(t[0]) + 1
    if i < len(s):
        nxt1 = s[i]
        return nxt1[1].istitle()

def nxt1_low(t, s):
    i = int(t[0]) + 1
    if i < len(s):
        nxt1 = s[i]
        return nxt1[1].islower()

def nxt1_up(t, s):
    i = int(t[0]) + 1
    if i < len(s):
        nxt1 = s[i]
        return nxt1[1].isupper()
    
def nxt2_cap(t, s):
    i = int(t[0]) + 2
    if i < len(s):
        nxt2 = s[i]
        return nxt2[1].istitle()

def nxt2_low(t, s):
    i = int(t[0]) + 2
    if i < len(s):
        nxt2 = s[i]
        return nxt2[1].islower()

def nxt2_up(t, s):
    i = int(t[0]) + 2
    if i < len(s):
        nxt2 = s[i]
        return nxt2[1].isupper()
    
def pre2_pre1_cap(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    if p2w and p1w:
        return ' '.join([p2w, p1w]).istitle()
    
def pre2_pre1_low(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    if p2w and p1w:
        return ' '.join([p2w, p1w]).islower()
    
def pre2_pre1_up(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    if p2w and p1w:
        return ' '.join([p2w, p1w]).isupper()
    
def pre1_c_cap(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p1w and cw:
        return ' '.join([p1w, cw]).istitle()
    
def pre1_c_low(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p1w and cw:
        return ' '.join([p1w, cw]).islower()
    
def pre1_c_up(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p1w and cw:
        return ' '.join([p1w, cw]).isupper()
    
def c_nxt1_cap(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if cw and n1w:
        return ' '.join([cw, n1w]).istitle()
    
def c_nxt1_low(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if cw and n1w:
        return ' '.join([cw, n1w]).islower()
    
def c_nxt1_up(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if cw and n1w:
        return ' '.join([cw, n1w]).isupper()
    
def nxt1_nxt2_cap(t, s):
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if n1w and n2w:
        return ' '.join([n1w, n2w]).istitle()
    
def nxt1_nxt2_low(t, s):
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if n1w and n2w:
        return ' '.join([n1w, n2w]).islower()
    
def nxt1_nxt2_up(t, s):
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if n1w and n2w:
        return ' '.join([n1w, n2w]).isupper()
    
def pre2_pre1_c_cap(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p2w and p1w and cw:
        return ' '.join([p2w, p1w, cw]).istitle()
    
def pre2_pre1_c_low(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p2w and p1w and cw:
        return ' '.join([p2w, p1w, cw]).islower()
    
def pre2_pre1_c_up(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p2w and p1w and cw:
        return ' '.join([p2w, p1w, cw]).isupper()
    
def pre1_c_nxt1_cap(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if p1w and cw and n1w:
        return ' '.join([p1w, cw, n1w]).istitle()
    
def pre1_c_nxt1_low(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if p1w and cw and n1w:
        return ' '.join([p1w, cw, n1w]).islower()
    
def pre1_c_nxt1_up(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if p1w and cw and n1w:
        return ' '.join([p1w, cw, n1w]).isupper()
    
def c_nxt1_nxt2_cap(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if cw and n1w and n2w:
        return ' '.join([cw, n1w, n2w]).istitle()
    
def c_nxt1_nxt2_low(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if cw and n1w and n2w:
        return ' '.join([cw, n1w, n2w]).islower()
    
def c_nxt1_nxt2_up(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if cw and n1w and n2w:
        return ' '.join([cw, n1w, n2w]).isupper()
    
def c_dot(t, s):
    cw = c_w(t, s)
    if len(cw) > 1:
        return cw[-1] == '.'

def c_poss(t, s):
    cw = c_w(t, s)
    if len(cw) > 2:
        return cw[-2] == "'"
    
def c_stat(t, s):
    cw = c_w(t, s)
    return cw in state_name

def pre1_stat(t, s):
    p1w = pre1_w(t, s)
    if p1w:
        return p1w in state_name
    
def nxt1_stat(t, s):
    n1w = nxt1_w(t, s)
    if n1w:
        return n1w in state_name
    
def pre1_c_stat(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p1w and cw:
        return ' '.join([p1w, cw]) in state_name
    
def c_nxt1_stat(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if cw and n1w:
        return ' '.join([cw, n1w]) in state_name
    
def pre2_pre1_c_stat(t, s):
    p2w = pre2_w(t, s)
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    if p2w and p1w and cw:
        return ' '.join([p2w, p1w, cw]) in state_name
    
def pre1_c_nxt1_stat(t, s):
    p1w = pre1_w(t, s)
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    if p1w and cw and n1w:
        return ' '.join([p1w, cw, n1w]) in state_name
    
def c_nxt1_nxt2_stat(t, s):
    cw = c_w(t, s)
    n1w = nxt1_w(t, s)
    n2w = nxt2_w(t, s)
    if cw and n1w and n2w:
        return ' '.join([cw, n1w, n2w]) in state_name
    

state_name = [n.strip() for n in open('/Users/yaocheng/Desktop/state_name.txt', 'r')]
    
feats = [c_w,
         pre1_w, pre2_w, nxt1_w, nxt2_w,
         pre1_c_w, c_nxt1_w,
         #pre2_pre1_w, nxt1_nxt2_w,
         #pre2_pre1_c_w, c_nxt1_nxt2_w,
         c_pos,
         pre1_pos, pre2_pos,
         nxt1_pos, nxt2_pos,
         pre2_pre1_pos, pre1_c_pos,
         #c_nxt1_pos, nxt1_nxt2_pos,
         #pre2_pre1_c_pos,
         #pre1_c_nxt1_pos,
         #c_nxt1_nxt2_pos,
         bos, eos,
         c_cap, c_low, c_up,
         #pre1_cap, pre1_low, pre1_up,
         #nxt1_cap, nxt1_low, nxt1_up,
         #pre2_pre1_cap, pre2_pre1_low, pre2_pre1_up,
         pre1_c_cap, pre1_c_low, pre1_c_up,
         c_nxt1_cap, c_nxt1_low, c_nxt1_up,
         #nxt1_nxt2_cap, nxt1_nxt2_low, nxt1_nxt2_up,
         pre2_pre1_c_cap, pre2_pre1_c_low, pre2_pre1_c_up,
         pre1_c_nxt1_cap, pre1_c_nxt1_low, pre1_c_nxt1_up,
         c_nxt1_nxt2_cap, c_nxt1_nxt2_low, c_nxt1_nxt2_up,
         c_stat, pre1_stat, nxt1_stat,
         pre1_c_stat, c_nxt1_stat,
         pre2_pre1_c_stat, pre1_c_nxt1_stat, c_nxt1_nxt2_stat,
         c_dot,
         c_poss]