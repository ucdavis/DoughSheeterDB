import pygsheets
gc = pygsheets.authorize("client_secret.json")

import csv
from datascience import *
import numpy as np
import webbrowser

#access google workbook
sponsorType = input("what is the sponsor name? enter 1 if Ardent")
if sponsorType == "1":
    sponsor = "Ardent"
else:
    sponsor = sponsorType
flourType = input('what is the flour type? enter 1 for allPurpose; 2 for breadFlour ')
if flourType == "1":
    flour = "allPurpose"
else if flourType == "2":
    flour = "breadFlour"
else:
    flour = flourType

time = input("when did you run")
fileName = sponsor+ '-'+flour+"-"+time
sh = gc.open(fileName)
coverSheet = sh.worksheet_by_title("coverSheet")

# add raw data sheet
rawData = sh.add_worksheet('rawData', rows=24000, cols = 7, index =2)

#add header and upload csv files
rawData.cell('A1').value = 'unixTime'
rawData.cell('B1').value = 'posNum'
rawData.cell('C1').value = 'posLoc'
rawData.cell('D1').value = 'height'
rawData.cell('E1').value = 'passNum'
rawData.cell('F1').value = 'beltNum'
rawData.cell('G1').value = 'direction'

#add columns and header to height csv file
numPasses = int(coverSheet.cell("B9").value)
files = make_array()
inFile = make_array()
outFile = make_array()
for i in np.arange(numPasses):
    baseString = "H_P" +str(i+1)+".csv"
    inString = "in"+baseString
    outString = "out" + baseString
    inFile = np.append(inFile, inString)
    outFile = np.append(outFile, outString)
    files = np.append(files, inString)
    files = np.append(files, outString)
    
#find the path for where the data stored
path = "data/"+input("when did you start the experiment? yyyy-mm-dd-hh-mm")

#edit all the inFile
for a in np.arange(len(inFile)):
    with open(path+"/"+inFile.item(a), newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        new_data = []
        passnum = a+1
        if a%2==0:
            beltnum = 1
        else:
            beltnum = 0
        for i, item in enumerate(data):
            item.append(passnum)
            item.append(beltnum)
            item.append('in')
            new_data.append(item)
    with open(path+"/"+inFile.item(a),'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
        w.writerows(data)
    print (inFile.item(a))

for a in np.arange(len(outFile)):
    with open(path+"/"+outFile.item(a), newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        new_data = []
        passnum = a+1
        if a%2==0:
            beltnum = 0
        else:
            beltnum = 1
        for i, item in enumerate(data):
            item.append(passnum)
            item.append(beltnum)
            item.append('out')
            new_data.append(item)
    with open(path+"/"+outFile.item(a),'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
        w.writerows(data)
    print (outFile.item(a))
    
#appending all csv files
def append_csv_file(file):
    csvData = open(file, 'r')
    csvReader = csv.reader(csvData)
    header = next(csvReader)
    heightIndex = header.index('height')
    timeIndex = header.index('unixTime')
    directionIndex = header.index('direction')
    posNumIndex = header.index('posNum')
    posLocIndex = header.index('posLoc')
    beltNumIndex = header.index('beltNum')
    passNumIndex=header.index('passNum')
    coordList = []
    for row in csvReader:
        time=row[timeIndex]
        height = row[heightIndex]
        direction = row[directionIndex]
        passNum = row[passNumIndex]
        posNum = row[posNumIndex]
        posLoc = row[posLocIndex]
        beltNum = row[beltNumIndex]
        coordList.append([time, posNum,posLoc,height, passNum, beltNum, direction])
    rawData.append_table(start='A2', end='G70000', values=coordList, dimension='ROWS', overwrite=False)
for i in np.arange(len(files)):
    append_csv_file(path+"/"+files.item(i))
    print (files.item(i))
    
# adding columns to VF and append it to google sheet
with open(path+"/"+'VF.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(path+"/"+'VF.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','force'])
    w.writerows(data)
forceData = sh.add_worksheet('rawDataForce', rows=2000, cols=2, index=3)
forceData.cell('A1').value = 'unixTime' 
forceData.cell('B1').value = 'verticalForce'

csvData = open(path+'/'+'VF.csv', 'r')
csvReader = csv.reader(csvData)
header = next(csvReader)
timeIndex = header.index('unixTime')
forceIndex = header.index('force')
coordList = []
for row in csvReader:
    time=row[timeIndex]
    force = row[forceIndex]
    coordList.append([time, force])
forceData.append_table(start='A2', end='B2000', values=coordList, dimension='ROWS', overwrite=False)

#add data sheets for filtering data, finding averages, and doing analysis
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
inHeightID = template.worksheet_by_title('inHeight').id
inHeight = sh.add_worksheet('inHeight', rows=15000, cols=6, src_tuple=[templateID,inHeightID], index=4)
inHeightAvgID = template.worksheet_by_title('inHeightAvg').id
inHeight = sh.add_worksheet('inHeightAvg', rows=15000, cols=6, src_tuple=[templateID,inHeightAvgID], index=5)

#add data sheets for filtering data, finding averages, and doing analysis
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
inHeightID = template.worksheet_by_title('inHeight').id
inHeight = sh.add_worksheet('inHeight', rows=15000, cols=6, src_tuple=[templateID,inHeightID], index=4)
inHeightAvgID = template.worksheet_by_title('inHeightAvg').id
inHeight = sh.add_worksheet('inHeightAvg', rows=15000, cols=6, src_tuple=[templateID,inHeightAvgID], index=5)
print ("inHeight done")
outHeightID = template.worksheet_by_title('outHeight').id
outHeight = sh.add_worksheet('outHeight', rows=15000, cols=6, src_tuple=[templateID,outHeightID], index=6)
outHeightAvgID = template.worksheet_by_title('outHeightAvg').id
outHeightAvg = sh.add_worksheet('outHeightAvg', rows=15000, cols=6, src_tuple=[templateID,outHeightAvgID], index=7)
print ("outHeight done")
vFID = template.worksheet_by_title('VF').id
forceData = sh.add_worksheet('VF', rows=2000, cols=2, src_tuple=[templateID,vFID], index=8)
print("force done")
consolidateID = template.worksheet_by_title('consolidatedData').id
consolidate = sh.add_worksheet('consolidatedData', rows=2000, cols=8, src_tuple=[templateID,consolidateID], index=9)

analysisID= template.worksheet_by_title('analysis').id
analysis = sh.add_worksheet('analysis', rows=15000, cols=6, src_tuple=[templateID,analysisID], index=10)
print("analysis done" )
visualizationFrTempID = template.worksheet_by_title('visualization').id
visualization = sh.add_worksheet('visualization', rows=2000, cols=5, src_tuple=[templateID, visualizationFrTempID], index=10)
visualID = sh.worksheet_by_title('visualization').id
print ("visualization done" )
#open visualization in webbrowser
shID = sh.id
webbrowser.open('https://docs.google.com/spreadsheets/d/'+shID +'/edit#gid='+str(visualID)) )

#open visualization in webbrowser
shID = sh.id
webbrowser.open('https://docs.google.com/spreadsheets/d/'+shID +'/edit#gid='+str(visualizationID)) 
#sharing to operator and sponsor by email
operatorEmail = coverSheet.cell('C2').value
sh.share(operatorEmail)
sponsorEmail = coverSheet.cell('C4').value
sh.share(sponsorEmail)
