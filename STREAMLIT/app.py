import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="India Cultural Explorer",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Home content
st.markdown("""
    <h1 style='text-align: center; color: #4682B4;'>Welcome to India Cultural Explorer</h1>
    <p style='text-align: center; font-size: 18px;'>
        Discover traditional art forms, explore cultural heritage sites, and promote responsible tourism through data and stories.
    </p>
""", unsafe_allow_html=True)

# Display Indian map image centered
image = Image.open("assets/images/india_flag.png")  # Ensure this image exists in the assets/images folder
st.image(image, caption="Map of India", use_container_width=True)
