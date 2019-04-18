import pandas as pd
import datetime
import csv

# load in professional and answer csv
prof_csv = pd.read_csv("professionalsCLEAN.csv") # professionals dataset cleaned by Sebastian
answers_csv = pd.read_csv("D:/DS-CSVs/answers.csv")
answers_df = pd.DataFrame(answers_csv)

csvFile = open("new_professionals.csv", 'a') # csv to write professionals to
file = open("deletedProfessionalsID.txt", "a") # text file to record deleted professionals

csvWriter = csv.writer(csvFile)

#creates new row with the needed column titles
csvWriter.writerow(['professionals_id', 'professionals_location', 'professionals_industry', 'professionals_headline', 'professionals_date_joined'])

print('Processing Professionals...')

# iterate through professionals and filter out individuals who have not answered a question in a specific amount of time
for i in range(len(prof_csv)):
    keep_prof = False
    id = prof_csv.loc[i]['professionals_id'] # professionals account id
    date_joined = prof_csv.loc[i]['professionals_date_joined'] # date the professional created their account
    current_year = int(datetime.datetime.now().year) # current year
    current_month = int(datetime.datetime.now().month) # current month

    # if date joined is within four months of current date, we can keep the professional
    if int(str(date_joined)[0:4])-current_year == 0 and current_month- int(str(date_joined)[5:7]) <= 4:
        keep_prof = True
    else:
        # iterate through answers
        for answer in answers_df.itertuples():
            answer_year = int(str(answer[4])[0:4]) # year answer was submitted
            if id == answer[2] and current_year - answer_year <= 2: # check if answer is by the current professional and <= 2 years old
                keep_prof = True
                break # break out of answers iteration if an answer within the specified constraints are found

    if keep_prof: # add professionals information to csv file
        csvWriter.writerow(prof_csv.loc[i])
    else: # add professionals id to list of deleted professionals
        file.write(prof_csv.loc[i]['professionals_id'])
        file.write('\n')

csvFile.close()
file.close()
print("Finished.")
