import streamlit as st
from data_utils import load_resident_departures
import pandas as pd

def app():

    st.subheader("Resident Departures (as a trend indicator)")
    departures = load_resident_departures()
    st.line_chart(departures.set_index("Particulars"))

app()