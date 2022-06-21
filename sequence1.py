import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import streamlit as st

from os import listdir

# Position of the page
st.set_page_config(layout='wide')
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 2rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Importing data
df = pd.read_parquet('data/df_video.parquet')

image = Image.open('data/logo_vinci.png')
col1, col2, col3 = st.columns([5,7,4])

with col1:
    st.markdown('<p style="font-family:Calibri; color:#1C5D84; font-size: 60px;">Smart Data Hub</p>', unsafe_allow_html=True)
with col2:
    st.write("")
with col3:
    st.image(image, width =300)


# Side bar

airport = st.sidebar.selectbox("Airport", df.homeAirportCode.unique().tolist())
jet_fuel = st.sidebar.slider('Jet Fuel Price', 200, 1000, 482, format="%d $")
add_factor = st.sidebar.multiselect( "Additional Factors", ['None', 'Influencers Campaign', 'Promo Campaign', 'Weather Hazard'])
pred = st.sidebar.button('Predict')

# Displaying a variable according to the chosen parameters
var_to_display = ""
if (pred | (add_factor == "Promo Campaign")) & (jet_fuel > 500):
    var_to_display = "_increaseFuel"       
if pred & (jet_fuel > 500) & (add_factor == "Promo Campaign"):
    var_to_display = "_influencer"    
 
df_id = df.query('homeAirportCode == @airport')

fig1 = px.line(df_id.query('snapshotDate == "2022-01-31"'),  x="movementDate", y=['pax'], color_discrete_sequence=['#1C5D84'])
fig2 = px.line(df_id.query(f'snapshotDate == "2022-05-09"'), x="movementDate", y=['pax_pred'+var_to_display], color_discrete_sequence=['red', 'blue', 'green'])
fig2.update_traces(patch={"line": {"dash": 'dot'}})

fig_final = go.Figure()               
fig_final.add_traces(data=fig1.data + fig2.data)

fig_final.update_layout(title=f'Airport {airport} | Pax forecast',
                        autosize=False,
                        width=1400, height=300,
                        margin=dict(l=0, r=0, b=0, t=40),
                        showlegend=False,
                        font_color="#1C5D84",
                        title_font_color="#1C5D84")

st.plotly_chart(fig_final)

# col1, col2, = st.columns([7,3])

# with col1:
#     with st.expander("Predictive Modeler Input Variables"):
#         st.image(Image.open('data/features.png'), width =600)

size_image=44

with st.expander("Predictive Modeler Input Variables"):
    col1, col2, col3, col4 = st.columns([0.5, 2, 0.5, 5])
    
    with col1:
        st.image(Image.open('data/oag_flights.png'), width =size_image)
        st.image(Image.open('data/oag_seats.png'), width =size_image)
        st.image(Image.open('data/calendar.png'), width =size_image)
    with col2:
        st.write("")
        st.write("""OAG Flights per Airline""")
        st.write("")
        st.write("""OAG Seats per Airline""")
        st.write("")
        st.write("""Calendar & Holidays""")
    with col3:
        st.image(Image.open('data/traffic_hist.png'), width =size_image)
        st.image(Image.open('data/routes.png'), width =size_image)
        st.image(Image.open('data/travel_restri.png'), width =size_image)
    with col4:
        st.write("")
        st.write("Traffic History")
        st.write("")
        st.write("Routes")
        st.write("")
        st.write("Travel Restrictions")
            