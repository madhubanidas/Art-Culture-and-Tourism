import streamlit as st
from data_utils import load_tourism_statistics, load_monthly_visitors, load_tourism_by_country, load_tourism_monthly, load_state_tourism
import plotly.express as px
import pandas as pd

def app():
    st.header("✈️ Tourism Statistics")
    
    # Load all datasets
    df = load_tourism_statistics()
    state = load_state_tourism()
    monthly = load_monthly_visitors()
    tourism_by_country = load_tourism_by_country()
    tourism_monthly = load_tourism_monthly()

    st.title("📊 Tourist Visits Trend Analysis (2018-2020)")

    # STATE TOURISM DATA PROCESSING
    state_df = state.copy()
    
    # Drop serial number column if exists
    if 'Sl. No.' in state_df.columns:
        state_df = state_df.drop(columns=['Sl. No.'])
    
    # Melt and process data
    melted_df = pd.melt(
        state_df,
        id_vars=["States/UT"],
        var_name="Year_Metric",
        value_name="Value"
    )
    
    # Split Year and Metric
    split_cols = melted_df["Year_Metric"].str.split(" - ", expand=True)
    melted_df["Year"] = split_cols[0]
    melted_df["Metric"] = split_cols[1]
    
    # Filter and clean data
    melted_df = melted_df[melted_df["Year"].str.isnumeric()]
    melted_df["Year"] = melted_df["Year"].astype(int)
    melted_df["Value"] = (
        melted_df["Value"]
        .astype(str)
        .str.replace(",", "")
        .str.extract('(\d+)', expand=False)
        .astype(float)
    )
    
    # Pivot and rename
    processed_df = melted_df.pivot_table(
        index=["States/UT", "Year"],
        columns="Metric",
        values="Value"
    ).reset_index()
    processed_df.columns.name = None
    processed_df = processed_df.rename(columns={
        "DTVs": "Domestic Visits",
        "FTVs": "Foreign Visits"
    })
    processed_df["Year"] = processed_df["Year"].astype(str)
    
    # SIDEBAR CONTROLS
    st.sidebar.header("Controls")
    all_states = ["All"] + sorted(processed_df["States/UT"].unique())
    selected_state = st.sidebar.selectbox("Select State/UT", all_states)
    visit_type = st.sidebar.radio("Select Visit Type", ["Both", "Domestic", "Foreign"])
    use_log_scale = st.sidebar.checkbox("Use logarithmic scale", value=True)
    
    # Filter data
    filtered_df = processed_df if selected_state == "All" else processed_df[processed_df["States/UT"] == selected_state]
    
    # MAIN VISUALIZATIONS
    st.header("Tourist Visits Analysis")
    
    if selected_state == "All":
        # NATIONAL VIEW
        agg_df = filtered_df.groupby("Year").sum().reset_index()
        
        # National trends
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("National Trends - Domestic Visits")
            fig = px.line(agg_df, x="Year", y="Domestic Visits", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("National Trends - Foreign Visits")
            fig = px.line(agg_df, x="Year", y="Foreign Visits", markers=True, color_discrete_sequence=["orange"])
            st.plotly_chart(fig, use_container_width=True)
        
        # STATE-WISE COMPARISON CHARTS (NEW ADDITION)
        st.subheader("State-wise Comparison")

        max_val = processed_df[["Domestic Visits", "Foreign Visits"]].max().max()
        min_val = processed_df[["Domestic Visits", "Foreign Visits"]].min().min()
        range_ratio = max_val / min_val if min_val > 0 else 1000
        
            # Domestic visits by state - full height
        fig1 = px.bar(
            processed_df, 
            x="States/UT", 
            y="Domestic Visits", 
            color="Year",
            barmode="group", 
            title="Domestic Visits by State",
            log_y=use_log_scale if range_ratio > 100 else False,
            height=600  # Increased height
        )
        fig1.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1, use_container_width=True)
        
        # Foreign visits by state - full height
        fig2 = px.bar(
            processed_df, 
            x="States/UT", 
            y="Foreign Visits", 
            color="Year",
            barmode="group", 
            title="Foreign Visits by State",
            log_y=use_log_scale if range_ratio > 100 else False,
            height=600  # Increased height
        )
        fig2.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # State ranking in tabs
        st.subheader("State Ranking by Total Visits")
        state_totals = processed_df.groupby("States/UT")[["Domestic Visits", "Foreign Visits"]].sum().reset_index()
        state_totals["Total Visits"] = state_totals["Domestic Visits"] + state_totals["Foreign Visits"]
        
        tab1, tab2 = st.tabs(["Domestic Visits", "Foreign Visits"])
        with tab1:
            top_domestic = state_totals.sort_values("Domestic Visits", ascending=False)
            fig = px.bar(top_domestic.head(20), x="States/UT", y="Domestic Visits",
                        title="Top States by Domestic Visits",
                        log_y=use_log_scale if range_ratio > 100 else False)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top_domestic[["States/UT", "Domestic Visits"]].reset_index(drop=True))
        
        with tab2:
            top_foreign = state_totals.sort_values("Foreign Visits", ascending=False)
            fig = px.bar(top_foreign.head(20), x="States/UT", y="Foreign Visits",
                        title="Top States by Foreign Visits",
                        log_y=use_log_scale if range_ratio > 100 else False)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top_foreign[["States/UT", "Foreign Visits"]].reset_index(drop=True))
    
    else:
        # STATE-SPECIFIC VIEW (unchanged)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Visit Trends in {selected_state}")
            if visit_type in ["Both", "Domestic"]:
                fig = px.line(filtered_df, x="Year", y="Domestic Visits",
                             markers=True, title="Domestic Visits")
                st.plotly_chart(fig, use_container_width=True)
            
            if visit_type in ["Both", "Foreign"]:
                fig = px.line(filtered_df, x="Year", y="Foreign Visits",
                             markers=True, title="Foreign Visits",
                             color_discrete_sequence=["orange"])
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"Comparison in {selected_state}")
            fig = px.bar(filtered_df, x="Year", 
                        y=["Domestic Visits", "Foreign Visits"],
                        barmode="group", 
                        title="Domestic vs Foreign Visits Comparison")
            st.plotly_chart(fig, use_container_width=True)
    
    # Raw data
    st.subheader("Raw Data")
    st.dataframe(filtered_df.sort_values(["States/UT", "Year"]), use_container_width=True)

    # TABBED VIEWS
    tab1, tab2, tab3 = st.tabs(["Domestic vs Foreign", "Top Countries", "Monthly Trends"])

    with tab1:
        fig = px.line(df, x='Year', y=['Tourist Visits - Domestic', 'Tourist Visits - Foreign'],
                    title="Domestic vs Foreign Tourist Visits (1991-2020)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        top_countries = tourism_by_country.melt(id_vars=['Name of Countries'], 
                                            var_name='Year', value_name='Visitors')
        top_countries['Year'] = top_countries['Year'].astype(int)
        latest_year = top_countries['Year'].max()
        latest_data = top_countries[top_countries['Year'] == latest_year].nlargest(10, 'Visitors')
        
        fig = px.bar(latest_data, x='Name of Countries', y='Visitors',
                    title=f"Top 10 Countries by Visitors ({latest_year})")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = px.line(tourism_monthly.melt(id_vars=['Month'], var_name='Year', value_name='Visitors'),
                    x='Month', y='Visitors', color='Year',
                    title="Monthly Tourism Trends Over Years")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Visitors Trend")
    st.line_chart(monthly.set_index("Particulars"))
       
    st.subheader("Annual Tourist Statistics")
    st.dataframe(df)

app()