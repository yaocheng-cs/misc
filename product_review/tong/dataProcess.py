'''
Created on 2012-10-2
Version 1.1

@author: Tong Feng
'''
import re

'''
Definition:
    Delete the whole line when its value equals to anyone in the String Array.
    stringList: all the values of lines that going to be deleted
    textArray: the original text Array
    return a new text Array after deleting
'''
def DeletebyStrValue(stringList, textArray):
    new_textArray = []
    for text in textArray:
        flag = 0
        for strTemp in stringList:
            if text == strTemp:
                flag = 1
        if flag == 0:
            new_textArray.append(text)
    return new_textArray

'''
Definition:
    Delete the whole line when its value matches to anyone in the String Array.
    stringList: all the values of lines that are going to be matching
    textArray: the original text Array
    return a new text Array after deleting
'''
def DeletebyStrMatch(stringList, textArray):
    new_textArray = []
    for text in textArray:
        flag = 0
        for strTemp in stringList:
            matchResult = strTemp in text
            if matchResult:
                flag = 1
        if flag == 0:
            new_textArray.append(text)
    return new_textArray

'''
Definition:
    Delete the whole line when its value matches to anyone in the Regular Expressions.
    regExpList: all the RegExps that are going to be deleting
    textArray: the original text Array
    return a new text Array after deleting
'''
def DeletebyRegExp(regExpList, textArray):
    new_textArray = []
    for text in textArray:
        flag = 0
        for regTemp in regExpList:
            p = re.compile(regTemp, re.IGNORECASE)
            m = p.match(text)
            if m != None:
                flag = 1
        if flag == 0:
            new_textArray.append(text)
    return new_textArray
