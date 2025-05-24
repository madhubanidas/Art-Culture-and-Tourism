import streamlit as st
from data_utils import  load_hotel_data
import pandas as pd

def app():
    hotels = load_hotel_data()

def visualize_hotel_data(hotels):
    st.title("🏨 India Hotel Infrastructure (2002-2012)")
    st.markdown("### Number of Hotel Rooms by Category")
    
   
    years = [str(y) for y in range(2002, 2013)]
    for year in years:
        hotels[year] = pd.to_numeric(hotels[year].replace('NA', pd.NA), errors='coerce')
    
    
    melted = hotels.melt(
        id_vars=["Particulars"],
        value_vars=years,
        var_name="Year",
        value_name="Number of Rooms"
    )
    
    
    melted['Year'] = pd.to_datetime(melted['Year'])
    
    
    chart_data = melted.pivot(
        index="Year",
        columns="Particulars",
        values="Number of Rooms"
    )
    
    
    tab1, tab2 = st.tabs(["All Categories", "Individual Categories"])
    
    with tab1:
        st.line_chart(chart_data, height=500)
    
    with tab2:
        selected_category = st.selectbox(
            "Select Hotel Category",
            options=hotels['Particulars'].unique(),
            index=0
        )
        filtered_data = chart_data[[selected_category]]
        st.line_chart(filtered_data, height=400)
        st.metric(
            label=f"Growth Rate (2002-2012)",
            value=f"{calculate_growth_rate(filtered_data):.1f}%"
        )
    
    
    with st.expander("View Raw Data"):
        st.dataframe(hotels.style.highlight_max(axis=0, color='#90EE90'), use_container_width=True)

def calculate_growth_rate(df):
    try:
        start = df.iloc[0].values[0]
        end = df.iloc[-1].values[0]
        return ((end - start) / start) * 100
    except:
        return 0

if __name__ == "__main__":
    
    data = {
        'Particulars': ['Total', 'Above Five Star', 'Five Star', 'Four Star', 
                       'Three Star', 'Two Star', 'One Star', 'Heritage', 
                       'Classification Awaited'],
        '2002': [85481, 16240, 10107, 8551, 22783, 15999, 6343, 2124, 3334],
        '2003': [91720, 16885, 10416, 8655, 26071, 17629, 6606, 2124, 3334],
        '2004': [97770, 17885, 10982, 8831, 28783, 18449, 6765, 2173, 3902],
        '2005': [67613, 15739, 7367, 5483, 19985, 5673, 1629, 1970, 9767],
        '2006': [75502, 20943, 8470, 7354, 20342, 5823, 1435, 2211, 8924],
        '2007': [83781, 20110, 9792, 7584, 24496, 6637, 1774, 2450, 10415],
        '2008': [95087, 22254, 11387, 9299, 30577, 8494, 2834, 1921, 7807],
        '2009': [92784, 23113, 11822, 8652, 23164, 6539, 2755, 2545, 12411],
        '2010': [117815, 34187, 17144, 12059, 36585, 8446, 2537, 3879, 580],
        '2011': [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        '2012': [76567, 18509, 8563, 8229, 29697, 4926, 3057, 1807, 1359]
    }
    hotels = pd.DataFrame(data)
    
    visualize_hotel_data(hotels)

app()
