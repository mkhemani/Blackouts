# Author: CM
# Modified: MK 8/23

from selenium import webdriver
import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import webdriver_manager
import requests
from tqdm import tqdm
import re
import os
import time 
from pathlib import Path



# get cd function
def getFilename_fromCd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

# Go to website in Edge
DPU_URL = 'https://eeaonline.eea.state.ma.us/DPU/Fileroom/dockets/bynumber'
EDGE_DRIVER = Service(r'C:\msedge\msedgedriver.exe')
edge_option = webdriver.EdgeOptions()

driver = webdriver.Edge(service=EDGE_DRIVER, options=edge_option)
driver.get(DPU_URL)
WebDriverWait(driver, 10)

# make strings
# 21-SQ-14
yr_str = ['21'] 
dpu_units = ['14'] #'10', '11', '12', '13', '14'
q_strings = ['Q4'] 

sq_strings = []
for yr in yr_str:
    for dpu in dpu_units:
        sq_strings.append(yr + '-SQ-' + dpu)

sor_strings = []
for yr in yr_str:
    for q in q_strings:
        sor_strings.append(yr + '-SOR-' + q)

# Now loop through the SOR and QR things
def get_links_by_string(dirname, docketNum):

    print(dirname + ": " + docketNum)
    this_folder = os.path.join(dirname, docketNum)
    if not os.path.exists(this_folder):
        os.makedirs(this_folder)

    driver.find_element(By.ID, 'docketNum').clear()
    driver.find_element(By.ID, 'docketNum').send_keys(docketNum)
    driver.find_element(By.ID, 'byNumber').click()
    time.sleep(5)
    
    # Now ... download everything on this page
    # make a new download folder by the name
    # there are a variable number of files on this page
    lnks = driver.find_elements(By.TAG_NAME, "a")
    print(len(lnks))

    for lnk in lnks:
        # get_attribute() to get all href
        href = lnk.get_attribute('href')
        api_sub = "FileService.Api"

        if href.find(api_sub) != -1:

            r = requests.get(href)

            filename = str(getFilename_fromCd(r.headers.get('content-disposition')))            
            print(".... " + filename)

            open(this_folder + "\\\\" + filename.replace('"', ''), 'wb').write(r.content)

# tests
 #get_links_by_string('SQ', '21-SQ-14')

# get all data
for sq in sq_strings:
    get_links_by_string('SQ', sq)

for sor in sor_strings:
    get_links_by_string('SOR', sor)
