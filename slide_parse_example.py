# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 12:57:12 2018

@author: shaox201
"""


import os
cwd = r'C:\Users\shaox201\Dropbox\xys\classes\murray2018\FINA8823_ML\data\download_filing'
os.chdir(cwd)
import pandas as pd
import re
from bs4 import BeautifulSoup


infile = '13D1001606_2011-08-29'
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
        
data = []
temp_table = tables[2]
# each table will be examined
rows = temp_table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
    
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
        
