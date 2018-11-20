import pygsheets
#Library for array manipulation
import numpy as np
#Link to google api and allow access/create/edit google sheet
gc = pygsheets.authorize("client_secret.json")

#This code reads experiments parameters from google sheets and  
# saves to csv for easier passing of variables to runDoughSheeterWithParams.py 


# Experiment enter meta-data (sponsor name, flour type, the time the experiment starts)
# all meta-data is the concatenated and become the title of the google workbook for the experiment
with open('SpreadsheetKey.csv', 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    key=[row for row in csv_reader]
    print (key)

sh = gc.open_by_key(key[0][0])
sponsor = key[0][1]

# use handle to access coverSheet in the workbook 
coverSheet = sh.worksheet_by_title('coverSheet')

# create a new csv file
# write the experiment parameters(pass number, speed, gap) from google cover sheet to local(to ubuntu box) csv file

with open('parameters.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # the first row of the parameter.csv recorded the date and time for the experiment and number of passes
    writer.writerow([coverSheet.cell('B5').value, int(coverSheet.cell('B9').value)])
    # every row after the first row records the parameters for one pass correspondingly: 
    # direction, roller gap, roller speed, belt0speed, belt1speed
    # direction =1, belt1 to belt0; direction = 2, belt0 to belt 1
    passNumber = int(coverSheet.cell('B9').value)
    for i in np.arange(passNumber):
        parameter = [i+1,(i%2+1), int(coverSheet.cell('I'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('J'+str(i+2)).value), int(coverSheet.cell('G'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('E'+str(i+2)).value)]
        print ("Writing row to parameter.csv " +str(parameter))
        writer.writerow(parameter)

# Record address for this experiment workbook and its meta-data, to 2 Master lists sheets 
# Experiment Master List - Has record of all experiments performed, Sponsor Experiment List - Subset of Master specific to sponsor
# Access the two experiment list sheet("Experiment master list" and sponsor "experiment list")
# Get the workbook id and read&save the pass number of the experiment
shID = sh.id
master = gc.open("Experiment master list")
masterID = master.id
sponsorSh = gc.open(sponsor + " experiment list")
coverSheet = sh.worksheet_by_title('coverSheet')
passNumber = int(coverSheet.cell('B9').value)
time = coverSheet.cell('B5').value
flour = coverSheet.cell('B7').value

# write experiment sponsor name, time, type of flour, pass number, and url of the workbook to the "master experiment list" sheet
# write experiment time, type of flour, pass number, and url of the workbook to the "sponsor's experiment list" sheet
experimentRow = [sponsor, time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
expSh = master.worksheet_by_title("Experiment")
expSh.append_table(start='A21', end='G70000', values=experimentRow, dimension='ROWS', overwrite=False)
sponsorExperimentSheet = sponsorSh.worksheet_by_title("Experiment")
sponsorExpRow = [time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
sponsorExperimentSheet.append_table(start='A21', end='G70000', values=sponsorExpRow, dimension='ROWS', overwrite=False)