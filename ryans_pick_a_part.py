#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from datetime import datetime

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://ryanspickapart.com/Home/Inventory')

vehicle_make = driver.find_element(By.NAME, 'VehicleMake')
vehicle_make_select = Select(vehicle_make)
all_make_options = vehicle_make_select.options
assert len(all_make_options)
assert all_make_options[0].text == 'Select Make'
all_make_options.pop(0)
assert all(map(lambda m: m.get_attribute('value').lower() == m.text.lower(), all_make_options))
all_makes = [make.text for make in all_make_options]

results = []

for make in all_makes:
    vehicle_make = driver.find_element(By.NAME, 'VehicleMake')
    vehicle_make_select = Select(vehicle_make)
    vehicle_make_select.select_by_value(make)
    WebDriverWait(driver, 10).until(staleness_of(vehicle_make))
    vehicle_model = driver.find_element(By.NAME, 'VehicleModel')
    vehicle_model_select = Select(vehicle_model)
    assert vehicle_model_select.options[0].text == 'Select Model'
    vehicle_model_select.select_by_visible_text('Select Model')

    # luckily the inventory table is the only table on the page, because
    # it doesn't even have an id or name
    inventory_table_body = driver.find_element(By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody')
    inventory_table_rows = inventory_table_body.find_elements(By.TAG_NAME, 'tr')
    assert inventory_table_rows[0].text == 'YEAR MAKE MODEL COLOR ROW ARRIVAL DATE STOCK #'
    inventory_table_rows.pop(0)

    for row in inventory_table_rows:
        year_td = row.find_element(By.TAG_NAME, 'td')
        make_td = driver.execute_script('return arguments[0].nextElementSibling', year_td)
        model_td = driver.execute_script('return arguments[0].nextElementSibling', make_td)
        color_td = driver.execute_script('return arguments[0].nextElementSibling', model_td)
        row_td = driver.execute_script('return arguments[0].nextElementSibling', color_td)
        arrival_date_td = driver.execute_script('return arguments[0].nextElementSibling', row_td)
        stock_number_td = driver.execute_script('return arguments[0].nextElementSibling', arrival_date_td)
        record = {
            'year': year_td.text,
            'make': make_td.text,
            'model': model_td.text,
            'color': color_td.text,
            'row': row_td.text,
            'arrival_date': datetime.strptime(arrival_date_td.text, '%m/%d/%Y'),
            'stock_number': stock_number_td.text,
        }
        print(record)
        results.append(record)

print(f"{len(results)} total")
driver.quit()
