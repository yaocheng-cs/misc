'''
Created on 2012-10-1
Version 1.1

@author: Tong Feng
'''
import fileIO
import dataProcess
import nltk
import os

def Create_Directory(dir_productCategory):
    dir_datasetUNICODE = dir_productCategory + "DataSetUnicode\\"
    dir_datasetASCII = dir_productCategory + "DataSetASCII\\"
    dir_dataset = dir_productCategory + "DataSet\\"
    dir_sents = dir_productCategory + "Sents\\"
    dir_sents_s = dir_productCategory + "Sents_S\\"
    dir_sents_s_cf_pf = dir_productCategory + "Sents_S_CF_PF\\"
    dir_other = dir_productCategory + "other\\"
    if not os.path.exists(dir_productCategory): os.makedirs(dir_productCategory)
    if not os.path.exists(dir_datasetUNICODE): os.makedirs(dir_datasetUNICODE)
    if not os.path.exists(dir_datasetASCII): os.makedirs(dir_datasetASCII)
    if not os.path.exists(dir_dataset): os.makedirs(dir_dataset)
    if not os.path.exists(dir_sents): os.makedirs(dir_sents)
    if not os.path.exists(dir_sents_s): os.makedirs(dir_sents_s)
    if not os.path.exists(dir_sents_s_cf_pf): os.makedirs(dir_sents_s_cf_pf)
    if not os.path.exists(dir_other): os.makedirs(dir_other)
    open(dir_productCategory + "CF.txt", 'w').close()
    open(dir_productCategory + "PF.txt", 'w').close()

def Create_DataSetASCII(old_dir, new_dir):
    filelist = fileIO.GetFilesNameList(old_dir)
    for x in filelist:
        print('Creating DataSetASCII...'+ x)
        fileIO.ConvertUnicodetoASCII(old_dir, x, new_dir, x)

def Create_DataSet(dir_datasetASCII, dir_dataset):
    fileList = fileIO.GetFilesNameList(dir_datasetASCII)
    for x in fileList:
        textArray = fileIO.ReadTXT(dir_datasetASCII + x, 1)
        result = RawDataPreprocessing(textArray)
        for i in range(len(result)):
            fileIO.WriteTXT(dir_dataset + x, result[i], 'a')
            print("Creating DataSet... " + x)
            
def Create_Sents(dir_dataset, dir_sents):
    m_filelist = fileIO.GetFilesNameList(dir_dataset)
    for x in m_filelist:
        m_file = fileIO.ReadTXT(dir_dataset + x, 1)
        reviews = []
        for i in range(len(m_file)):
            if m_file[i][0] != ' ':
                reviews.append(m_file[i])
        # dividing into sentences
        sentences = ""
        for i in range(len(reviews)):
            j = []
            j = nltk.sent_tokenize(reviews[i])
            for m in range(len(j)):
                if m != (len(j)-1):
                    sentences += j[m] + '\n'
                else:
                    sentences += j[m]
        fileIO.WriteTXT(dir_sents + x, sentences, 'a')
        print("Creating Sents..." + x)

def Create_Sents_S_CF_PF(dir_sents_s, dir_sents_s_cf_pf, dir_PFlist):
    pf_list = Get_PF_list(dir_PFlist)
    filelist = fileIO.GetFilesNameList(dir_sents_s)
    for x in filelist:
        print('Creating Sents_S_CF_PF...' + x)
        old_content = fileIO.ReadTXT(dir_sents_s + x, 1)
        resultArray = []
        for i in range(len(old_content)):
            sents = ""
            for j in range(5, len(old_content[i])-2):
                sents = sents + old_content[i][j]
            resultArray = Match_CF_PF(sents, pf_list)
            new_content = "\"" + str(resultArray[0]) + "\",\"" + str(resultArray[1]) + "\"," + old_content[i]
            fileIO.WriteTXT(dir_sents_s_cf_pf + x, new_content, 'a')
            
def Match_CF_PF(sents, pf_list):
    for i in range(len(pf_list)):
        resultArray = []
        result = ((pf_list[i][1].lower()+' ') in (sents.lower())) or ((pf_list[i][1].lower() + '.') in sents.lower())
        if result:
            # append CF
            resultArray.append(pf_list[i][2])
            # append PF
            resultArray.append(pf_list[i][0])
        else:
            # adding into CF_0
            resultArray.append(0)
            resultArray.append(0)
    return resultArray
       
def Get_PF_list(dir_PFlist):
    pf_temp1 = fileIO.ReadTXT(dir_PFlist, 1)
    pf_temp2 = []
    pf_list = []
    for i in range(len(pf_temp1)):
        pf_temp2.append(pf_temp1[i][:-1])
    for i in range(len(pf_temp2)):
        pf_list.append(pf_temp2[i].split('\t'))
    return pf_list   
  
def RawDataPreprocessing(textArray):
    stringList = []
    stringList.append('  Yes\n')
    stringList.append('No \n')
    stringList.append('\n')
    
    regExpList = []
    regExpList.append('\s*\n')
    
    stringMatchList = []
    stringMatchList.append('PermalinkComment Comment')
    stringMatchList.append('Most Helpful First')
    stringMatchList.append('(What\'s this?)')
    stringMatchList.append('&lsaquo;')
    
    # Disable this when use it later
    stringMatchList.append('people found the following review helpful')
    
    result = []
    result = dataProcess.DeletebyStrValue(stringList, textArray)
    result = dataProcess.DeletebyRegExp(regExpList, result)
    result = dataProcess.DeletebyStrMatch(stringMatchList, result)
    return result

###########################################################
'''v1.0
# Verify whether a text contains anyone in stringList.
# If yes, save it into PFs or CFs. If no, save it into 'CF_0.txt'
def Compare(dir_file_root, stringList, textArray):
    for i in range(len(textArray)):       
        for j in range(1,len(stringList),3):
            # verify the first pf is in the review or not
            result = ((stringList[j].lower()+' ') in (textArray[i].lower())) or ((stringList[j].lower() + '.') in (textArray[i]).lower())
            if result:
                Write_into_file(dir_file_root, stringList[j-1], textArray[i], stringList[j+1])
                print('Adding a new review into PF and CF...')
            else:
                Write_into_file(dir_file_root, 0, textArray[i], 0)

# Write reviews into PFs and CFs     
def Write_into_file(dir_file_root, PF_id, review, CF_id):
    fileIO.WriteTXT(dir_file_root+'\\PFs\\PF_'+PF_id+'.txt', review, 'a')
    fileIO.WriteTXT(dir_file_root+'\\CFs\\CF_'+CF_id+'.txt', review, 'a')
    
def ConvertTXTtoREVIEWS(file_name_dir):
    fileCorpus = fileIO.ReadTXT(file_name_dir, 0)
    passage = fileCorpus.split('Yes\nNo \n\n\n\n\n\n\n\n\n\n\n \n | PermalinkComment Comment')     
    return passage

def ConvertTXTtoPF(file_name_dir):
    fileCorpus = fileIO.ReadTXT(file_name_dir, 0)
    sentences = nltk.sent_tokenize(fileCorpus)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = sentences[0]
    return sentences
'''