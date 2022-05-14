
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import string

import etl.assess_params

def make_address(pt, address_fields=[etl.assess_params.address_col]):
    addr = ' '.join(pt[address_fields].astype(str).apply(string.capwords))
    if addr == 'Nan':
        addr = ''
    return addr

def swap_missing(x, missing_val=-1.0,
                        missing_fill='-'):
    if x == missing_val:
        return missing_fill


def make_tooltip_text(pt, value_col=etl.assess_params.value_col,
                        date_col=etl.assess_params.date_col):
    addr = make_address(pt)
    value = pt[value_col]
    if value == -1.0:
        value = ''
    else:
        value = f'\n${value:,.0f}'
    dt = pt[date_col].split("-")[0] # just yr
    if dt == -1.0:
        dt = ''
    else:
        dt = f' ({dt})'
    return addr + f"{value}{dt}"


def add_title(title_text):
    st.title(title_text)

def add_map(map_pts, lat='lat', lon='lon'):
    if not isinstance(map_pts, pd.DataFrame):
        raise TypeError("add_map() needs a dataframe")
    if lat not in map_pts.columns and lon not in map_pts.columns:
        raise ValueError("map_pts needs lat and lon columns")
    #st.map(map_pts[[lat, lon]])
    # not perfect way to do this but good enough for now
    map_centre = map_pts[lat].mean(), map_pts[lon].mean()
    m = folium.Map(location=map_centre)
    for _, i in map_pts.iterrows():
        tooltip = folium.Tooltip(text=make_tooltip_text(i))
        folium.Marker(location=[i[lat], i[lon]],
        tooltip=tooltip).add_to(m)
    map_data = st_folium(m)
