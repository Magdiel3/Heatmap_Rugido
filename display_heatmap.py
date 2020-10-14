import streamlit as st
import os
import io
import json
import pandas as pd
import numpy as np
import folium
from folium import plugins
from streamlit_folium import folium_static


# SetUp for website
st.beta_set_page_config(
     page_title="El Rugido en MX"
)

def local_css(file_name):
    with io.open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
local_css("style.css")

st.title("¿Dónde rugen los Tigres (6652)")

# Some basic description of the project
st.header("¿Cómo funciona?")
st.markdown("""
        Los miembros de **Tigres 6652** han llenado un [formulario](https://forms.gle/ozU7gcf7KhAXt8mA6),
        espero, con el que pudimos localizar sus puntos en el mapa y cuando tu cargas esta página, se
        revisa automáticamente que estén todos los puntos actualizados o si hay nuevas respuestas.
    
        Las respuestas nuevas o actualizadas son automáicamente buscadas en Google Maps a través de la
        API que manejan que, de momento, es gratis.
    """)

# Plotting of the first map
st.header("Lo que queremos ver")
st.write("")

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

# Transform dictionary to DataFrame
tigres_df = pd.DataFrame.from_dict(tigres,orient='index')
tigres_df = pd.concat([tigres_df.drop(['GPS'], axis=1), tigres_df['GPS'].apply(pd.Series)], axis=1)

# Define data midpoint
north_east = [33.507737, -117.465716]
south_west = [14.292654, -86.771553]
mx_boundries = [[north_east[0],south_west[0]],[north_east[1],south_west[1]]]
midpoint = (np.average(mx_boundries[0]), np.average(mx_boundries[1]))

# Generate map
m=folium.Map([midpoint[0],midpoint[1]],zoom_start=5)

# convert to (n, 2) nd-array format for heatmap
location_data = tigres_df[['lat', 'lng']].values

# plot heatmap
m.add_child(plugins.HeatMap(location_data, radius=15))

persmission = int(os.getenv("DISPLAY_NAMES"))
print(persmission)
# Add markers to every Tiger
if persmission:
    tooltip = 'Click me!'
    for tigre in tigres.values():
        apodo = tigre.get('Apodo (nombre corto)',"Un Tigre")
        tigre_gps = [
            tigre.get("GPS",{}).get("lat",midpoint[0]),
            tigre.get("GPS",{}).get("lng",midpoint[1])
        ]
        folium.Marker(tigre_gps, popup=apodo, tooltip=tooltip).add_to(m)
    st.markdown(f"**Respuestas:** {len(list(tigres.keys()))}")
folium_static(m)

# Some useful docs for the user
st.header("Un poco más de explicación")
st.write("El mapa no tiene tanta complejidad, realmente son solo 4 líneas de código")
st.code("""
# Generate map
m=folium.Map([midpoint[0],midpoint[1]],zoom_start=5)

# convert to (n, 2) nd-array format for heatmap
location_data = tigres_df[['lat', 'lng']].values

# plot heatmap
m.add_child(plugins.HeatMap(location_data, radius=15))

folium_static(m)
""")
st.markdown("""
Y el resto es usar la API de Google para la hoja de cálculo con las respuestas del
formulario y para obtener las coordenadas con Google Maps. También hay algo más para
poder hacer la página visible que es usar un servidor de [Heroku]()
""")
st.markdown("""
La información es recabada y almacenada en un archivo con formato JSON y cada ejemplo se
ve algo así como lo siguiente:
""")
st.write(tigres['José Magdiel Martínez Ulloa'])
st.markdown("""
Pero no te preocupes, la información solo la tienen los desarrolladores y, aunque todo el
[código](https://github.com/Magdiel3/Heatmap_Rugido) es abierto, no están considerados los
archivos con información del formulario ni las credenciales de la API.
""")