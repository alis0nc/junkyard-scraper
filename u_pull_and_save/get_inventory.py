#!/usr/bin/env python3
import requests
import json

BASE_URL = 'https://api.u-pullandsave.com/vehicles'
results = []

with open('u_pull_and_save/all_models.json', 'r') as models_file:
    all_models = json.load(models_file)
    for make, models in all_models.items():
        print(f'Searching for all {make}')
        for model, model_info in models.items():
            newest_valid_year = model_info['valid_years'][0]
            # TODO: handle both stores (105 and 110)
            search_response = requests.get(BASE_URL + f'/search?year={newest_valid_year}&make={make}&model={model}&store=110')
            search_results = search_response.json()
            for result in search_results:
                record = {
                    'year': result['modelYear'],
                    'make': result['modelMake'],
                    'model': result['modelName'],
                    'color': result['colorOfVehicle'],
                    'row': result['yardRow'],
                    'stock_number': result['stockID'],
                    'upas_id': result['vehicleID'],
                }
                results.append(record)

print(results)
print(f'{len(results)} total')
