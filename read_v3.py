
import pdfplumber
import pandas as pd
import csv
import os

file = "/Users/allisonjames/Desktop/13-SOR-Q4-Filing-8413.pdf"

pdf = pdfplumber.open(file)
p0 = pdf.pages[49] #first page, to configure table_settings
im = p0.to_image(resolution = 600)

#table settings will change per file
table_settings = {
    "horizontal_strategy": "lines",
    "vertical_strategy": "lines"
    #"explicit_vertical_lines": [35, 114, 153, 186, 226, 349, 382, 419, 451, 594, 742]
}

#extracting table to png to check the lines
im.reset().debug_tablefinder(table_settings).save('pg49.png')
tbl = p0.extract_table(table_settings)


#home directory
home_dir = os.path.expanduser("~")

#file path
csv_file_path = os.path.join(home_dir, "Desktop", "13-SOR-Q4-Filing-8413SectionB.csv") #will have to change this for each file


#defining the page start and page end
page_start = 49
page_end = 69


# pp.pprint(table)

# two things to look up for Python
# - list comprehension
# - Pass by reference

# Creating a csv writer object
csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)  # Save as CSV
last_nonempty = None
headers_written = False
    
# Loop extracting the table on each page
for page in pdf.pages[page_start-1:page_end]:
    
    tables = page.extract_tables(table_settings)
    
    # Loop through each table on the page
    for table in tables:
        
        # create a new table that doesn' have any blanks
        rows_to_keep = list()
        row_i = 0
        for row in table:
            if any(val != "" for val in row):
                rows_to_keep.append(row_i)
            row_i = row_i + 1
        # only keep rows with data using list comprehension
        table =  [table[i] for i in rows_to_keep]

        # Downfilling the first column
        # CODE CHALLENGE: How would we expand this to downfill for more than the first column?
        # hint: add another loop (to make this a "nested for loop", aka a loop inside a loop)
        #      i think it will be easiest  to make the loop outsdie
        for a in [0,1,2,3]:
            last_nonempty = None # you'll need to reset something here ....
            for row in table:
                if row[a] == "": ## something needs to change
                    row[a] = last_nonempty  ## something needs to change
                else:
                    last_nonempty = row[a]  ## something needs to change

        # CSV outputs the headers one time
        if not headers_written:
            csv_writer.writerow(table[0])
            headers_written = True
             # If no column headers 'for row in table:'. If column headers 'for row in table[1:]:'
                # Checks if values in a row are empty strings and if YES, continues to next row without writing it to CSV file
        for row in table:
            if row[0] == "Town":
                continue
            else:
            #  if not all(val == "" for val in row):
            #    continue     
                csv_writer.writerow(row)
            # Replacing spaces and commas
            # row[5:8] = [val.replace(' ', '').replace(',', '') for val in row[5:8]]

csv_file.close()