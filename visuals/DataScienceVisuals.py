#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

#load in data
data = pd.read_csv("professionals.csv")

#store industries
industry = []
for word in data['professionals_industry']:
    industry.append(word)

#create dictionary of industries-> count
industry_count = defaultdict(int)
for word in industry:
    industry_count[word] += 1

#reverse dictionary
sortedIndustry = [(v,k) for k,v in industry_count.items()]
sortedIndustry.sort(reverse=True)

#create data lists
top = []
topTitles = []
for i in range(20):
    if i !=1:
        top.append(sortedIndustry[i][0])
        topTitles.append(sortedIndustry[i][1])

matplotlib.rcParams['figure.figsize'] = [14,4]

#create horizontal bar chart
plt.barh(range(len(top)), top)
plt.yticks(range(len(topTitles)), topTitles)
plt.gca().invert_yaxis()
plt.xlabel('Number of Professionals',fontsize=14)
plt.title('Number of Professionals Within an Industry',fontsize=18)
plt.ylabel('Industry Name',fontsize=14)

plt.savefig('professionals_industry.png',bbox_inches = 'tight')

print("Number of professionals without an industry:", industry_count[np.nan])

plt.show()


# In[27]:


import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib

#Comments similar as above

data = pd.read_csv("professionals.csv")

industry = []
for word in data['professionals_location']:
    industry.append(word)

industry_count = defaultdict(int)
for word in industry:
    industry_count[word] += 1

sortedIndustry = [(v,k) for k,v in industry_count.items()]
sortedIndustry.sort(reverse=True)

top = []
topTitles = []
for i in range(20):
    if i != 0 :
        top.append(sortedIndustry[i][0])
        topTitles.append(sortedIndustry[i][1])

plt.barh(range(len(top)), top)
plt.yticks(range(len(topTitles)), topTitles)
plt.gca().invert_yaxis()
plt.ylabel('Location Name',fontsize=14)
plt.title('Locations of Professionals',fontsize=18)
plt.xlabel('Number of Professionals',fontsize=14)

#save figure as a png file
plt.savefig('professionals_location.png',bbox_inches = 'tight')

print("Number of professionals without a location:", industry_count[np.nan])

plt.show()


# In[31]:


#comments similar as above

tagsData = pd.read_csv("tags.csv")
tags = {}
for i in range(len(tagsData)):
    tags[tagsData['tags_tag_id'][i]] = tagsData['tags_tag_name'][i]
    
userTagData = pd.read_csv("tag_users.csv")

tagFrequency = []
for i in range(len(userTagData)):
    tagFrequency.append(tags[userTagData['tag_users_tag_id'][i]])
    
tagCount = defaultdict(int)
for word in tagFrequency:
    tagCount[word] += 1
    
sortedTag = [(v,k) for k,v in tagCount.items()]
sortedTag.sort(reverse=True)

top = []
topTitles = []
for i in range(20):
    if i != 0 :
        top.append(sortedTag[i][0])
        topTitles.append(sortedTag[i][1])
        
plt.barh(range(len(top)), top)
plt.yticks(range(len(topTitles)), topTitles)
plt.ylabel('Tag Name',fontsize=14)
plt.gca().invert_yaxis()
plt.title('Number of professionals following a tag', fontsize=18)
plt.xlabel('Number of Professionals',fontsize=14)

plt.savefig('professionals_tags.png',bbox_inches='tight')

plt.show()


# In[35]:


import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib

#comments similar as above

data = pd.read_csv("students.csv")

student_location = []
for word in data['students_location']:
    student_location.append(word)

location_count = defaultdict(int)
for word in student_location:
    location_count[word] += 1
    
sortedLocation = [(v,k) for k,v in location_count.items()]
sortedLocation.sort(reverse=True)

top = []
topLocations = []
for i in range(20):
    if i != 0 :
        top.append(sortedLocation[i][0])
        topLocations.append(sortedLocation[i][1])

plt.barh(range(len(top)), top)
plt.yticks(range(len(topLocations)), topLocations)
plt.gca().invert_yaxis()
plt.ylabel('Location Name',fontsize=14)
plt.title('Locations of Students',fontsize=18)
plt.xlabel('Number of Students',fontsize=14)

plt.savefig('students_locations.png',bbox_inches='tight')

print("Number of students without a location:", location_count[np.nan])

plt.show()


# In[36]:


emails = pd.read_csv("emails.csv")

emails.emails_frequency_level.replace(["email_notification_daily", "email_notification_immediate", "email_notification_weekly"], ["daily", "immediate", "weekly"], inplace=True)

frequencies = []
for word in emails['emails_frequency_level']:
    frequencies.append(word)

emailFreq = defaultdict(int)
for word in frequencies:
    emailFreq[word] += 1
    
sortedLocation = [(v,k) for k,v in emailFreq.items()]
sortedLocation.sort(reverse=True)

top = []
topFreq = []
for i in range(len(sortedLocation)):
    top.append(sortedLocation[i][0])
    topFreq.append(sortedLocation[i][1])


plt.bar(range(len(top)), top)
plt.xticks(range(len(topFreq)), topFreq)
plt.xlabel('Type of Frequency',fontsize=14)
plt.title('Email Frequencies of Recipients',fontsize=18)
plt.ylabel('Number of Emails',fontsize=14)

plt.savefig('email_frequency.png')

plt.show()


# In[ ]:





# In[37]:


questions = pd.read_csv("questions.csv")

years = []
monthYear = []

for word in questions['questions_date_added']:
    years.append(word[:4])
    monthYear.append(word[:7])

yearFreq = defaultdict(int)
years.sort()
for word in years:
    yearFreq[word] += 1
    
monthYearFreq = defaultdict(int)
monthYear.sort()
for word in monthYear:
    monthYearFreq[word] += 1
    
sortedYears = [(v,k) for k,v in yearFreq.items()]

top = []
topFreq = []
for i in range(len(sortedYears)):
    top.append(sortedYears[i][0])
    topFreq.append(sortedYears[i][1])
    
plt.bar(range(len(top)), top)
plt.xticks(range(len(topFreq)), topFreq)
plt.xlabel('Year Added',fontsize=14)
plt.title('Year Date of Questions Added',fontsize=18)
plt.ylabel('Number of Questions',fontsize=14)

plt.savefig('year_date_added.png')

plt.show()


# In[39]:


sortedDates = [(v,k) for k,v in monthYearFreq.items()]

top = []
topFreq = []
for i in range(len(sortedDates)):
    top.append(sortedDates[i][0])
    topFreq.append(sortedDates[i][1])
    
matplotlib.rcParams['figure.figsize'] = [18,5]

plt.bar(range(len(top)), top,align='center',width=.8)
plt.xticks(range(len(topFreq)), topFreq)
plt.xlabel('Date Added',fontsize=14)
plt.title('Date of Questions Added',fontsize=18)
plt.ylabel('Number of Questions',fontsize=14)
plt.xticks(rotation=90,fontsize=9)

plt.savefig('full_date_added.png',bbox_inches='tight')

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




