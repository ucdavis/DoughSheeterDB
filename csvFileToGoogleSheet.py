import pygsheets
gc = pygsheets.authorize()

import csv
from datascience import *
import numpy as np

sh = gc.open('NewDoughSheet')
wks = sh.add_worksheet('Raw data', rows=33000, cols= 10)

dataFile = make_array('inH_P1.csv','outH_P1.csv','inH_P2.csv','outH_P2.csv',
                      'outH_P2.csv', 'inH_P3.csv', 'outH_P3.csv', 
                      'inH_P4.csv','outH_P4.csv')
for file in np.arange(len(dataFile)):
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
    print (len(coordList))
    lenFile = len(coordList)

    wks.append_table(start='A3', end='B81', values=coordList, dimension='ROWS', overwrite=True)