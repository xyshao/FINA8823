
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:06:31 2017

@author: shaox201
"""
# set the director first to where the 10-K's are located
import os
cwd = r'C:\Users\shaox201\Dropbox\xys\classes\murray2018\FINA8823_ML\data\download_filing'
os.chdir(cwd)
import pandas as pd
import re
from bs4 import BeautifulSoup

# Write a function to strip 10-K to text 
# =============================================================================
# local_p = [file for file in os.listdir(cwd)]
# =============================================================================
flist = [file for file in os.listdir(cwd)]
record_sum = pd.DataFrame(columns=['cusip','Date','Filename'])
for infile in flist:
    date = infile[-10:]

    # First do one document
    with open(infile,'r') as f:
        x=f.read()
        


    # I am naming the variable according to the steps to be able to check each step
    # In the function, the variable will be named with one name to save the memory
    # 1.remove ASCII-Encoded segments (GRAPHIC, ZIP, EXCEL and PDF)
    exp1=re.compile('<DOCUMENT>\s*<TYPE>(?:GRAPHIC|ZIP|EXCEL|PDF).*?</DOCUMENT>',re.DOTALL)
    x1= re.sub(exp1,'', x)
    
    # make a soup
    x2=BeautifulSoup(x1,"lxml") 
    
    
    tables = x2.find_all('table')
    record = []
    # loop through the tables to scrap the text and numbers
    # from the 13D filing
    for table in tables:
        data = []
        
        # each table will be examined
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        
        # the 'data' will be a list of lists and we need to format it into a string with
        # cusip and the numbers next to the cusip
        y = [str(x) for x in data]
        temp0 =  "".join(y)
        # remove special symbols
        temp1 = re.sub('[^0-9a-zA-Z]+', '', temp0)
        # remove the space (xa0) and the non digit characters except for 'cusip'
        temp2 = re.sub('xa0|13D', '', temp1)
        
        if 'CUSIP' in temp2: 
            # print(temp2)
            # keep only the digits and cusip
            test_re = re.findall(r'\d+|CUSIP', temp2)
            record.append([item for item in test_re if len(item)>=5])   
            
            
    if record:
        record2 = [item for sublist in record for item in sublist]
        record2 = [str(x) for x in record2]       
        record_df = pd.DataFrame(list(zip(record2)),columns=['cusip'])
        record_df['Date'] =date
        record_df['Filename']=infile
        record_sum = record_sum.append(record_df, ignore_index=True)                    

# shift the next observation upward 
record_sum['cusip9'] = record_sum.groupby(['Filename'])['cusip'].shift(-1)

record_sum =  record_sum.loc[(record_sum.cusip == 'CUSIP')]
record_sum = record_sum[record_sum['cusip9'].astype(str).str.isdigit()]



record_sum['cusip9'] =  record_sum['cusip9'].astype(str).str[:9]
record_sum = record_sum.loc[record_sum['cusip9'].str.len() == 9]


record_sum2 = record_sum[['Date','Filename','cusip9']].drop_duplicates()
record_sum3 = record_sum2[['Filename']].drop_duplicates()
dup_file = len(record_sum2['Filename']) - len(record_sum3['Filename'])

# =============================================================================
# cwd = r'C:\Users\shaox201\Dropbox\xys\classes\murray2018\FINA8823_ML\data'
# os.chdir(cwd)
# record_sum2.to_csv('cusip.csv', sep=',')
# 
# 
# =============================================================================
    
        
        
    
    
    
