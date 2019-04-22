#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import re

#Open the CSV
qkey = pd.read_csv('questionskeywords.csv')
#print(qkey['KeyWords'][79],'\n')
#print(re.sub('[^A-Za-z ]+', '',qkey['KeyWords'][79]))

#Replaces special characters within the 'KeyWords' columns using regex.sub
for i in range(len(qkey)):
    qkey['KeyWords'][i] = re.sub('[^A-Za-z ]+', '',qkey['KeyWords'][i])

#Saves the CSV
qkey.to_csv("questionskeywords.csv", index=False)

print("done")

