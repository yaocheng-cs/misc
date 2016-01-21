'''
Version 1.1
Sep.25, 2012

@author: Tong Feng

File Description:
All functions dealing with system folder or file I/O, including read, write, modify.
'''
import os

'''
Definition:
    Convert a single TXT file to ASCII ()
    old_file_dir: folder address for original file, as "D:\t1\"
    new_file_dir: folder address for new file to store, as "D:\t2\"
    old_file_name: name of original file, as "test1.txt"
    new_file_name: name of new file, as "test2.txt"
    no return
''' 
def ConvertUnicodetoASCII(old_file_dir, old_file_name, new_file_dir, new_file_name):
    fc = open(old_file_dir + old_file_name,'r').read().decode('utf-16')
    temp = open(new_file_dir + new_file_name,'w')
    temp.write(fc.encode('ascii', 'replace'))
    temp.close()

'''
Definition:
    Get all the names of files in a given folder address
    files_root_dir: address of the folder
    return a list with names
''' 
def GetFilesNameList(files_root_dir):
    filelist = os.listdir(files_root_dir)
    return filelist

'''
Definition:
    Get corpus from TXT
    file_name_dir: file address in the system, as "d:\test.txt"
    style: read by corpus or lines (0 - corpus, 1 - lines)
    return the content as a string
'''
def ReadTXT(file_name_dir, style):
    if style == 0:
        fileInput = open(file_name_dir, 'r')
        try:
            fileCorpus = fileInput.read()
        finally:
            fileInput.close()
        return fileCorpus
    else:
        fileInput = open(file_name_dir, 'r')
        try:
            fileLines = fileInput.readlines()
        finally:
            fileInput.close()
        return fileLines

'''
Definition:
    Over-write of Add the content into a file
    file_name_dir: address of the file, as "d:\test.txt"
    content: the string you want to add into the file
    style: 'a' means add at the end of an exist file, or create a new file then add;
           'w' means over-write into the file, or create a new file then write.
'''
def WriteTXT(file_name_dir, content, style):
    fileOutputPF = open(file_name_dir, style)
    fileOutputPF.write(str(content))
    fileOutputPF.close()   

###############################################################   
# Version 1.0
'''   
def ConvertUnicodetoASCII(old_dir, new_dir):
    filelist = os.listdir(old_dir)
    for x in filelist:
        print('converting file'+ x + 'to ascii format...')
        fc = open(old_dir + x,'r').read().decode('utf-16')
        temp = open(new_dir + x,'w')
        temp.write(fc.encode('ascii', 'replace'))
        temp.close()
        
def ConvertTXTtoREVIEWS(filename):
    fileInput = open(filename, 'r')
    try:
        fileCorpus = fileInput.read()
    finally:
        fileInput.close()
    passage = fileCorpus.split('Yes\nNo \n\n\n\n\n\n\n\n\n\n\n \n | PermalinkComment Comment')     
    return passage

def ConvertTXTtoPF(filename):
    fileInput = open(filename, 'r')
    try:
        fileCorpus = fileInput.read()
    finally:
        fileInput.close()
    sentences = nltk.sent_tokenize(fileCorpus)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = sentences[0]
    return sentences
    
def Write_into_file(address, PF_id, review, CF_id):
    fileOutputPF = open(address+'\\PFs\\PF_'+PF_id+'.txt', 'a')
    fileOutputPF.write(str(review))
    fileOutputPF.close()   
    
    fileOutputCF = open(address+'\\CFs\\CF_'+CF_id+'.txt', 'a')
    fileOutputCF.write(str(review))
    fileOutputCF.close()
'''
###############################################################