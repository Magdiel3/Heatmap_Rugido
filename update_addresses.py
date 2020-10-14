import io
import json
import os
from pprint import pprint
from googlemaps_geocoding import get_geodata
from tqdm import tqdm

# Confidential info filepath
saved_responses_path = "data_store/form_responses.json"

# Will store the data
tigres = {}

# Populate dict from latest saved version
if os.path.isfile(saved_responses_path):
    with io.open(saved_responses_path) as json_file:
        tigres = json.load(json_file)
else:
    print("""*********************************************
************   File not found   *************
*********************************************""")
    quit()

# Loop for every member
for tigre, data in tqdm(tigres.items(),"Updating..."):

    # Check update condition
    if not data.get('Updated GPS',False):

        # Get response address
        cp = data.get('Código Postal','')
        
        # Call geocoding API
        update = get_geodata(address=cp + ", México")

        # Update or write data from API response
        if 'GPS' in data:
            data['GPS'].update(update)
        else:
            data['GPS'] = update

        # Unmark tag
        data['Updated GPS'] = True
        
        # pprint({cp:update})
    
    # Overwrite data
    tigres[tigre] = data

# Save to a file
with io.open(saved_responses_path,'w') as json_output:
    json.dump(tigres,json_output,ensure_ascii=False,indent=4,sort_keys=True)
    