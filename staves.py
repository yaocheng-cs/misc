'''
You want to create a staff to use in your martial arts training, and it has to meet some specific requirements.
You want it to be composed of two smaller staves of equal length so that you can either use it as a single staff or as two smaller ones.
You want the full sized staff's center of gravity to be exactly in the middle of the staff.
You have a very, very long branch from which you can cut the pieces for your staff. The mass of the branch varies significantly throughout it, so you use just any two pieces of the same length. Given a description of the mass throughout the branch, determine the longest staff you can make, then return three integers on a single line, the first two indicating the first index of each half-staff, and the third indicating the length of each half-staff.
The input will be given on a single line as a string of digits [1-9], each digit representing the mass of a section of the branch. All sections are the same size and the maximum length of the string is 500. Here is an example:
                       41111921111119
                        11119   11119
If the indicated sections are cut from the branch they will satisfy your requirements. They are both the same length, and they can be put together as either 9111111119 or 1111991111, both of which have a center of gravity exactly in the center of the staff.
Center of gravity can be determined by taking a weighted average of the mass of each section of the staff. Given the following distances and masses: Distance: 12345678 Mass: 22241211
Sum of the mass of each section: 2 + 2 + 2 + 4 + 1 + 2 + 1 + 1 = 15 Weighted sum of the masses: 2_1 + 2_2 + 2_3 + 4_4 + 1_5 + 2_6 + 1_7 + 1_8 = 60 Weighted sum / regular sum = 60 / 15 = 4
This means that the center of mass is in section 4 of the staff. If we wanted to use this staff the center of gravity would need to be (8+1)/2 = 4.5.
Here is an example problem:
                         131251141231 
                         ----    ----
If we take the sections indicated we get 1312 and 1231. By reversing the first one and putting them together we get 21311231
Sum of the mass of each section: 2 + 1 + 3 + 1 + 1 + 2 + 3 + 1 = 14 Weight sum of the masses: 2_1 + 1_2 + 3_3 + 1_4 + 1_5 + 2_6 + 3_7 + 1_8 = 63 Weighted sum / regular sum = 63 / 14 = 4.5
This puts the center of mass exactly in the center of the staff, for a perfectly balanced staff. There isn't a longer staff that can be made from this, so the answer to this problem is
0 8 4
Because the half-staves begin at indices 0 and 8 (in that order) and each is of length 4.


input 1:
123232111119232333277777999
output 1:
7 15 6

input 2:
7512839182731294837512653698759387212532563849823857812519853546649398328875256156256652116394915985281859358394738256421937941843758954891723598716547856473245243546392898871987152656238458214518158188152527386384518234758325165316563487283746285745938476523546127534721652812736459874658475366423876152387491872658763218276354827768598716283764571652637451962837648726876547826359871629836547862534761798346918275676473829648651672346981726587619462561625162561527384273482748237482734827348274827
output 2:
10 262 229

'''


# 71111 21325
# example of two staves of different weights, but when stiched together, the center of gravity
# can still be in the middle

sample0 = '131251141231'
sample1 = '123232111119232333277777999'
sample2 = '7512839182731294837512653698759387212532563849823857812519853546649398328875256156256652116394915985281859358394738256421937941843758954891723598716547856473245243546392898871987152656238458214518158188152527386384518234758325165316563487283746285745938476523546127534721652812736459874658475366423876152387491872658763218276354827768598716283764571652637451962837648726876547826359871629836547862534761798346918275676473829648651672346981726587619462561625162561527384273482748237482734827348274827'

cache = {}

def weighted_mass_sum(s, is_staff1=False):
    dis_correction = len(s) + 1 if is_staff1 else 1
    wms = 0
    for i in range(len(s)):
        wms += (i + dis_correction) * int(s[i])
    return wms

def mass_sum(s):
    ms = sum([int(x) for x in s])
    return ms

def calculate_mass(s, is_staff1=False):
    ms = mass_sum(s)
    wms = weighted_mass_sum(s, is_staff1)
    rwms = weighted_mass_sum(s[::-1], is_staff1)
    return (ms, wms, rwms)

def check(branch, s_len, cut_site0, cut_site1):
    try:
        ms0, wms0, rwms0 = cache[(0, s_len, cut_site0)]
    except KeyError:
        staff0 = branch[cut_site0:cut_site0+s_len]
        ms0, wms0, rwms0 = calculate_mass(staff0)
        cache[(0, s_len, cut_site0)] = (ms0, wms0, rwms0)
    try:
        ms1, wms1, rwms1 = cache[(1, s_len, cut_site1)]
    except KeyError:
        staff1 = branch[cut_site1:cut_site1+s_len]
        ms1, wms1, rwms1 = calculate_mass(staff1, True)
        cache[(1, s_len, cut_site1)] = (ms1, wms1, rwms1)
    ms = ms0 + ms1
    mid = s_len + 0.5
    if 1.0 * (wms0 + wms1) / ms == mid:
        return True
    if 1.0 * (wms0 + rwms1) / ms == mid:
        return True
    if 1.0 * (rwms0 + wms1) / ms == mid:
        return True
    if 1.0 * (rwms0 + rwms1) / ms == mid:
        return True
    return False

def cut_site(branch):
    b_len = len(branch)
    if b_len <= 1:
        return '0 0 0'
    max_s_len = b_len / 2
    for i in range(max_s_len, 0, -1):
        offset = b_len - i * 2
        for j in range(offset + 1):
            for k in range(j + i, b_len - i + 1):
                #print j, k, i
                if check(branch, i, j, k):
                    return ' '.join([str(j), str(k), str(i)])
    return '0 0 0'

b = sample2
print cut_site(b)
#print cache

