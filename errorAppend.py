import pygsheets
gc = pygsheets.authorize("client_secret.json")

import csv
from datascience import *
import numpy as np

sponsor = input("what is the sponsor name?")
flour = input('what is the flour type?')
time = input("when did you run")
fileName = sponsor+ '-'+flour+"-"+time
sh = gc.open(fileName)
coverSheet = sh.worksheet_by_title("coverSheet")




#add data sheets for filtering data, finding averages, and doing analysis
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
inHeightID = template.worksheet_by_title('inHeight').id
inHeight = sh.add_worksheet('inHeight', rows=15000, cols=6, src_tuple=[templateID,inHeightID], index=4)
inHeightAvgID = template.worksheet_by_title('inHeightAvg').id
inHeight = sh.add_worksheet('inHeightAvg', rows=15000, cols=6, src_tuple=[templateID,inHeightAvgID], index=5)
outHeightID = template.worksheet_by_title('outHeight').id
outHeight = sh.add_worksheet('outHeight', rows=15000, cols=6, src_tuple=[templateID,outHeightID], index=6)
outHeightAvgID = template.worksheet_by_title('outHeightAvg').id
outHeightAvg = sh.add_worksheet('outHeightAvg', rows=15000, cols=6, src_tuple=[templateID,outHeightAvgID], index=7)
vFID = template.worksheet_by_title('VF').id
forceData = sh.add_worksheet('VF', rows=2000, cols=2, src_tuple=[templateID,vFID], index=8)
consolidateID = template.worksheet_by_title('consolidatedData').id
consolidate = sh.add_worksheet('consolidatedData', rows=2000, cols=8, src_tuple=[templateID,consolidateID], index=9)

analysisID= template.worksheet_by_title('analysis').id
analysis = sh.add_worksheet('analysis', rows=15000, cols=6, src_tuple=[templateID,analysisID], index=10)

visualizationID = template.worksheet_by_title('visualization').id
visualization = sh.add_worksheet('visualization', rows=2000, cols=5, src_tuple=[templateID, visualizationID], index=10)
