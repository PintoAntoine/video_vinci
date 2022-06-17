import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import streamlit as st

from os import listdir

st.set_page_config(layout='wide')

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
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

df = pd.read_parquet('data/df_video.parquet')

airport = st.sidebar.selectbox(
    "Airport",
    df.homeAirportCode.unique().tolist()
)

jet_fuel = st.sidebar.slider(
     'Jet Fuel Price',
     200, 1000, 482)

add_factor = st.sidebar.selectbox(
    "Additional Factors",
    ['None', 'Influencers Campaign', 'Promo Campaign', 'Product Launch']
)

pred = st.sidebar.button('Predict')

var_to_display = ""
if pred:
    if jet_fuel > 500:
        var_to_display = "_increaseFuel" 
    if add_factor == "Influencers Campaign":
        var_to_display = "_influencer"
    pred = False
 
st.title("SMART FORECASTER")

df_id = df.query('homeAirportCode == @airport')

fig1 = px.line(df_id.query('snapshotDate == "2022-01-03"'), 
               x="movementDate", y=['pax'],
               color_discrete_sequence=['black'])
fig2 = px.line(df_id.query(f'snapshotDate == "2022-04-18"'),
               x="movementDate", y=['pax_pred'+var_to_display],
               color_discrete_sequence=['red', 'blue', 'green'])
fig2.update_traces(patch={"line": {"dash": 'dot'}})

fig_final = go.Figure()               
fig_final.add_traces(data=fig1.data + fig2.data)

fig_final.update_layout(title=f'Airport {airport} | Pax forecast',
                        autosize=False,
                        width=1000, height=300,
                        margin=dict(l=0, r=0, b=0, t=40),
                        showlegend=False)

st.plotly_chart(fig_final)

fig1 = px.line(df_id.query('snapshotDate == "2022-01-03"'),
               x="movementDate", y=['SPP'],
               color_discrete_sequence=['black'])
fig2 = px.line(df_id.query(f'snapshotDate == "2022-04-18"'),
               x="movementDate", y=['SPP_pred'+var_to_display],
               color_discrete_sequence=['red', 'blue', 'green'])
fig2.update_traces(patch={"line": {"dash": 'dot'}})

fig3 = px.scatter(x=["2022-04-25"], y=[8], symbol_sequence=['triangle-up'])
fig3.update_traces(marker=dict(size=30, color='red'))
fig3.update_traces(hovertemplate="EJU moved from T1 to T2")

fig_final = go.Figure()               
fig_final.add_traces(data=fig1.data + fig2.data + fig3.data)
fig_final.add_annotation(x="2022-04-25", y=8.1, text="!", showarrow=False, font=dict(size=20, color="white"))
fig_final.update_layout(title=f'Airport {airport} | Pax forecast',
                        autosize=False,
                        width=1000, height=300,
                        margin=dict(l=0, r=0, b=0, t=40),
                        showlegend=False)

st.plotly_chart(fig_final)