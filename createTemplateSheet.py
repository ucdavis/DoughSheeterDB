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
rawData.cell('A2').value = 'unixTime'
rawData.cell('B2').value = 'posNum'
rawData.cell('C2').value = 'posLoc'
rawData.cell('D2').value = 'height'
rawData.cell('E2').value = 'pass'
rawData.cell('F2').value = 'beltNum'
rawData.cell('G2').value = 'direction'

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


#filter the height and find the average
averageHID = gc.open_by_key(template).worksheet_by_title('averageHeight').id
averageH= sh.add_worksheet('averageHeight', rows=40000, cols=6, src_tuple=[template,averageHID], index=4)


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
