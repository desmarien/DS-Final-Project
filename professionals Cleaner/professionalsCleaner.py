
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import csv

#load in the professionals csv
data = pd.read_csv("professionals.csv")
csvFile = open('professionalsCLEAN.csv','a')

#opens writer
csvWriter = csv.writer(csvFile)
file = open("deletedProfessionalsID.txt","w")

#creates new row with the needed column titles
csvWriter.writerow(['professionals_id', 'professionals_location', 'professionals_industry', 'professionals_headline', 'professionals_date_joined'])

#copy of data, replaces the NaN within the csv file with np.nan
testData = data
testData['professionals_industry'].replace('', np.nan, inplace=True)
testData['professionals_headline'].replace('', np.nan, inplace=True)

#iterates through the data, if either the industry or headlines cells are not empty, add the info to the csv file
for i in range(len(data)):
    industry = data.loc[i]['professionals_industry']
    headline = data.loc[i]['professionals_headline']
    if headline is not np.nan or industry is not np.nan:
        newInfo = data.loc[i]
        
        #variables we're going to be cleaning
        info = ['professionals_industry','professionals_headline','professionals_location']
        
        #removes the nan string 
        for x in info:
            if newInfo[x] is np.nan:
                newInfo[x] = ''
        
        #writes as new row within the professionalsCLEAN.csv
        csvWriter.writerow(newInfo)
    else:
        newInfo = data.loc[i]
        file.write(newInfo['professionals_id'])
        file.write("\n")
#closes the file reader
print("done")
csvFile.close()
file.close()

