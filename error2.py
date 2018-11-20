import pygsheets
gc = pygsheets.authorize("client_secret.json")

import csv
from datascience import *
import numpy as np
import webbrowser

# access google workbook
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

time = input("when did you run the experiment? yyyy-mm-dd-hh-mm")
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
path = "data/"+input("where is your data stored? yyyy-mm-dd-hh-mm")


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

template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
inHeightID = template.worksheet_by_title('inHeight').id
inHeight = sh.add_worksheet('inHeight', rows=15000, cols=6, src_tuple=[templateID,inHeightID], index=4)
outHeightID = template.worksheet_by_title('outHeight').id
outHeight = sh.add_worksheet('outHeight', rows=15000, cols=6, src_tuple=[templateID,outHeightID], index=6)
