import csv
import pygsheets
gc = pygsheets.authorize("client_secret.json")
sponsor = input("what is the sponsor name?")
flour = input('what is the flour type?')
time = input('when did the experiment start? %Y-%m-%d-%H-%M')
fileName = sponsor+ '-'+flour+"-"+time
sh = gc.open(filename)
coverSheet = sh.worksheet_by_title('coverSheet')

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
