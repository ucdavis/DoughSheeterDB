import pygsheets
gc = pygsheets.authorize()

import csv
from datascience import *
import numpy as np


sh = gc.create('template')
#create(title, parent_id=None)

sheet1 = sh.worksheet_by_title('Sheet1')
template = gc.open('SponsorCode-DoughVariety-yyyymmdd-HH:mm').id

coverFrTemplate= gc.open_by_key(template).worksheet_by_title('CoverSheet')
coverFrTemplateID = coverFrTemplate.id

#adding worksheets to the spreadsheet
coverSheet = sh.add_worksheet('CoverSheet', rows=100, cols=10, src_tuple=[template,coverFrTemplateID], index=1)
analysis = sh.add_worksheet('Analysis', rows=100, cols=10, index=2)
rawData = sh.add_worksheet('RawData', rows=33000, cols = 10, index =3)
sh.del_worksheet(sheet1)

#add headers to raw data sheet
rawData.cell('A1').value = 'unixTime'
rawData.cell('B1').value = 'posNum'
rawData.cell('C1').value = 'posLoc'
rawData.cell('D1').value = 'height'
rawData.cell('E1').value = 'passNum'
rawData.cell('F1').value = 'beltNum'
rawData.cell('G1').value = 'direction'

#add columns and header to height csv file
numPasses = 4
files = make_array()
inFile = make_array()
outFile = make_array()
for i in np.arange(numPasses):
    baseString = "H_P" +str(i+1)+".csv"
    inString = "in"+baseString
    outString = "out" + baseString
    inFile = np.append(inFile, instring)
    outFile = np.append(outFile, outString)
    files = np.append(files, inString)
    files = np.append(files, outString)
  
with open('inH_P1.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 1
    beltnum = 1
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('in')
        new_data.append(item)
with open('inH_P1.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)

with open('outH_P1.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 1
    beltnum = 0
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('out')
        new_data.append(item)
with open('outH_P1.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])

with open('InH_P2.csv',newline='') as a:
    r = csv.reader(a)
    data = [line for line in r]
    new_data = []
    passnum = 2
    beltnum = 0
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('in')
        new_data.append(item)
with open('InH_P2.csv','w',newline='') as a:
    w = csv.writer(a)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)
    
with open('outH_P2.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 2
    beltnum = 1
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('out')
        new_data.append(item)
with open('outH_P2.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)
    
with open('inH_P3.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 3
    beltnum = 1
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('in')
        new_data.append(item)
with open('inH_P3.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)

with open('outH_P3.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 3
    beltnum = 0
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('out')
        new_data.append(item)
with open('outH_P3.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)

with open('inH_P4.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 4
    beltnum = 0
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('in')
        new_data.append(item)
with open('inH_P4.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)

with open('outH_P4.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
    new_data = []
    passnum = 4
    beltnum = 1
    for i, item in enumerate(data):
        item.append(passnum)
        item.append(beltnum)
        item.append('out')
        new_data.append(item)
with open('outH_P4.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','posNum', 'posLoc','height','passNum', 'beltNum', 'direction'])
    w.writerows(data)
    
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
    append_csv_file(files.item(i))


#filter the height and find the average
averageHID = gc.open_by_key(template).worksheet_by_title('averageHeight').id
averageH= sh.add_worksheet('averageHeight', rows=40000, cols=6, src_tuple=[template,averageHID], index=4)

#add header and upload force data
with open('VF.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('VF.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['unixTime','force'])
    w.writerows(data)
forceData = sh.add_worksheet('rawDataForce', rows=2000, cols=8, index=5)
forceData.cell('A1').value = 'unixTime' 
forceData.cell('B1').value = 'verticalForce'

csvData = open('VF.csv', 'r')
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

operatorEmail = coverSheet.cell('C2').value
sh.share(operatorEmail)
sponsorEmail = coverSheet.cell('C4').value
sh.share(sponsorEmail)

#getting the speed for belts and roller from the cover sheet
belt1P1 = int(coverSheet.cell('C12').value )
belt1P2 = int(coverSheet.cell('D12').value )
belt1P3 = int(coverSheet.cell('E12').value )
belt1P4 = int(coverSheet.cell('F12').value )
belt0P1 = int(coverSheet.cell('C14').value)
belt0P2 = int(coverSheet.cell('D14').value)
belt0P3 = int(coverSheet.cell('E14').value)
belt0P4 = int(coverSheet.cell('F14').value)
rollerP1= int(coverSheet.cell('C16').value)
rollerP2= int(coverSheet.cell('D16').value)
rollerP3= int(coverSheet.cell('E16').value)
rollerP4= int(coverSheet.cell('F16').value)
