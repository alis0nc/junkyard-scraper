#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://usautosupplymi.com/upull/wayne/wayne-inventory/')

# Close the annoying fb chat widget
fb_iframe = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "[data-testid='dialog_iframe']"))
driver.switch_to.frame(fb_iframe)
time.sleep(2) # give things time to settle
close_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='close']")
close_button.click()
driver.switch_to.parent_frame()

# Show 100 items
vehicles_length = driver.find_element(By.NAME, 'vehiclesw_length')
vehicles_length_select = Select(vehicles_length)
vehicles_length_select.select_by_value('100')

# Sort by arrival date descending
arrival_date_header = driver.find_element(By.XPATH, "//*[text()='Arrival Date']")
while arrival_date_header.get_attribute('aria-sort') != 'descending':
    arrival_date_header.click()

results = []

while True:
    next_button = driver.find_element(By.ID, 'vehiclesw_next')
    # Parse the table
    vehicles_table_body = driver.find_element(By.ID, 'vehiclesw').find_element(By.TAG_NAME, 'tbody')
    vehicles_table_rows = vehicles_table_body.find_elements(By.TAG_NAME, 'tr')

    for row in vehicles_table_rows:
        arrival_date_td = row.find_element(By.CSS_SELECTOR, "[data-label='Arrived']")
        # wayne doesn't put their stock numbers here, TODO parse this
        stock_number_td = driver.execute_script('return arguments[0].nextElementSibling', arrival_date_td)
        try:
            image_url = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except NoSuchElementException:
            image_url = None
        record = {
            'year': row.find_element(By.CSS_SELECTOR, "[data-label='Year']").text,
            'make': row.find_element(By.CSS_SELECTOR, "[data-label='Make']").text,
            'model': row.find_element(By.CSS_SELECTOR, "[data-label='Model']").text,
            'color': row.find_element(By.CSS_SELECTOR, "[data-label='Color']").text,
            'reference': row.find_element(By.CSS_SELECTOR, "[data-label='Reference']").text,
            'row': row.find_element(By.CSS_SELECTOR, "[data-label='Row']").text,
            'arrival_date': datetime.strptime(arrival_date_td.text, '%m/%d/%y'),
            'stock_number': stock_number_td.text,
            'image_url': image_url,
        }
        results.append(record)
    
    if 'disabled' in next_button.get_attribute('class').split():
        break

    next_button.click()

print(results)
print(f"{len(results)} total")

time.sleep(10)

driver.quit()
