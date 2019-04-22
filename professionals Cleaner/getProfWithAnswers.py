# Creates a CSV of all professionals who have answered questions
# Each row includes a professionals information from the professionals CSV and a list of all their answers text
# Professionals who are not copied over have their professional_id's stored in a text document

import pandas as pd
import datetime
import csv

# load in professional and answer csv
prof_csv = pd.read_csv("professionalsCLEAN.csv") # professionals dataset cleaned by Sebastian
answers_csv = pd.read_csv("D:/DS-CSVs/answers.csv")
answers_df = pd.DataFrame(answers_csv)

csvFile = open("professionals_with_answers.csv", 'a') # csv to write professionals to
file = open("deletedProfessionalsID_2.txt", "a") # text file to record deleted professionals

csvWriter = csv.writer(csvFile)

# creates new row with the needed column titles
csvWriter.writerow(['professionals_id', 'professionals_location', 'professionals_industry', 'professionals_headline', 'professionals_date_joined', 'answers_text'])

print('Processing Professionals...')

# iterate through professionals and filter out individuals who have not answered a question in a specific amount of time
for i in range(len(prof_csv)):
    id = prof_csv.loc[i]['professionals_id'] # professionals account id
    answers_text = [] # holds all the professionals answers
    prof_df = prof_csv.loc[i] # professionals row from prof_csv

    if answers_df.loc[answers_df["answers_author_id"]==id].empty: # if prof's id isnt in the answers csv, then they have neve answered a question
        # add them the the deleted profs text file
        file.write(prof_csv.loc[i]['professionals_id'])
        file.write('\n')
    else:
        answers = answers_df.loc[answers_df["answers_author_id"]==id]
        # compile all the professionals answers
        for answer in answers.itertuples():
            answers_text.append(answer[5])
        #add the answers text to the professionals information row
        prof_df["answers_text"] = answers_text
        # record the prof's information
        csvWriter.writerow(prof_df)

csvFile.close()
file.close()
print("Finished.")
