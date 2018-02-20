# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:15:15 2018

@author: shaox201
"""

import os
os.chdir('C:/Users/shaox201/Dropbox/xys/classes/murray2018/FINA8823_ML/data/download_filing')

import pandas as pd
tempdata = pd.DataFrame.from_csv('list_13d.csv', header=0, index_col=None)

import urllib.request 


for index,row in tempdata.iterrows():
    url = 'https://www.sec.gov/Archives/' +row['file']+'.txt'
    name='13D'+str(row['CIK'])+'_'+str(row['DATE_FILED'])
    con = urllib.request.urlopen(url)
    with open(os.path.basename(name),"wb") as f:
        f.write(con.read())
