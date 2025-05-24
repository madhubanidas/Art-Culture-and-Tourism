import streamlit as st
from data_utils import load_historical_sites
import plotly.express as px


def app():
    
    df = load_historical_sites()
    st.header("🏰 Cultural Heritage Sites:Puducheery")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(df, names='Nature of heritage (open space, monuments, street etc.)', 
                    title="Types of Heritage Sites")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(df, names='Heritage use', 
                    title="Current Use of Heritage Sites")
        st.plotly_chart(fig, use_container_width=True)

    st.line_chart(
    df,
    x='Name of heritage',
    y='Age of heritage (in Years)')
    st.dataframe(df)    




app()