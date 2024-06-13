---
title: "Alaska Lightning Strikes Visualization"
emoji: "⚡"
colorFrom: "blue"
colorTo: "purple"
sdk: "streamlit"
sdk_version: "1.9.0"
app_file: app.py
pinned: false
---

# Alaska Lightning Strikes Visualization

This project visualizes lightning strikes in Alaska using `geopandas` and `contextily` to plot the data on an interactive map in a Streamlit application.

## Description

This application reads lightning strike data from a shapefile, projects it to a different coordinate reference system, and plots it on an interactive map with a basemap for better visualization. The data is plotted using `geopandas` and the basemap is added using `contextily`.

## Setup

To run this application, you need the following dependencies:

- `streamlit`
- `geopandas`
- `contextily`
- `matplotlib`

These dependencies are listed in the `requirements.txt` file and will be automatically installed when you deploy this application on Hugging Face Spaces.

## Usage

To use the application:

1. Input the shapefile path to load the data.
2. The application will process the data and visualize it on a map.


