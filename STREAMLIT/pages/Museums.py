import streamlit as st
from data_utils import load_museums_data
import plotly.express as px

def app():
    df = load_museums_data()
    st.header("🏛️ Museums of India")  
    tab1, tab2, tab3 = st.tabs(["By District", "Fee Structure", "Contact Info"]) 

    with tab1:
        district_data = df.groupby('District ')['Museum Name '].agg(['count', lambda x: '<br>'.join(x)]).reset_index()
        district_data.columns = ['District ', 'Number of Museums', 'Museum Names ']

        fig = px.bar(district_data,
                        x='District ',
                        y='Number of Museums',
                        hover_data=['Museum Names '],
                        title="Museums by District",
                        labels={'Number of Museums': 'Number of Museums'})
        fig.update_traces(hovertemplate=
                            "<b>%{x}</b><br>" +
                            "Museums: %{y}<br>" +
                            "<br>%{customdata[0]}<extra></extra>")

        st.plotly_chart(fig, use_container_width=True)


    with tab2:
        fig = px.pie(df, names='Fee', title="Museum Fee Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.dataframe(df[['Museum Name ', 'District ', 'Contact Numbers', 'Email.Id']],
                    hide_index=True, 
                    use_container_width=True)       

app()        