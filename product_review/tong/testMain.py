'''
Version 1.1
Sep.25 2012
Updated Dec.01 2012

@author: Tong Feng
'''
import controller

dir_productCategory = "D:\\Workspace\\IS\\data\\camera\\"

dir_datasetUNICODE = dir_productCategory + "DataSetUnicode\\"
dir_datasetASCII = dir_productCategory + "DataSetASCII\\"
dir_dataset = dir_productCategory + "DataSet\\"
dir_sents = dir_productCategory + "Sents\\"
dir_sents_s = dir_productCategory + "Sents_S\\"
dir_sents_s_cf_pf = dir_productCategory + "Sents_S_CF_PF\\"
dir_PFlist = dir_productCategory + "PF.txt"

# Step 0: Create directory whenever adding new category
# controller.Create_Directory(dir_productCategory)

######################################
# Step 1-3: 
# Input: Raw data in file directory: xxxDataSetUnicode
# Output: xxxDataSetASCII, xxxDataSet(expected data), xxxSents(divided by sentences)
######################################

# Step 1: Convert Unicode to ASCII (get xxxDataSetASCII)
controller.Create_DataSetASCII(dir_datasetUNICODE, dir_datasetASCII)

# Step 2: Eliminate non-sense information (get xxxDataSet)
controller.Create_DataSet(dir_datasetASCII, dir_dataset)

# Step 3: Dividing corpus into sentences
controller.Create_Sents(dir_dataset, dir_sents)

##########################################
# Step 4:
# input: Sents_S (get from Sents after using sentiment140 API)
# output: Sents_S_CF_PF with Sentiment Value
##########################################

# Step 4: 
controller.Create_Sents_S_CF_PF(dir_sents_s, dir_sents_s_cf_pf, dir_PFlist)


##############################################
# From here begin: Version 1.0
'''
# Get review from one single file "B0009FCAJA.txt" - PASS
s_file = fileIO.ReadTXT("D:\Workspace\IS\data\mobile\MobileDataSet\B0009FCAJA.txt", 1)
reviews = []
for i in range(len(s_file)):
    if s_file[i][0] != ' ':
        reviews.append(s_file[i])
# Parsing to sentences
sentences = []
for i in range(len(reviews)):
    j = []
    j = nltk.sent_tokenize(reviews[i])
    for m in range(len(j)):
        if m != (len(j)-1):
            sentences.append(j[m] + '\n')
        else:
            sentences.append(j[m])
    
# Write into a single file with sentences
fileIO.WriteTXT("D:\B0009.txt", sentences, 'a')


# single product file test - - - PASS
# file pre-processing
filename_PF = 'C:\\Users\\Administrator\\Desktop\\POS\\moblie_PF_singleword.txt'
filename_Reviews = 'C:\\Users\\Administrator\\Desktop\\POS\\B004O0U4X0.txt'

review_list = fileIO.ConvertTXTtoREVIEWS(filename_Reviews)
PF_list = fileIO.ConvertTXTtoPF(filename_PF)

# compare and write into files
writeInAddress = 'C:\\Users\\Administrator\\Desktop\\POS'
contain.Compare(writeInAddress, PF_list, review_list)

# multiply product files test - - - PASS

dir_data_root = 'D:\\Workspace\\IS\\data\\mobile\\'
dir_PF = dir_data_root + 'moblie_PF_singleword.txt'
dir_rawDataTXT_Unicode = dir_data_root + 'MobileDataSetUnicode\\'
dir_rawDataTXT_ASCII = dir_data_root + 'MobileDataSetASCII\\'
writeInAddress = dir_data_root

# convert raw data from unicode txt to ascii txt
# enable the following code when necessary
# controller.ConvertFilesbyFolder_UnicodetoASCII(dir_rawData_Unicode, dir_rawDataTXT_ASCII)

PF_list = controller.ConvertTXTtoPF(dir_PF)
filename_List = fileIO.GetFilesNameList(dir_rawDataTXT_ASCII)
for productID in filename_List:
    review_list = controller.ConvertTXTtoREVIEWS(dir_rawDataTXT_ASCII + productID)
    # compare and write into files
    controller.Compare(writeInAddress, PF_list, review_list)

print('Finish Data Pre-processing!')
'''
