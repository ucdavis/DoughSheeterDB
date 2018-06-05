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

coverSheet = sh.add_worksheet('CoverSheet', rows=100, cols=10, src_tuple=[template,coverFrTemplateID], index=1)

analysis = sh.add_worksheet('Analysis', rows=100, cols=10, index=2)

#add headers
rawData = sh.add_worksheet('RawData', rows=33000, cols = 10, index =3)
rawData.cell('A2').value = 'UnixTime'
rawData.cell('B2').value = 'BeltNum'
rawData.cell('C2').value = 'Direction'
rawData.cell('D2').value = 'posNum'
rawData.cell('E2').value = 'posLoc'
rawData.cell('F2').value = 'height'

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
    
append_csv_file('inH_P1.csv')
append_csv_file('outH_P1.csv')
append_csv_file('inH_P2.csv')
append_csv_file('outH_P2.csv')
append_csv_file('inH_P3.csv')
append_csv_file('outH_P3.csv')
append_csv_file('inH_P4.csv')
append_csv_file('outH_P4.csv')

#filter the height and find the average
averageHID = gc.open_by_key(template).worksheet_by_title('averageHeight').id
averageH= sh.add_worksheet('averageHeight', rows=40000, cols=6, src_tuple=[template,averageHID], index=4)

sh.del_worksheet(sheet1)
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
