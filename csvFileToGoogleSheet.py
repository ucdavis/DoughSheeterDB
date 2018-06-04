import pygsheets
gc = pygsheets.authorize()

import csv
from datascience import *
import numpy as np

sh = gc.open('NewDoughSheet')
wks = sh.add_worksheet('Raw data', rows=33000, cols= 10)
#headers
wks.cell('A2').value = 'UnixTime'
wks.cell('B2').value = 'BeltNum'
wks.cell('C2').value = 'Direction'
wks.cell('D2').value = 'posNum'
wks.cell('E2').value = 'posLoc'
wks.cell('F2').value = 'height'

dataFile = make_array('inH_P1.csv','outH_P1.csv','inH_P2.csv','outH_P2.csv',
                      'outH_P2.csv', 'inH_P3.csv', 'outH_P3.csv', 
                      'inH_P4.csv','outH_P4.csv')
for file in np.arange(len(dataFile)):
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
    wks.append_table(start='A3', end='B33000', values=coordList, dimension='ROWS', overwrite=True)
