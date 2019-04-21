#content based recommender system for Kaggle Challenge
#goal: match professionals with career questions from students to answer
import pandas as pd
from rake_nltk import Rake #https://pypi.org/project/rake-nltk/
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import csv

#DATA CLEANING

# clean out questions.csv to only include: id, question title, question body
questions_df = pd.read_csv("Final Project Data/questions.csv")
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

#also we need to get rid of the questions_body column, since we don't need it anymore
questions_df.drop(columns = ['questions_body'], inplace = True)

# set the indexes of the dataframe as the question ids instead of integers, that way we can just pull the id if needed
questions_df.set_index('questions_id', inplace = True)

# merge all keywords together into one column - leave the question title column in so we can print easily later
questions_df['KeyWords'] = '' #NEW column of ALL keywords we just extracted from question title and body
columns = questions_df.columns
for index, row in questions_df.iterrows():
    #put together a word string from the lists of keywords in the columns we made, avoiding the title columns we want to keep
    word_string = ''
    for col in columns:
        if col != 'questions_title':
            word_string = word_string + ' '.join(row[col])+ ' '
    row['KeyWords'] = word_string
    
#get rid of the original two keywords columns since we combined them
questions_df.drop(columns = ['questions_keywords', 'questions_body_keywords'], inplace = True)

# TO DO: delete pros that have not answered any questions
# gather id #s of questions that have already been answered by each professional (might need to be excluded later??)
answers_df = pd.read_csv("Final Project Data/answers.csv")
professionals_df = pd.read_csv("Final Project Data/professionals.csv")

#CALCULATE SIMILARITY
# CountVectorizer performs a frequency count, we're going to use it on the combined question data + turn it into a matrix
# generate a cosine similarity matrix - very similar to the correlation heat maps we've done previously

#PROGRAM I/O - enter a pro id at random and result should be 10 recommended questions
