from datetime import datetime
# Library to access/edit/save googlesheets
import pygsheets
# Libary to edit csv data
import csv
#Libraries for handling datastructures - array, list
from datascience import *
import numpy as np
#Library to open url links in code
import webbrowser

# This code performs following tasks:
# Connects to google drive
# Creates a new google sheet for the experiment(s) 
# and writes data to it.

# Creating a connection to the drive , Authorization function takes the key file as parameter.
gc = pygsheets.authorize("client_secret.json")

#Query User for experiment meta-data : Sponsor Name and Flour type. Time of experiment is System time.
sponsorType = input("what is the sponsor name? enter 1 if Ardent")
if sponsorType == "1":
	sponsor = "Ardent"
else:
	sponsor = sponsorType

flourType = input('what is the flour type? enter 1 for allPurpose; 2 for breadFlour ')
if flourType == "1":
	flour = "allPurpose"
elif flourType == "2":
	flour = "breadFlour"
else:
	flour = flourType

time = datetime.now().strftime('%Y-%m-%d-%H-%M')


#Concatenate meta-data(sponsor+flour+time) to create file name of google sheet
# to which experiment data will be stored.
fileName = sponsor+ '-'+flour+"-"+time

#Store newly created file in folder specific to the Sponsor
#Any new sponsors should be added here
#Each folder is identified by folder address, which is found in the the googledrive hyperlink.
if sponsor == "Ardent":
    parent = "1cMT_LlBnU2BDa0T0Fti6uVoewEHV3ll-"
else:
    parent = "1YVG4T-0uPaubnIIi0-rMgUItSDt67OOm"
sh = gc.create(fileName, parent_id = parent)

with open('SpreadsheetKey.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Store the key of the spreadsheet in csv file
    writer.writerow([sh.id,sponsor])

# Access Template Spreadsheet to copy to new google sheet - "Cover Sheet" and "Parameter choices"
# These are standard sheets for every experiment and contain data about experimental settings and materials
template = gc.open("Dough Sheeter Spreadsheet Templates")
templateID = template.id
#copy parameter choices
paraChID = template.worksheet_by_title('parameter choices').id
sh.add_worksheet('parameter choices', rows=100, cols=10, src_tuple=[templateID,paraChID], index=2)
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
