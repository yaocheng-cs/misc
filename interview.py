'''
Created on Jul 26, 2012

@author: yaocheng
'''

def permute(a_string):
    if len(a_string) == 1:
        return [a_string]
    else:
        temp = []
        for i in permute(a_string[1:]):
            temp.extend(insert_at_all_positions(a_string[0], i))
        return temp
    
def insert_at_all_positions(ch, a_string):
    i = 0
    temp = []
    while i <= len(a_string):
        temp.append(a_string[0:i] + ch + a_string[i:])
        i = i + 1
    return temp

# hanoi tower solution
def hanoi(source, buf, target, n):
    if n == 2:
        item1 = source.pop(0)
        buf.insert(0, item1)
        item2 = source.pop(0)
        target.insert(0, item2)
        item1 = buf.pop(0)
        target.insert(0, item1)
    else:
        hanoi(source, target, buf, n - 1)
        itemn = source.pop(0)
        target.insert(0, itemn)
        hanoi(buf, source, target, n - 1)
    return

def coconut(num_of_pirate, to_monkey):
    flag = False
    x = 1
    while not flag:
        y = x * num_of_pirate + to_monkey
        t = 5
        while t > 0:
            y = y / (1 - 1.0 / num_of_pirate) + to_monkey
            if y == int(y):
                t = t - 1
                continue
            else:
                break
        if t == 0:
            flag = True
        else:
            x = x + 1
    return int(y)
             
def compare_to_rest(lst):
    l = len(lst)
    if l == 0:
        return None
    if l == 1:
        return lst[0]
    flags = [-1] * l
    for i in range(l):
        if flags[i] >= 0:
            continue
        else:
            curr = lst[i]
        for j in range(i + 1, l):
            if flags[j] >= 0:
                continue
            else:
                if lst[j] < curr:
                    flags[j] = i
                elif lst[j] > curr:
                    flags[i] = j
        print i, flags
    return lst[flags.index(-1)]
