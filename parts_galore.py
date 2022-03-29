#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import re

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.parts-galore.com/inventory/')

# this is so stupid
alldata = driver.find_element(By.ID, 'alldata')
assert alldata.get_attribute('style') == 'display: none;'
driver.execute_script("arguments[0].setAttribute('style', '')", alldata)
# yes the wobsite really does have a display:none table with the entire inventory in it

alldata_body = alldata.find_element(By.TAG_NAME, 'tbody')
alldata_rows = alldata_body.find_elements(By.TAG_NAME, 'tr')

results = []

for row in alldata_rows:
    year_td = row.find_element(By.TAG_NAME, 'td')
    make_td = driver.execute_script('return arguments[0].nextElementSibling', year_td)
    model_td = driver.execute_script('return arguments[0].nextElementSibling', make_td)
    location_td = driver.execute_script('return arguments[0].nextElementSibling', model_td)
    row_td = driver.execute_script('return arguments[0].nextElementSibling', location_td)
    data_make = row.get_attribute('data-make')
    data_model = row.get_attribute('data-model')
    assert data_make.lower() == make_td.text.lower()
    assert data_model.lower() == model_td.text.lower()
    record = {
        'year': year_td.text,
        'make': make_td.text,
        'model': model_td.text,
        'location': location_td.text,
        'row': row_td.text,
    }
    print(record)
    results.append(record)

print(f"{len(results)} total")

driver.quit()
