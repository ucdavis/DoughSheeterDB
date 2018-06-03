import pygsheets
gc = pygsheets.authorize()

import csv
from datascience import *
import numpy as np


sh = gc.create('template')
#create(title, parent_id=None)

sheet1 = sh.worksheet_by_title('Sheet1')
template = gc.open('SponsorCode-DoughVariety-yyyymmdd-HH:mm').id
template

coverFrTemplate= gc.open_by_key(template).worksheet_by_title('CoverSheet')

coverFrTemplateID = coverFrTemplate.id
coverFrTemplateID

coverSheet = sh.add_worksheet('CoverSheet', rows=100, cols=10, src_tuple=[template,coverFrTemplateID], index=1)

analysis = sh.add_worksheet('Analysis', rows=100, cols=10, index=2)

rawData = sh.add_worksheet('RawData', rows=33000, cols = 10, index =3)

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
