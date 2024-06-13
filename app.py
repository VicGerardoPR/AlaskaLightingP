import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import requests
import folium
import zipfile
from streamlit.components.v1 import html
import contextily as cx

# Función para descargar y descomprimir el archivo
def download_and_extract_data():
    url = 'https://fire.ak.blm.gov/content/maps/aicc/Data/Data%20(zipped%20Shapefiles)/CurrentYearLightning_SHP.zip'
    response = requests.get(url)
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    zip_file.extractall("CurrentYearLightning_SHP")

# Descargar y descomprimir los datos
st.title('Alaska Lightning Detection Network Analysis')

st.subheader('Verificar los rayos. ')

with st.spinner('Downloading and extracting data...'):
    download_and_extract_data()


# Cargar el shapefile
shapefile_path = 'CurrentYearLightning_SHP/TOA_STRIKES.shp'
alaskaP = gpd.read_file(shapefile_path)

st.subheader('Current Year Lightning Strikes in Alaska')
m = folium.Map(location=[alaskaP['LATITUDE'].mean(), alaskaP['LONGITUDE'].mean()], zoom_start=6)

for _, row in alaskaP.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=3,
        weight=1,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Renderizar el mapa usando st.components.v1.html
folium_html = m._repr_html_()
html(folium_html, width=700, height=500)


# Convertir a datetime
alaskaP['STRIKETIME'] = pd.to_datetime(alaskaP['STRIKETIME'])

alaskaP['year'] = alaskaP['STRIKETIME'].dt.year
alaskaP['month'] = alaskaP['STRIKETIME'].dt.month
alaskaP['day'] = alaskaP['STRIKETIME'].dt.day
alaskaP['hour'] = alaskaP['STRIKETIME'].dt.hour
alaskaP['dayofweek'] = alaskaP['STRIKETIME'].dt.dayofweek
alaskaP['week'] = alaskaP['STRIKETIME'].dt.isocalendar().week

# Número de rayos por mes
st.subheader('Number of Lightning Strikes by Month')
fig, ax = plt.subplots()
sns.countplot(x='month', data=alaskaP, ax=ax)
ax.set_title('Number of Lightning Strikes by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Count')
st.pyplot(fig)

# Número de rayos por día
st.subheader('Number of Lightning Strikes by Day')
fig, ax = plt.subplots()
sns.countplot(x='day', data=alaskaP, ax=ax)
ax.set_title('Number of Lightning Strikes by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Count')
st.pyplot(fig)

# Distribución de tipos de rayos en un mapa
st.subheader('Lightning Strikes by Type')
fig, ax = plt.subplots()
alaskaP.plot(column="STROKETYPE", legend=True, ax=ax)
ax.set_title('Lightning Strikes by Type')
st.pyplot(fig)


# Número de rayos por día del año actual
st.subheader('Number of Lightning Strikes by Day in Current Year')
alaskaP['day'] = alaskaP['STRIKETIME'].dt.date
daily_counts = alaskaP['day'].value_counts().sort_index()
daily_counts.index = pd.to_datetime(daily_counts.index)
fig, ax = plt.subplots()
sns.lineplot(x=daily_counts.index, y=daily_counts.values, marker='o', ax=ax)
ax.set_title('Number of Lightning Strikes by Day')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
ax.grid(True)
st.pyplot(fig)

# Número de rayos por hora en el año actual
st.subheader('Number of Lightning Strikes by Hour in Current Year')
current_year = alaskaP['year'].max()
daily_data = alaskaP[alaskaP['year'] == current_year]
hourly_counts = daily_data['hour'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, ax=ax)
ax.set_title('Number of Lightning Strikes by Hour in Current Year')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Count')
ax.grid(True)
st.pyplot(fig)

# Número de rayos por día de la semana
st.subheader('Number of Lightning Strikes by Day of the Week')
alaskaP['day_of_week'] = alaskaP['STRIKETIME'].dt.dayofweek
day_of_week_counts = alaskaP['day_of_week'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=day_of_week_counts.index, y=day_of_week_counts.values, ax=ax)
ax.set_title('Number of Lightning Strikes by Day of the Week')
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Count')
ax.set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
ax.grid(True)
st.pyplot(fig)

# Número de rayos por día en los últimos 10 días
st.subheader('Number of Lightning Strikes by Day in Last 10 Days')
last_10_days = daily_counts.tail(10)
fig, ax = plt.subplots()
sns.lineplot(x=last_10_days.index, y=last_10_days.values, marker='o', ax=ax)
ax.set_title('Number of Lightning Strikes by Day in Last 10 Days')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
ax.grid(True)
st.pyplot(fig)

