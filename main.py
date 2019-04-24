#content based recommender system for Kaggle Challenge
#goal: match professionals with career questions from students to answer
import pandas as pd
from rake_nltk import Rake #https://pypi.org/project/rake-nltk/
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import csv
import re

#DATA CLEANING

#initialize dataframes
professionals_df = pd.read_csv("Final Project Data/professionals.csv")
questions_df = pd.read_csv("Final Project Data/questions.csv")
answers_df = pd.read_csv("Final Project Data/answers.csv")

# clean out questions.csv to only include: id, question title, question body
questions_df = questions_df[['questions_id', 'questions_title', 'questions_body']]

# function to perform keyword rake on a given df with the name of the column and name of new column created with keywords
def getKeywords(df, column_name, new_column_name):
    # add a new empty column to df
    df[new_column_name] = ""
    for index, row in df.iterrows():
        column_data = row[column_name]
        #word rake, automatically uses stop words and gets rid of punctuation!!! :D
        r = Rake()
        # extract key words
        r.extract_keywords_from_text(column_data)
        # get the dictionary with key words as keys and their scores as values (maybe use later? idk)
        keywords_scores = r.get_word_degrees()
        # assigning the key words to the new column
        row[new_column_name] = list(keywords_scores.keys())
        
#get keywords for title and question body        
getKeywords(questions_df, 'questions_title', 'questions_keywords')
getKeywords(questions_df, 'questions_body', 'questions_body_keywords')
# set the indexes of the dataframe as the question ids instead of integers, that way we can just pull the id if needed
questions_df.set_index('questions_id', inplace = True)
#get rid of the questions_body column, since we don't need it anymore
questions_df.drop(columns = ['questions_body'], inplace = True)

# merge all keywords together into one column - leave the question title column in so we can print easily later
questions_df['KeyWords'] = ''
#NEW column of ALL keywords we just extracted from question title and body
columns = questions_df.columns
for index, row in questions_df.iterrows():
    #put together a word string from the lists of keywords in the columns we made, avoiding the question title
    word_string = ''
    for col in columns:
        if col != 'questions_title':
            word_string = word_string + ' '.join(row[col])+ ' '
    row['KeyWords'] = word_string

#noticed ther are some special characters left behind from keywords, gonna clean the dataset
for i in range(len(questions_df)):
    questions_df['KeyWords'][i] = re.sub('[^A-Za-z ]+', '',questions_df['KeyWords'][i])

#get rid of the original two keywords columns since we combined them
questions_df.drop(columns = ['questions_keywords', 'questions_body_keywords'], inplace = True)
#create a csv of the new, clean dataframe
questions_df.to_csv('Final Project Data\questionsKeywords.csv')

#drop everything from professionals df other than id, since they're not needed
professionals_df.drop(columns = ['professionals_location', 'professionals_industry', 'professionals_date_joined',
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
    #find all indexes where the pro id occurs within the answers df
    location_list = answers_df.answers_author_id[answers_df.answers_author_id == y].index.tolist()
    #use those indexes to get question id's from answers df
    question_list = []
    for loc in location_list:
        question_list.append(answers_df.answers_question_id[loc])
    index = professionals_df.index[professionals_df['professionals_id'] == y][0] # get row numeric index based on the professionals id
    professionals_df.at[index, 'answered_questions'] = question_list # add the professionals list of questions to professionals dataframe
    
#now that we have the keywords, we want to set pro id as index for later searches
professionals_df.set_index('professionals_id', inplace = True)
# convert professionals df to csv so we can read it for testing
professionals_df.to_csv('Final Project Data\professionalsKeywords.csv')

#countvectorizer will count frequency of each word in the question keywords for the whole column of keywords 
count = CountVectorizer()
count_matrix = count.fit_transform(questions_df['KeyWords'])
# generating the cosine similarity matrix of the keyword frequency
cosine_sim = cosine_similarity(count_matrix, count_matrix)
#this should generate a comparison of all questions to each other, and look similar to the heat maps we did in class

#generating the top 10 results!

#associate the question_id's to a numerical index used for navigating the cosine matrix
indices = pd.Series(questions_df.index)

#returns a list of top 10 recommended question id's and similarity scores...
# written as a function so that when a professional has more than one question, we can run this for each question_id
# and then gather the top 10 results from the mega-list of questions and scores. This way we account for similarity
# to all the questions previously answered by the professional.
def top10(question_ids, cosine_sim):
    #new list for storing ids and scores
    recommended_questions_dict = {}
    #create a dictionary of question ids and sim scores, containing top 10 sim scores for each question i
    for i in question_ids:
        #get matrix index of question_id i
        index = indices[indices == i].index[0]
        #create a series of all scores, sort from highest to lowest
        sim_scores = pd.Series(cosine_sim[index]).sort_values(ascending = False)
        #get the scores AND the index in the matrix of the top 10 scores for question i
        top_scores = list(sim_scores.iloc[1:11])
        top_indices = list(sim_scores.iloc[1:11].index)
        #get the question_ids of top ten scores for question i
        for i in range(len(top_indices)):
            #saves question id as a key to the score
            recommended_questions_dict[(questions_df.index)[top_indices[i]]] = top_scores[i]
    top_10_recs = dict(Counter(results).most_common(10))
    return list(top_10_recs.keys())

#OUTPUT/Results
pro_id = input("enter a professional id#: ")
search_questions = professionals_df.at[pro_id, 'answered_questions']
results = top10(search_questions, cosine_sim)
print(results)
