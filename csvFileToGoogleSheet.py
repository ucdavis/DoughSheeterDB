import pygsheets
gc = pygsheets.authorize()

import csv
from datascience import *
import numpy as np

sh = gc.open('NewDoughSheet')
wks = sh.add_worksheet('Raw data', rows=33000, cols= 10)
#headers
wks.cell('A2').value = 'UnixTime'
wks.cell('B2').value = 'posNum'
wks.cell('C2').value = 'posLoc'
wks.cell('D2').value = 'height'
wks.cell('E2').value = 'pass'
wks.cell('F2').value = 'beltNum'
wks.cell('G2').value = 'direction'


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
    coordList = []
    for row in csvReader:
        time=row[timeIndex]
        height = row[heightIndex]
        direction = row[directionIndex]
        posNum = row[posNumIndex]
        posLoc = row[posLocIndex]
        beltNum = row[beltNumIndex]
        coordList.append([time,beltNum, direction, posNum,posLoc,height])
    rawData.append_table(start='A2', end='G70000', values=coordList, dimension='ROWS', overwrite=False)

numPasses = 4
files = make_array()
for i in np.arange(numPasses):
  baseString = "H_P" +str(i+1)+".csv"
  inString = "in"+baseString
  outString = "out" + baseString
  files = np.append(files, inString)
  files = np.append(files, outString)
  
for i in np.arange(len(files)):
    append_csv_file(files.item(i))

