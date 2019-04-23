#content based recommender system for Kaggle Challenge
#goal: match professionals with career questions from students to answer
import pandas as pd
from rake_nltk import Rake #https://pypi.org/project/rake-nltk/
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import csv

#DATA CLEANING

#initialize dataframes
professionals_df = pd.read_csv("D:/DS_CSVs/professionals.csv")
questions_df = pd.read_csv("D:/DS_CSVs/questions.csv")
answers_df = pd.read_csv("D:/DS_CSVs/answers.csv")

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

#get rid of the questions_body column, since we don't need it anymore
#questions_df.drop(columns = ['questions_body'], inplace = True) #commented this out as question_body is needed later

# set the indexes of the dataframe as the question ids instead of integers, that way we can just pull the id if needed
questions_df.set_index('questions_id', inplace = True)

# merge all keywords together into one column - leave the question title column in so we can print easily later
questions_df['KeyWords'] = '' #NEW column of ALL keywords we just extracted from question title and body
columns = questions_df.columns
for index, row in questions_df.iterrows():
    #put together a word string from the lists of keywords in the columns we made, avoiding the question title
    word_string = ''
    for col in columns:
        if col != 'questions_title':
            word_string = word_string + ' '.join(row[col])+ ' '
    row['KeyWords'] = word_string

#get rid of the original two keywords columns since we combined them
questions_df.drop(columns = ['questions_keywords', 'questions_body_keywords'], inplace = True)
#testing changes, create a csv of dataframe
questions_df.to_csv('D:/DS_CSVs/questionsKeywords.csv')

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
professionals_df.to_csv('D:/DS_CSVs/professionalsKeywords.csv')
