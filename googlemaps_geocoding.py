import io
import json
import os
import googlemaps
from pprint import pprint

# Address for lookup
maps_query = "27265"

def main():
    # Confidential info filepath
    saved_responses_path = "data_store/form_responses.json"

    # Populate dict from latest saved version
    tigres = {}
    if os.path.isfile(saved_responses_path):
        with io.open(saved_responses_path) as json_file:
            tigres = json.load(json_file)
    else:
        print("""*********************************************
    ************   File not found   *************
    *********************************************""")
        quit()

    pprint(get_geodata(maps_query))

def get_geodata(address = maps_query):
    """Gets coordinates from address query

    Parameters
    ----------
    address : str
        The address to look up as it would work in Google Maps
    Returns
    -------
    dict
       a dict contianing the City and State names (long and short versions)
       and coordinates from the query
    """

    # Get Google map key from env variable
    gmaps_key = os.getenv("GOOGLE_MAPS_KEY")

    # Start the client
    gmaps = googlemaps.Client(key=gmaps_key)

    # Geocoding an address
    geocode_results = gmaps.geocode(address)#,components={"country": "MX"})
    # pprint(geocode_results)

    # Handle No Results
    if not geocode_results:
        print(address + " was not found. Try another address format or check typos.")
        return {}
    
    geocode_result = geocode_results[0]

    format_data = {}

    # Parse and format data
    address_components = geocode_result.get("address_components",[])

    for address_component in address_components:
        types = address_component.get("types","")

        # Parse locality
        if types and 'locality' in types:
            format_data['City'] = [
                address_component['long_name'],
                address_component['short_name']
            ]

        # Parse State
        if types and 'administrative_area_level_1' in types:
            format_data['State'] = [
                address_component['long_name'],
                address_component['short_name']
            ]

        location = geocode_result.get('geometry',{}).get('location',{})

        if location:
            format_data['lat'] = location.get('lat',False)
            format_data['lng'] = location.get('lng',False)

    return format_data
    
if __name__ == "__main__":
    main()