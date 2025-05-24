import streamlit as st
from data_utils import load_geo_heritage
import plotly.express as px


def app():
    geo_heritage = load_geo_heritage()
    st.header("⛰️ Geological Heritage Sites")

    state_counts = geo_heritage['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Number of Sites']

    
    fig = px.bar(state_counts,
                 x='State', 
                 y='Number of Sites',
                 title="Geological Heritage Sites by State")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Geological Heritage Sites Data")
    st.dataframe(geo_heritage)

app()    