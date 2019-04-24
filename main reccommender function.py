#!/usr/bin/env python
# coding: utf-8

# In[45]:


import pandas as pd
from rake_nltk import Rake
import seaborn as sns
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

raw = pd.read_csv('professionalsKeywords.csv')
q_raw = pd.read_csv('questionsKeywords.csv')
raw = raw[raw.columns[~raw.columns.str.contains('Unnamed:')]] #purge empty columns

# In[138]:


'''
User I/O (Olivia)

- should be able to enter a pro id chosen at random and print 10 recommended questions

- (will probably require work from Destiny's code)

'''
#choose randomly from list of valid professionals
def randomProfessional():
    global raw
    return raw.sample()


#This will be where Destiny's code goes
def recommend():
    
    l= ['332a511f1569444485cf7a7a556a5e54',
        'eb80205482e4424cad8f16bc25aa2d9c',
        '4ec31632938a40b98909416bdd0decff',
        '2f6a9a99d9b24e5baa50d40d0ba50a75',
        '5af8880460c141dbb02971a1a8369529']
    return l

#This is where the math happens
#Right now professional_id thing isn't implemented. that var does nothing
#example output: 1 dataframe of this format:

#  question_ID  |   question_title                      | 
#--------------------------------------------------------
#     123...    |   How do I turn the shower on?        |
#     4f6...    |   I want to be a nurse. What's the... |
#     3cb...    |   Please help! (engineering)          |

def getRecommendations(professional_id=0):
    
    # Pseudocode:
    # This assumes the recommend function will return just a list of 10 ids
    
    '''
    questions = read_csv(questions.csv)
    topTenQuestionIds = recommend(professional_id)
    
    result = pd.DataFrame(columns=['question_id','question_title'])
    for id in topTenQuestionIds:
        temp = questions.get_row_by_id(id)
        result.append_row(temp)
        
    return result
    '''
    
    #All Questions, for lookup purposes
    questions = pd.read_csv('questions.csv')
    
    #List Of IDs
    topTen = recommend()
    
    #dataframe to hold ID & title for convenience. empty now
    result = pd.DataFrame(columns=['question_id','question_title'])
    
    j = 0
    for i in topTen:
        #This just grabs title into temp
        title = questions.loc[questions['questions_id'] == i, 'questions_title'].iloc[0]
        
        #This should just append a row that looks like ['bd7dfb3f', 'How do i make my teacher think im a mermaid']
        result.loc[j] = [i,title]
        j+= 1
        
    #Reset index real quick and move on
    result.set_index('question_id', inplace=True)
    
    return result

def main():
    #it does the same thing no matter what you enter!
    choice = input("Enter a professional's ID for 10 recommendations...or just press enter for a random one.")
    if choice is None or choice == '': #idk which one happens when you enter nothing
        choice = randomProfessional()
        print('the professional you got is ')
        print(choice['professionals_id'].iloc[0])
        print('with these keywords')
        print(choice['answered_questions'].iloc[0])
    #try:
    recs = getRecommendations(choice)
    print('10 questions to recommend to this professional:')
    for q in recs.iterrows():
        #q will be a tuple of values (question_id, question_text)
        print(q[1][0])


    #except Exception as e:
    #    print('had an oopsie...')
    #    print(e)
        
main()


# In[50]:





# In[127]:



#EXAMPLE!


df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')

df = df[['Title','Genre','Director','Actors','Plot']]

df['Key_words'] = ""

dflist = np.array_split(df, 2)

profs = dflist[0]

quests = dflist[1]

#This creates the bag of words column and discards extra columns
#Tuned to movie data now, but should be easy enough to change into professionals data
def clean(data):
    for index, row in data.iterrows():
        plot = row['Plot']
        actors = row['Actors']
        director = row['Director']
        genre = row['Genre']
        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake()

        for item in [plot,actors,director,genre]:


            # extracting the words by passing the text
            r.extract_keywords_from_text(item)

            # getting the dictionary whith key words as keys and their scores as values
            key_words_dict_scores = r.get_word_degrees()

            # assigning the key words to the new column for the corresponding movie
            row['Key_words'] += ' '.join(list(key_words_dict_scores.keys()))


    # dropping the Plot column
    data.drop(columns = ['Plot'], inplace = True)
    data.drop(columns = ['Actors'], inplace = True)
    data.drop(columns = ['Director'], inplace = True)
    data.drop(columns = ['Genre'], inplace = True)
    data = data.set_index('Title')
    
clean(profs)
clean(quests)

count = CountVectorizer()
cm1 = count.fit_transform(profs['Key_words'])
cm2 = count.fit_transform(quests['Key_words'])

# generating the cosine similarity matrix
cosine_sim = cosine_similarity(cm1, cm2)


indices = pd.Series(profs.index)

#  defining the function that takes in movie title 
# as input and returns the top 10 recommended movies
def recommendations(title, cosine_sim = cosine_sim):
    
    # initializing the empty list of recommended movies
    recommended_movies = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])
        
    return recommended_movies

recommendations('Baby Driver')
'''
##############################################################################################################

q_raw = pd.read_csv('questionsKeywords.csv')
q_raw = q_raw[q_raw.columns[~q_raw.columns.str.contains('Unnamed:')]] #purge empty columns

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(q_raw['KeyWords'])
# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

#get rid of the original two keywords columns since we combined them
q_raw.drop(columns = ['questions_keywords', 'questions_body_keywords'], inplace = True)
#testing changes, create a csv of dataframe
q_raw.to_csv('questionsKeywordsOUTPUT.csv')

#drop everything from professionals df other than id, since they're not needed
raw.drop(columns = ['professionals_location', 'professionals_industry', 'professionals_date_joined',
                                'professionals_headline'], inplace = True)
# delete pros that have not answered any questions
# gather id #s of questions that have already been answered by each professional (might need to be excluded later??)

#only need author id and matching question id from answers
answers_df.drop(columns = ['answers_date_added', 'answers_body'], inplace = True)
#set df indexes to answers_id
answers_df.set_index('answers_id', inplace = True)

#deleting pros that haven't answered any questions (AKA doesn't appear in answers_df)
for x in professionals_df['professionals_id']:
    #counts the number of times a pro id appears in the answers df
    pro_count = ((answers_df.answers_author_id == x).sum())
    #if pro id does not exist in answers df, delete it from professionals
    if(pro_count) == 0:
        #basically recreate the dataframe, excluding the row with the professional that hasn't answered questions
        professionals_df = professionals_df[professionals_df.professionals_id != x]
#now that we have the shortened list of professionals, gather the question id's that were answered by each pro
# within the answers df... then grab the question data corresponding to the ids
professionals_df['answered_questions'] = ''

for y in professionals_df['professionals_id']:
    # y is a professionals id
    #find all indexes where the pro id occurs within the answers df
    location_list = answers_df.answers_author_id[answers_df.answers_author_id == y].index.tolist()
    #use those indexes to get question id's from answers df
    question_list = [] # list of question id's answered by the professional
    for loc in location_list:
        question_list.append(answers_df.answers_question_id[loc]) # construct list of question ids by prof
    #with the question id's, gather all the question keywords into a single word string and throw it into the new
    # column in professionals
    questions_text_list = list() # list of questions body text
    for q in question_list:
        # get question text from question_df using q (question_id) as an index
        questions_text_list.append(questions_df.questions_body[q])  # append to list of questions answered by the professional

    index = professionals_df.index[professionals_df['professionals_id'] == y][0] # get row numeric index based on the professionals id
    professionals_df.at[index, 'answered_questions'] = questions_text_list # add the professionals list of questions to professionals dataframe

#now that we have the keywords, we want to set pro id as index for later searches
professionals_df.set_index('professionals_id', inplace = True)
# convert professionals df to csv so we can read it for testing
professionals_df.to_csv('professionalsKeywordsOUTPUT.csv')

'''

