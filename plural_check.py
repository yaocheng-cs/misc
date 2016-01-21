import sys
import os
from collections import defaultdict

# usage: 
# run as a script

# python plural_check.py <input_folder_or_file_path> <output_file_path>

# or call as a function

# import plural_check
# plural_check.check('input_folder_or_file_path', 'output_file_path')

def get_immediate_path(path):
    """
    If path to a file is passed in, return the path enclosed in a list;
    If path to a folder is passed in, get all immediate sub-paths within the folder, return as a list
    If path doesn't exist, print a message then return an empty list
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return [os.path.join(path, f) for f in os.listdir(path)]
        else:
            return [path]
    else:
        print 'Given path does not exist.'
        return []

def pluralized(singular):
    """
    Given a singular form, using rules to determine the plural form
    """
    if singular[-1] in ['s', 'x', 'z']:
        return singular + 'es'
    if singular[-2:] in ['ch', 'sh']:
        return singular + 'es'
    if singular[-1] == 'y':
        return singular[:-1] + 'ies'
    if singular in ['echo', 'embargo', 'hero', 'potato', 'tomato', 'torpedo', 'veto']:
        return singular + 'es'
    return singular + 's'

def check(input_path, output_path):
    """
    This function use POS tag to decide the number of a noun, it goes after following tags:
    ['NN', 'NN$', 'NNS', 'NNS$', 'NP', 'NP$', 'NPS', 'NPS$', 'NR', 'NR$', 'NRS', 'NRS$]

    Each POS tag becomes a 'bucket', and words are collected into buckets based on their POS tag.
    During collecting, the possessive form of a word is treated the same as its non-possessive
    form. For example, (tree) and (tree's) will both be collected as 'NN', while (students)
    and (students') will both be collected as 'NNS'. So in the end, there will be only 6 buckets
    instead of 12.

    Then we go through each of the three singular buckets ('NN', 'NP', 'NR'), examine every unique
    word inside, see how often (if at all) its pluralized form appears in corresponding plural bucket 
    ('NNS', 'NPS', 'NRS'). If the plural form appears more often than the singular, the word is 
    written to output. Every time when a word's plural form is found, it will be discarded from the 
    plural set, once all the words from singular buckets are examined, remaining plural forms in the 
    plural set are those NEVER appear in singular form.

    Since the tranform from singular to plural is done by applying simple rules, this function
    won't be able to properly deal with words with irregular plural forms. Also, limited by the POS
    tags it's interested in, this function skips deteminters/quantifiers (such as this and these) 
    and pronouns (I, we, myself, ourself).
    """
    pos2tokens = defaultdict(list)
    for p in get_immediate_path(input_path):
        fp = open(p, 'r')
        for line in fp:
            # read each line in the document and try to split it with whitespace
            for t in line.strip().split():
                slash_index = t.rfind('/')
                # get the token part
                token = t[:slash_index]
                if not token.isupper():
                    token = token.lower()
                # remove appositive
                apos_index = token.rfind("'")
                if apos_index > 0:
                    token = token[:apos_index]
                # get the POS part
                pos = t[slash_index + 1:]
                # remove auxiliary parts from the combined tag
                if pos[0:3] == 'fw-':
                    pos = pos[3:]
                plus_index = pos.find('+')
                if plus_index > 0:
                    pos = pos[:plus_index]
                dash_index = pos.find('-')
                if dash_index > 0:
                    pos = pos[:dash_index]
                # remove the '$' representing possessive form
                pos = pos.strip('$')
                # collect words into POS buckets
                if pos in ['nn', 'nns', 'np', 'nps', 'nr', 'nrs']:
                    pos2tokens[pos].append(token)
    with open(output_path, 'w') as fp:
        # go through singular buckets
        for pos in ['nn', 'np', 'nr']:
            # prepare singular set and plural set
            singular_set = set(pos2tokens[pos])
            plural_set = set(pos2tokens[pos + 's'])
            # go through the singular set
            for token in singular_set:
                # count how many times the singular form appears
                singular_count = pos2tokens[pos].count(token)
                # get plural form
                plural = pluralized(token)
                # count how many times the plural form appears
                plural_count = pos2tokens[pos + 's'].count(plural)
                if plural_count > 0:
                    # discard found plural form from the plural set
                    # don't use 'remove', it will raise exception for example if both 'ax' and 'axe' exist in singular set 
                    plural_set.discard(plural)
                    if plural_count > singular_count:
                        # output words which appear in plural form more often than in singular form
                        fp.write(' '.join([
                                            token, str(singular_count), 
                                            plural, str(plural_count),
                                            str(100.0 * plural_count / (plural_count + singular_count)) + '%'
                                           ]) + '\n')
            # don't forget words only appear in their plural forms; has to appear at least twice to be included
            for plural in plural_set:
                plural_count = pos2tokens[pos + 's'].count(plural)
                if plural_count > 1:
                    fp.write(' '.join(['<no-appearance>', '0', plural, str(plural_count), '100%']) + '\n')


if __name__ == '__main__':
    check(sys.argv[1], sys.argv[2])