from datetime import datetime
import pygsheets
import csv
from datascience import *
import numpy as np
import webbroswer
gc = pygsheets.authorize("client_secret.json")

#create google sheet with appropriate names
sponsor = input("what is the sponsor name?")
flour = input('what is the flour type?')
time = datetime.now().strftime('%Y-%m-%d-%H-%M')
fileName = sponsor+ '-'+flour+"-"+time
# store file in appropriate sponsor's folder
if sponsor == "Ardent":
    parent = "1cMT_LlBnU2BDa0T0Fti6uVoewEHV3ll-"
else: 
    parent = "1YVG4T-0uPaubnIIi0-rMgUItSDt67OOm"
sh = gc.create(fileName, parent_id = parent)

# copy coverSheet to this new google sheet
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
coverFrTemplateID = template.worksheet_by_title('coverSheet').id
coverSheet = sh.add_worksheet('coverSheet', rows=100, cols=10, src_tuple=[templateID,coverFrTemplateID], index=1)
coverSheet.update_cell("B5", time)
print ("fill out cover sheet")
# delete blank sheet1
sheet1 = sh.sheet1
sh.del_worksheet(sheet1)
# open coverSheet
shID = sh.id
webbrowser.open('https://docs.google.com/spreadsheets/d/'+shID) 
