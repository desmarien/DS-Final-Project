# A Content-Based Filtering Recommendation System for Matching Student Questions to Interested Professionals
Data Science final project, COSC 481 Spring 2019

### Team
- Sebastian Cortes
- Olivia Lyons
- Destiny Adams (Organizer)
- Hannah Roe
- Harrison Ratcliffe

## Abstract
CareerVillage.org is a forum based website created to help students without guidance get answers to career questions from real professionals. In an effort to improve their system for recommending questions to volunteering professionals, CareerVillage partnered with Kaggle and Data Science for Good to challenge programmers around the globe with preparing a solution.

This paper describes the process our team followed in an attempt to apply classroom-based knowledge to real world problems that have potentially great societal impact. As students ourselves, we understood the pressure and confusion of selecting a “final” career path, and so felt compelled to apply ourselves to this challenge.

Volunteering professionals are to receive email subscriptions on a weekly to monthly basis containing new questions, ideally related to their industry. Using the account, question, and answer data provided by CareerVillage, our team has developed a simple, content based recommendation system that would provide ten new questions based on the professionals previous activity. This output could be used to ensure professionals remain active by continuing to recommend relevant questions, which helps students navigate their path to being future professionals. 

### Stats
Internal Imports from Anaconda
Language - Python, Version 3

#### Packages
Can be used with python's "import" function

Pandas (import pandas)

Numpy (import numpy)

Sklearn.metric.pairwise - cosine_similarity (from sklearn.metric.pairwise import cosine_similarity)

Sklearn.feature_extraction.text - CountVectoizer (from sklearn.feature_extraction.text import CountVectorizer)

Regex (import re)

CSV (import csv)

Collections - Counter (from collections import Counter)

nltk - Rake (installation instructions: https://pypi.org/project/rake-nltk/)

## Due Dates
All team submission emails should come from the team leads.
Be very careful to pay attention to all deadlines noted below. **There will be no allowances
for late turnins, including slip days.**
- [x] 3/21, 5pm - Link to the github page for your project via email
- [x] 3/28, 5pm – Selection notification of data set(s) via email
- [X] 4/7, 5pm – Selection of question to be answered, justification paper via email
- [x] 4/24, 5pm – Final clone of the github repository for all code and the final paper
- [x] 4/24, 5pm – Link for the clean dataset(s) via email or dataset available via github
- [ ] 4/24, 11:59pm – Team member reviews via email
- [ ] 4/24, 11:59pm – Presentation slides final clone
- [ ] 4/25, 2pm – Final presentations
