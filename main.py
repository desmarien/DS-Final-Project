#content based recommender system for Kaggle Challenge
#goal: match professionals with career questions from students to answer
import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#DATA CLEANING
# clean out questions.csv to only include: id, question title, question body
# separate the hashtags from question body into their own column
# perform keyword rake on question body
# merge question title, question body, and hashtags into one column

# delete pros that have not answered any questions
# gather questions that have already been answered by each professional (might need to be excluded later??)
# add question id's that have already been answered into a column of profressionals.csv

#CALCULATE SIMILARITY
# CountVectorizer performs a frequency count, we're going to use it on the combined question data + turn it into a matrix
# generate a cosine similarity matrix - very similar to the correlation heat maps we've done previously

#PROGRAM I/O - enter a pro id at random and result should be 10 recommended questions
