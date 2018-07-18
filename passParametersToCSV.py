import csv
import pygsheets
gc = pygsheets.authorize("client_secret.json")

sponsorType = input("what is the sponsor name? enter 1 if Ardent")
if sponsorType = "1":
	sponsor = "Ardent"
else:
	sponsor = sponsorType

flourType = input('what is the flour type? enter 1 for allPurpose; 2 for breadFlour ')
if flourType = "1":
	flour = "allPurpose"
else if flourType = "2":
	flour = "breadFlour"
else:
	flour = flourType

time = input('when did the experiment start? %Y-%m-%d-%H-%M')
fileName = sponsor+ '-'+flour+"-"+time
sh = gc.open(filename)
coverSheet = sh.worksheet_by_title('coverSheet')

# write parameters to csv files
with open('parameters.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    #first row - dateAndTime, number of passes
    writer.writerow([coverSheet.cell('B5').value, int(coverSheet.cell('B9').value)])
    #every row is parameters for one pass: direction, roller gap, roller speed, belt0speed, belt1speed
    # direction =1, belt1 to belt0; direction = 2, belt0 to belt 1
    passNumber = int(coverSheet.cell('B9').value)
    for i in np.arange(passNumber):
        parameter = [(i%2+1), int(coverSheet.cell('I'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('J'+str(i+2)).value), int(coverSheet.cell('G'+str(i+2)).value)]
        parameter += [int(coverSheet.cell('E'+str(i+2)).value)]
        writer.writerow(parameter)
# write experiment entry to master experiment list
shID = sh.id
master = gc.open("Experiment master list")
masterID = master.id
sponsorSh = gc.open(sponsor + "experiment list")
coverSheet = sh.worksheet_by_title('coverSheet')
passNumber = int(coverSheet.cell('B9').value)

experimentRow = [sponsor, time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
expSh = master.worksheet_by_title("Experiment")
expSh.append_table(start='A21', end='G70000', values=experimentRow, dimension='ROWS', overwrite=False)
sponsorExperimentSheet = sponsorSh.worksheet_by_title("Experiment")
sponsorExpRow = [time, flour, passNumber, ('https://docs.google.com/spreadsheets/d/'+shID)]
sponsorExperimentSheet.append_table(start='A21', end='G70000', values=sponsorExpRow, dimension='ROWS', overwrite=False)

