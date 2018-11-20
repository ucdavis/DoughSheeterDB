#Libraries for handling datastructures - array, list
from datascience import *
import numpy as np
#Library to open url links in code
import webbrowser

# This code performs following tasks:
# Connects to google drive
# Creates a new google sheet for the experiment(s)
# and writes data to it.

# Creating a connection to the drive , Authorization function takes the key file as parameter.
gc = pygsheets.authorize("client_secret.json")

#Query User for experiment meta-data : Sponsor Name and Flour type. Time of experiment is System time.
sponsorType = input("what is the sponsor name? enter 1 if Ardent")
if sponsorType == "1":
	sponsor = "Ardent"
else:
	sponsor = sponsorType

flourType = input('what is the flour type? enter 1 for allPurpose; 2 for breadFlour ')
if flourType == "1":
	flour = "allPurpose"
elif flourType == "2":
	flour = "breadFlour"
else:
	flour = flourType

time = datetime.now().strftime('%Y-%m-%d-%H-%M')


#Concatenate meta-data(sponsor+flour+time) to create file name of google sheet
# to which experiment data will be stored.
fileName = sponsor+ '-'+flour+"-"+time

#Store newly created file in folder specific to the Sponsor
#Any new sponsors should be added here
#Each folder is identified by folder address, which is found in the the googledrive hyperlink.
if sponsor == "Ardent":
    parent = "1cMT_LlBnU2BDa0T0Fti6uVoewEHV3ll-"
else:
    parent = "1YVG4T-0uPaubnIIi0-rMgUItSDt67OOm"
sh = gc.create(fileName, parent_id = parent)

with open('SpreadsheetKey.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Store the key of the spreadsheet in csv file
    writer.writerow([sh.id,sponsor])

# Access Template Spreadsheet to copy to new google sheet - "Cover Sheet" and "Parameter choices"
# These are standard sheets for every experiment and contain data about experimental settings and materials
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
#copy parameter choices
paraChID = template.worksheet_by_title('parameter choices').id
sh.add_worksheet('parameter choices', rows=100, cols=10, src_tuple=[templateID,paraChID], index=2)
coverFrTemplateID = template.worksheet_by_title('coverSheet').id
coverSheet = sh.add_worksheet('coverSheet', rows=100, cols=10, src_tuple=[templateID,coverFrTemplateID], index=1)
coverSheet.update_cell("B5", time)
print ("fill out cover sheet")
# delete blank sheet1
sheet1 = sh.sheet1
sh.del_worksheet(sheet1)
# open coverSheet
shID = sh.id
webbrowser.open('https://docs.google.com/spreadsheets/d/'+shID)

input("Have you filled out the cover sheet? Enter anything for yes")

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