#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

#load in data
answers = pd.read_csv('answers.csv')

#store all authors ID
authors = []
for word in answers['answers_author_id']:
    authors.append(word)

#create dictionary using Id and their count
author_count = defaultdict(int)
for word in authors:
    author_count[word] += 1
    
#reverse dictionary: id->count to count->id
sortedAuthors = [(v,k) for k,v in author_count.items()]
sortedAuthors.sort(reverse=True)

#store all reply count
reply_count = []
for i in range(len(sortedAuthors)):
    reply_count.append(sortedAuthors[i][0])

matplotlib.rcParams['figure.figsize'] = [14,4]

import seaborn as sns

#create boxplot
num_bins = 10
ax = sns.boxplot(reply_count).set_title('Number of responses from professionals')
plt.savefig('original_boxplot.png',bbox_inches='tight')
plt.show()

#remove outliers
normal = []
counter = 0
for i in reply_count:
    if i <= 10:
        normal.append(i)
    else:
        counter = counter+1

print("Outliers removed:", counter)
print("Top 10 number of answers from professionals", reply_count[:10])

#create new boxplot without outliers
ax = sns.boxplot(normal).set_title('Number of responses from professionals')
plt.savefig('outliers_removed_boxplot.png',bbox_inches='tight')
plt.show()

#create histogram of new data
matplotlib.rcParams['figure.figsize'] = [10,6]
plt.hist(normal,num_bins)
plt.title('Number of professionals that have provided answers')
plt.xlabel('Number of responses to questions',fontsize=14)
plt.ylabel('Number of professionals', fontsize=14)
plt.savefig('professionals_with_responses.png',bbox_inches='tight')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




