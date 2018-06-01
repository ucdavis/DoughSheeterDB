import pygsheets
gc = pygsheets.authorize()

import csv

sh = gc.open('NewDoughSheet')

wks = sh.add_worksheet('New Dough3', rows=8000, cols= 10)

wks.cell('B2').value = 'UnixTime'
wks.cell('C2').value = 'BeltNum'
wks.cell('D2').value = 'Direction'
wks.cell('E2').value = 'posNum'
wks.cell('F2').value = 'posLoc'
wks.cell('G2').value = 'height'

gpsTrack = open('/Users/karissaxu/Msdoughsheeter code/ImportEg.csv', 'r')
csvReader = csv.reader(gpsTrack)
header = next(csvReader)
header[0]

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

wks.resize(rows=lenFile+5, cols =10 )

wks.append_table(start='B3', end='B8500', values=coordList, dimension='ROWS', overwrite=True)