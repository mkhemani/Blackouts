# /# Author: CWM
# # Purpose: downloading tables from PDFs
# # refs:
# #   https://www.thepythoncode.com/article/extract-pdf-tables-in-python-camelot
# #   https://tabula-py.readthedocs.io/en/latest/tabula.html
# # https://github.com/tabulapdf/tabula-java/issues/255
# # pip install pdfplumber
# import camelot

# file = "C:\\Users\\cmilando\\OneDrive - Boston University\\Documents\\51 - Optum\\02_Blackouts\\SOR\\13-SOR-Q3\\13-SOR-Q3-Filing-5625.pdf"

# tables = camelot.read_pdf(file, pages="1-20")
# # hmm does work now
# tables[0]
# print(tables[0].df)


# # ----------------------------------------------------------------------------
# import tabula
# import os

# tables = tabula.read_pdf(file, pages=2)

# tabula.convert_into(file, "output6a.tsv", output_format="tsv", pages="6",
#                     area = [17, 0, 90, 100],
#                     relative_area=True,
#                     #          Town    dt    ID
#                     columns=[0,    14,    20,   23, 100],
#                     relative_columns=True)

# -----------------------------------------------------------------------------
# this is the solution
# https://github.com/jsvine/pdfplumber/tree/stable#extracting-tables
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

#OUTPUT ERRORS
#13-SOR-Q3-Filing-5625SectionA: IT IS NOT RECOGNIZING ROW 2, COLUMN 4's third VALUE. Manual check for that needs to be done
                                # column headers are not included, so have to reference from the OG pdf
#13-SOR-Q3-Filing-5625SectionB: No need for replacing ',' and ' '. 
#13-SOR-Q3-Filing-5705: no need to replace spaces or commas. CSV is interesting format because of the pdf, so have to reference the 
                                # OG pdf to manually check the service territory for each table. 
#13-SOR-Q4-Filing-8412: similar as above

# NOTE: python arrays/indices go from 0:x, not 1:x
# NOTE: many similar functions as in R are written in the `pandas` library, so look at those
# NOTE: unfortunately, this will have to be modified for each pdf, the final workflow will be 
#       opening this script, changing the filename, changing the page numbers, changeing the vertical lines, and then running

#CODE APPENDIX
#13-SOR-Q3-Filing-5625SectionA: "explicit_vertical_lines": [35, 114, 154, 186, 226, 350, 385, 425, 456.5, 602, 750]
