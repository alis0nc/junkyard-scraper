#!/usr/bin/env python3
import requests
import json

BASE_URL = 'https://api.u-pullandsave.com/vehicles'

all_models = {}

years_response = requests.get(BASE_URL + '/years')
years = [y['modelYear'] for y in years_response.json()]

for year in years:
    print(f'Gathering makes and models for {year}')
    makes_for_year_response = requests.get(BASE_URL + f'/make/{year}')
    makes_for_year = [m['vehicleMake'] for m in makes_for_year_response.json()]

    for make in makes_for_year:
        if make not in all_models:
            all_models[make] = {}
        models_for_make_and_year_response = requests.get(BASE_URL + f'/model/{year}/{make}')
        models_for_make_and_year = {m['hollanderModel']:m for m in models_for_make_and_year_response.json()}

        def add_valid_year(make, model, year):
            if 'valid_years' not in all_models[make][model]:
                all_models[make][model]['valid_years'] = [year]
            else:
                all_models[make][model]['valid_years'].append(year)

        for model_key, model in models_for_make_and_year.items():
            if model_key not in all_models[make]:
                all_models[make][model_key] = model
            add_valid_year(make, model_key, year)

with open('all_models.json', 'w') as models_file:
    json.dump(all_models, models_file)
