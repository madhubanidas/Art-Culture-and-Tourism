import streamlit as st

def app():
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    ## India Cultural Heritage Explorer
    
    A comprehensive digital platform showcasing India's rich cultural heritage and tourism patterns.
    """)
    
    
    import streamlit as st
from PIL import Image

def app():
    st.title("About India Cultural Explorer")
    
    # Header with image
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("assets/images/india_heritage.jpg", width=300)
    with col2:
        st.markdown("""
        ## Preserving India's Cultural Tapestry
        A data-driven platform showcasing India's diverse heritage through interactive exploration
        """)
    
    st.markdown("---")
    
    # Project Overview
    st.header("🌍 Project Vision")
    st.markdown("""
    **Design, develop, and produce a solution on Streamlit that:**
    - Showcases traditional art forms
    - Uncovers cultural experiences across India
    - Promotes responsible tourism practices
    
    Our platform bridges technology and culture, making India's heritage accessible to everyone while supporting preservation efforts.
    """)
    
    # Context Section
    with st.expander("📜 Cultural Context", expanded=True):
        st.markdown("""
        India's art and culture space is incredibly diverse and rich, encompassing:
        - 5,000+ years of continuous civilization
        - 8 classical dance forms
        - 1,600+ spoken languages
        - 40+ UNESCO World Heritage Sites
        
        This diversity is influenced by ancient traditions, regional variations, and modern interpretations, 
        creating a living cultural mosaic that we aim to document and celebrate.
        """)
    
    # Methodology
    st.header("🔧 How We Built It")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        ### Data Collection
        - Government open data portals
        - Tourism ministry datasets
        """)
    with cols[1]:
        st.markdown("""
        ### Technology Stack
        - Streamlit (Frontend)
        - Pandas (Data Processing)
        - Plotly (Visualizations)
        - Wikipedia API (Cultural Context)
        """)
    with cols[2]:
        st.markdown("""
        ### Key Features
        - Interactive heritage maps
        - Cultural significance analysis
        - Tourism trend visualizations
        - Responsible travel guides
        """)
    
    
    st.markdown("---")
    st.header("📚 Project Resources")
    st.markdown("""
    ### Data Sources
    1. [Government of India Open Data](https://data.gov.in)
    
    
    ### Research Methodology
    - Data-first approach to cultural documentation
    - Geospatial analysis of heritage sites
    - Temporal tourism pattern tracking
    - Community-sourced validation
    """)
    
    
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;  border-radius: 10px;">
        <p>© 2023 India Cultural Explorer | Made with ❤️ for India's heritage</p>
        <p>Supported by the Open Heritage Initiative</p>
    </div>
    """, unsafe_allow_html=True)


app()