import io
import json
import os
import googlemaps
from pprint import pprint


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

# Get Google map key from env variable
gmaps_key = os.getenv("GOOGLE_MAPS_KEY")

print(gmaps_key)

gmaps = googlemaps.Client(key=gmaps_key)

# Geocoding an address
geocode_result = gmaps.geocode('04450, MEX')

pprint(geocode_result)