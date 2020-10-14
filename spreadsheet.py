import io
import os
import os.path
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# COnfidential info filepath
saved_responses_path = "data_store/form_responses.json"

# Will store the data
tigres = {}

# Populate dict from latest saved version
if os.path.isfile(saved_responses_path):
    with io.open(saved_responses_path) as json_file:
        tigres = json.load(json_file)

# based on https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# read that file for how to generate the creds and how to use gspread to read and write to the spreadsheet

# use creds to create a client to interact with the Google Drive API
scopes = ['https://spreadsheets.google.com/feeds']

# Must be exported to the environment variables
json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
client = gspread.authorize(creds)

# Find a workbook by url
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1VIXTJFnDBys49KMHxWg9YepknVVzAfpHkyHYKpXSAvs/edit#gid=704459328")
sheet = spreadsheet.sheet1

# Extract and print all of the values
rows = sheet.get_all_records()
# print(rows)

# Format to dataframe
data = pd.DataFrame(rows)
# print(data)

# Save to a local file
with io.open(saved_responses_path,"w") as json_output:
    
    # Format responses into a dict
    for tigre in rows:

        # Remove the full name to use as key
        nombre = tigre.pop("Nombre (Completo)")
        
        if nombre:
            
            # Remove whitespaces at the end of the name
            while nombre[-1] == " ":
                nombre = nombre[:-1]

            # Create item if not captured already
            if not tigres.get(nombre,""):
                tigres[nombre] = tigre

            # Tag updated ZIP codes
            if tigres[nombre].get("GPS","") and str(tigre.get("Código Postal")).zfill(5) == tigres[nombre]["Código Postal"]:
                tigres[nombre]["Updated GPS"] = True
            else:
                tigres[nombre]["Updated GPS"] = False

            # Update if something changed
            tigres[nombre].update(tigre)

            # Parse ZIP codes with zero padding
            tigres[nombre]["Código Postal"] = str(tigres[nombre]["Código Postal"]).zfill(5)
    
    # Save to a file
    json.dump(tigres,json_output,ensure_ascii=False,indent=4,sort_keys=True)