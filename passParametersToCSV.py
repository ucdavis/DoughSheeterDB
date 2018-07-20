#Library to write and edit csv files
import csv
#Library to link to google sheets with google API
import pygsheets
#Link to google api and allow access/create/edit google sheet
gc = pygsheets.authorize("client_secret.json")

# Experiment enter meta-data (sponsor name, flour type, the time the experiment starts)
# all meta-data is the concatenated and become the title of the google workbook for the experiment
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
time = input('when did the experiment start? %Y-%m-%d-%H-%M')
fileName = sponsor+ '-'+flour+"-"+time

# open google workbook by its title
sh = gc.open(filename)
# access coverSheet in the workbook by calling its name
coverSheet = sh.worksheet_by_title('coverSheet')

# create a new csv file
# write the experiment parameters(pass number, speed, gap) to csv files

with open('parameters.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # the first row of the parameter.csv recorded the date and time for the experiment and number of passes
    writer.writerow([coverSheet.cell('B5').value, int(coverSheet.cell('B9').value)])
    # every row after the first row records the parameters for one pass correspondingly: 
    # direction, roller gap, roller speed, belt0speed, belt1speed
    # direction =1, belt1 to belt0; direction = 2, belt0 to belt 1
    passNumber = int(coverSheet.cell('B9').value)
    for i in np.arange(passNumber):
        parameter = [(i%2+1), int(coverSheet.cell('I'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('J'+str(i+2)).value), int(coverSheet.cell('G'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('E'+str(i+2)).value)]
        writer.writerow(parameter)

# document the experiment workbook address and its meta-data into two "experiment list" sheets for future references
# access the two experiment list sheet("Experiment master list" and sponsor "experiment list")
# get the workbook id and sotre the pass number of the experiment
shID = sh.id
master = gc.open("Experiment master list")
masterID = master.id
sponsorSh = gc.open(sponsor + "experiment list")
coverSheet = sh.worksheet_by_title('coverSheet')
passNumber = int(coverSheet.cell('B9').value)

# write experiment sponsor name, time, type of flour, pass number, and url of the workbook to the "master experiment list" sheet
# write experiment time, type of flour, pass number, and url of the workbook to the "sponsor's experiment list" sheet
experimentRow = [sponsor, time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
expSh = master.worksheet_by_title("Experiment")
expSh.append_table(start='A21', end='G70000', values=experimentRow, dimension='ROWS', overwrite=False)
sponsorExperimentSheet = sponsorSh.worksheet_by_title("Experiment")
sponsorExpRow = [time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
sponsorExperimentSheet.append_table(start='A21', end='G70000', values=sponsorExpRow, dimension='ROWS', overwrite=False)

