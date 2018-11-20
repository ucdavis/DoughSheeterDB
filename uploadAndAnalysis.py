# Library to access/edit/save googlesheets
import pygsheets
# Library to read and edit csv files
import csv
# Libraries for handling datastructures - array, list
from datascience import *
import numpy as np
# Library to open url links in code
import webbrowser


#Creating a connection to the drive , Authorization function takes the key file as parameter.
gc = pygsheets.authorize("client_secret.json")

#Query User for experiment meta-data : Sponsor Name and Flour type. Time of experiment is the time User started the experiment
#concatenate the meta-data and form title for the experiment workbook
#access existing google workbook with the experiment title

with open('SpreadsheetKey.csv', 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    key=[row for row in csv_reader]
    print (key)

sh = gc.open_by_key(key[0][0])
coverSheet = sh.worksheet_by_title("coverSheet")
time = coverSheet.cell('B5').value
flour = coverSheet.cell('B7').value

# add empty raw data sheet to the experiment workbook
rawData = sh.add_worksheet('rawData', rows=24000, cols=7, index=2)

# filling out raw data sheet
# add header to the rawData sheet
rawData.cell('A1').value = 'unixTime'
rawData.cell('B1').value = 'posNum'
rawData.cell('C1').value = 'posLoc'
rawData.cell('D1').value = 'height'
rawData.cell('E1').value = 'passNum'
rawData.cell('F1').value = 'beltNum'
rawData.cell('G1').value = 'direction'

# write an array of file names that will later be used to access raw data files
# inFile is the array of inHeight data files
# outFile is the array of outHeight data files
# files include both inFile and outFile
numPasses = int(coverSheet.cell("B9").value)
files = make_array()
inFile = make_array()
outFile = make_array()
for i in np.arange(numPasses):
    baseString = "H_P" + str(i + 1) + ".csv"
    inString = "in" + baseString
    outString = "out" + baseString
    inFile = np.append(inFile, inString)
    outFile = np.append(outFile, outString)
    files = np.append(files, inString)
    files = np.append(files, outString)

# find the path to where the data stored on the local computer
# the path is "data/yyyy-mm-dd-hh-mm", which is when the experiment is started
path = "data/" + input("where is your data stored? yyyy-mm-dd-hh-mm")

# read and store every files in inFile in a list called "data"
# edit all the inFile by appending "in" as the direction, pass number, and belt number according to its pass number to each row
# enumerate data and update all the rows with the additional meta-data
# open the same file in inFile, write the header, and overwrite each rows with new_data
# For index "a", pass number will be "a+1" since np.arange(a) starts with 0, 1, 2, a-1
# pass number is a+1; for an even "a" value, belt number is 1 since the machine always start at the belt1 side
for a in np.arange(len(inFile)):
    with open(path + "/" + inFile.item(a), newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        new_data = []
        passnum = a + 1
        if a % 2 == 0:
            beltnum = 1
        else:
            beltnum = 0
        for i, item in enumerate(data):
            item.append(passnum)
            item.append(beltnum)
            item.append('in')
            new_data.append(item)
    print("Modifying raw data files for analysis and processing; adding passNum, beltNum, direction")
    with open(path + "/" + inFile.item(a), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['unixTime', 'posNum', 'posLoc', 'height', 'passNum', 'beltNum', 'direction'])
        w.writerows(data)
    print(inFile.item(a))

# read and store every files in outFile in a list called "data"
# edit all the inFile by appending "out" as the direction, pass number, and belt number according to its pass number to each row
# enumerate data and update all the rows with the additional meta-data
# open the same file in outFile, write the header, and overwrite each rows with new_data
# For index "a", pass number will be "a+1" since np.arange(a) is 0, 1, 2... a-1
for a in np.arange(len(outFile)):
    with open(path + "/" + outFile.item(a), newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        new_data = []
        passnum = a + 1
        if a % 2 == 0:
            beltnum = 0
        else:
            beltnum = 1
        for i, item in enumerate(data):
            item.append(passnum)
            item.append(beltnum)
            item.append('out')
            new_data.append(item)
    with open(path + "/" + outFile.item(a), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['unixTime', 'posNum', 'posLoc', 'height', 'passNum', 'beltNum', 'direction'])
        w.writerows(data)
    print(outFile.item(a))


# a method to append csv file on rawData sheet
# parameter "file" is the name of the file that will be appended on rawData sheet
def append_csv_file(file):
    # read the csv file from the method's parameter
    csvData = open(file, 'r')
    csvReader = csv.reader(csvData)
    # next() skip the header of the csv file
    header = next(csvReader)
    heightIndex = header.index('height')
    timeIndex = header.index('unixTime')
    directionIndex = header.index('direction')
    posNumIndex = header.index('posNum')
    posLocIndex = header.index('posLoc')
    beltNumIndex = header.index('beltNum')
    passNumIndex = header.index('passNum')
    # coordList is a list to store the csv file into a 2-D list by using a for loop
    coordList = []
    for row in csvReader:
        time = row[timeIndex]
        height = row[heightIndex]
        direction = row[directionIndex]
        passNum = row[passNumIndex]
        posNum = row[posNumIndex]
        posLoc = row[posLocIndex]
        beltNum = row[beltNumIndex]
        coordList.append([time, posNum, posLoc, height, passNum, beltNum, direction])
    # append_table() append the coordList, which is the csv file on rawData sheet without overwriting any rows
    rawData.append_table(start='A2', end='G70000', values=coordList, dimension='ROWS', overwrite=False)


print("Uploading data files to google sheet")
# append all csv file in the "files" array by using a for loop
for i in np.arange(len(files)):
    append_csv_file(path + "/" + files.item(i))
    print(files.item(i))

# read from the vertical force csv file and store the file into a 2-D list called "data"
# add the header to the vertical force csv file, then add all the rows in the "data" list
# save header and the vertical force data in the original VF.csv
# create a raw force data sheet
# write header "unixTime" and "vertical Force"
with open(path + "/" + 'VF.csv', newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(path + "/" + 'VF.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime', 'force'])
    w.writerows(data)
forceData = sh.add_worksheet('rawDataForce', rows=2000, cols=2, index=3)
forceData.cell('A1').value = 'unixTime'
forceData.cell('B1').value = 'verticalForce'

# use csv.reader to read the VF.csv
# next() skipped the header in the csv file
# store the column index into variables: timeIndex, forceIndex
# coordList is a 2-D list that save all the rows in VF.csv
# append_table is used to append all rows in coordList
csvData = open(path + '/' + 'VF.csv', 'r')
csvReader = csv.reader(csvData)
header = next(csvReader)
timeIndex = header.index('unixTime')
forceIndex = header.index('force')
coordList = []
for row in csvReader:
    time = row[timeIndex]
    force = row[forceIndex]
    coordList.append([time, force])
forceData.append_table(start='A2', end='B2000', values=coordList, dimension='ROWS', overwrite=False)

# open the template workbook and get its ID
# used inHeight, inHeightAvg, outHeight, outHeightAvg, and VF sheet's id from the template and add the same sheets to
# the new experiment workbook so that the in/outHeight is first filtered by Height value that is greater than 2.5 mm and
# then average by slice
# and vertical force that is positive
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
inHeightID = template.worksheet_by_title('inHeight').id
inHeight = sh.add_worksheet('inHeight', rows=15000, cols=6, src_tuple=[templateID, inHeightID], index=4)
inHeightAvgID = template.worksheet_by_title('inHeightAvg').id
inHeight = sh.add_worksheet('inHeightAvg', rows=15000, cols=6, src_tuple=[templateID, inHeightAvgID], index=5)
print("inHeight done")
outHeightID = template.worksheet_by_title('outHeight').id
outHeight = sh.add_worksheet('outHeight', rows=15000, cols=6, src_tuple=[templateID, outHeightID], index=6)
outHeightAvgID = template.worksheet_by_title('outHeightAvg').id
outHeightAvg = sh.add_worksheet('outHeightAvg', rows=15000, cols=6, src_tuple=[templateID, outHeightAvgID], index=7)
print("outHeight done")
vFID = template.worksheet_by_title('VF').id
forceData = sh.add_worksheet('VF', rows=2000, cols=2, src_tuple=[templateID, vFID], index=8)
print("force done")

# used consolidatedData sheet from the template to add the same sheet to new experiment workbook
# queries and formulas in the sheet will query the average height and force per pass along with the time for in and out per pass
consolidateID = template.worksheet_by_title('consolidatedData').id
consolidate = sh.add_worksheet('consolidatedData', rows=2000, cols=8, src_tuple=[templateID, consolidateID], index=9)

# analysis sheet from the template workbook is copied into the new experiment workbook by finding its sheet ID
# analysis sheet has formulas and charts to create stress-strain curve, and recovery-stress curve
analysisID = template.worksheet_by_title('analysis').id
analysis = sh.add_worksheet('analysis', rows=15000, cols=6, src_tuple=[templateID, analysisID], index=10)
print("analysis done")
# visualization sheet has three queries that append all in/outHeight and force data with its timestamp
# it is copied from the template sheet with its id
# two chart will be created, one is the height and force vs time, and the other is width and force vs time
visualizationFrTempID = template.worksheet_by_title('visualization').id
visualization = sh.add_worksheet('visualization', rows=2000, cols=5, src_tuple=[templateID, visualizationFrTempID],
                                 index=10)
visualID = sh.worksheet_by_title('visualization').id
print("visualization done")

# open visualization in webbrowser
shID = sh.id
webbrowser.open('https://docs.google.com/spreadsheets/d/' + shID + '/edit#gid=' + str(visualID))

# access the cells that store email of the operator and sponsor in the coverSheet
# share() method shares the workbook with the email address given in the parameter
# sharing to operator and sponsor by email
operatorEmail = coverSheet.cell('C2').value
sh.share(operatorEmail)
sponsorEmail = coverSheet.cell('C4').value
sh.share(sponsorEmail)