import streamlit as st
from data_utils import load_destinations,load_tourism_website
from map_visualizer import create_india_map
import pandas as pd
import wikipediaapi
import plotly.express as px


def show_destination_details(row, index):
    """Display rich destination details"""
    with st.expander(f"🏛️ {row['Destination']} ({row['State']})", expanded=False):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            df_map = pd.DataFrame({
                'LATITUDE': [row['LATITUDE']],
                'LONGITUDE': [row['LONGITUDE']],
                'Destination': [row['Destination']]
            })
            fig = px.scatter_mapbox(
                df_map,
                lat="LATITUDE",
                lon="LONGITUDE",
                hover_name="Destination",
                zoom=12,
                height=300
            )
            fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True, key=f"plot_{index}")
            st.caption(f"Coordinates: {row['LATITUDE']:.4f}, {row['LONGITUDE']:.4f}")

        with col2:
            st.markdown(f"""
            ### Cultural Significance
            # e
            {row['CULTURAL_IMPORTANCE']}
            
            **State**: {row['State']}
            """)
            
            # Fetch more details on demand
            if st.button("Get deeper historical context", key=f"more_{row['Destination']}_{index}"):
                with st.spinner("Fetching detailed information..."):
                    wiki = wikipediaapi.Wikipedia(
                    language='en',
                    user_agent="STREAMLIT/1.0 (madhubanidas@gmail.com)")
                    page = wiki.page(row['Destination'])
                    if page.exists():
                        sections = "\n\n".join(
                            f"### {s.title}\n{s.text}" 
                            for s in page.sections if s.title in 
                            ["History", "Architecture", "Cultural Importance"]
                        )
                        st.markdown(sections)
                    else:
                        st.warning("No additional information found")

def app():
    st.title("🗺️ Cultural Destinations of India")
    
    with st.spinner("Loading cultural destinations (this may take a minute for first run)..."):
        df = load_destinations()
        links=load_tourism_website()
    
    if df.empty:
        st.error("No destination data found!")
        return
    
    required_cols = ['LATITUDE', 'LONGITUDE', 'Destination', 'State']
    if not all(col in df.columns for col in required_cols):
                st.error(f"Missing required columns. Needed: {required_cols}")
                st.write("Current columns:", df.columns.tolist())
                return
    
    tab1, tab2 , tab3 = st.tabs(["Interactive Map", "Destination Explorer", "Tourism Links"])
    
    with tab1:
        st.subheader("Explore Cultural Sites")
        fig = create_india_map(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Detailed Information")
        
        
        selected_State = st.selectbox(
            "Filter by State",
            ["All"] + sorted(df['State'].unique()),
            index=0
        )
        
        
        filtered_df = df if selected_State == "All" else df[df['State'] == selected_State]
        
     
        search_query = st.text_input("Search destinations")
        if search_query:
            filtered_df = filtered_df[
                filtered_df['Destination'].str.contains(search_query, case=False) |
                filtered_df['CULTURAL_IMPORTANCE'].str.contains(search_query, case=False)
            ]
        
        
        for index, row in filtered_df.iterrows():
            show_destination_details(row, index)
            st.markdown("---")
    with tab3:
        st.subheader("Tourism Links")
        st.markdown("""
        Here are the links to the official tourism websites of various states in India. 
        """)

        # Filter out rows where Website Url is missing or empty
        valid_links = links[links["Website Url"].notna() & (links["Website Url"].str.strip() != "")]
        # Remove leading/trailing whitespace and tabs from State Name
        valid_links["State Name"] = valid_links["State Name"].str.strip().str.replace('\t', '', regex=True)
        # Display as a table with clickable links
        def make_clickable(val):
            return f'<a href="{val}" target="_blank">{val}</a>'
        table = valid_links[["State Name", "Website Url"]].copy()
        table["Website Url"] = table["Website Url"].apply(make_clickable)
        st.write(
            table.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

app()            

