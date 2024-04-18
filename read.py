# /# Author: CWM
# #  Modified by: Muskaan Khemani 4/23
# # Purpose: downloading tables from PDFs
# ref: https://github.com/jsvine/pdfplumber/tree/stable#extracting-tables
# if you don't see (env) run the line `.\env\Scripts\activate`
import pdfplumber
import pandas as pd
import csv
import os

file = "C:\\Users\\mkhemani\\OneDrive - Boston University\\02_Blackouts\\SOR\\13-SOR-Q4\\13-SOR-Q4-Filing-8413.pdf"


pdf = pdfplumber.open(file)
p0 = pdf.pages[49] #first page, to configure table_settings
im = p0.to_image(resolution = 600)

#table settings will change per file
table_settings = {
    "horizontal_strategy": "lines",
    "vertical_strategy": "lines"
}

#extracting table to png to check the lines
im.reset().debug_tablefinder(table_settings).save('pg.png')
tbl = p0.extract_table(table_settings)


#home directory
home_dir = os.path.expanduser("~")

#file path
file_path = os.path.join(home_dir, "Desktop", "13-SOR-Q4-Filing-8413-SectionB.csv") #will have to change this for each file

#defining the page start and page end
page_start = 49
page_end = 69

#creating a csv writer object
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    last_nonempty = None
    headers_written = False
    #loop extracting the table on each page
    for page in pdf.pages[page_start-1:page_end]: 
        tables = page.extract_tables(table_settings)
        #loop through each table on the page
        for table in tables:
                #downfilling the first column
                #for i, row in enumerate(table):
                    #if row[0] == "":
                        #row[0] = last_nonempty
                    #else:
                        #last_nonempty = row[0] 
                if not headers_written:
                     csv_writer.writerow(table[0])
                     headers_written = True
            #write table data to csv
                for row in table:
                    if row[0] == "Day":
                        continue
                    else:
                #for row in table[1:]: #If no column headers 'for row in table:'. If column headers 'for row in table[1:]:' 
                        #checks if values in a row are empty strings and if YES, continues to next row without writing it to CSV file
                        #if all(val == "" for val in row):
                              #continue
                        #replacing spaces and commas
                        #row[5:8] = [val.replace(' ','').replace(',','')for val in row[5:8]]                
                        csv_writer.writerow(row)

#CODE APPENDIX
#13-SOR-Q3-Filing-5625SectionA: "explicit_vertical_lines": [35, 114, 154, 186, 226, 350, 385, 425, 456.5, 602, 750]
