import pygsheets
gc = pygsheets.authorize()

#open an existing spreadsheet by title
sh = gc.open('title')
wks = sh.sheet1

#write in cells - method 1
wks.update_cells('A1',[['Dough Sheet Testing on May 29, 2018']])
wks.update_cells('A1:A5\'92,[[1], [2], [3], [4], [5]])

#write in cells - method 1=2
wsk.cell('91F2').value = 'posLoc'
wsk.cell('A1').set_text_format('bold', True).value = 'dough sheeter'

#add a new worksheet - empty
sh.add_worksheet('title', rows=100, cols= 26)

# copy to a new worksheet
sh.add_worksheet('title', rows=100, cols=26, src_tuple = tuple_of_worksheet_spreadsheet_id, src_worksheet = source_worksheet, index = tab_index)

# returns a worksheet by title
wsk = sh.worksheet_by_title('title')

#get id for spreadsheet or worksheet
print (sh.id)
