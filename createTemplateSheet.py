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