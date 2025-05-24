import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from data_utils import load_tourism_funding

def app():
    st.title("🏛️ Tourism Trends & Government Funding Analysis")

    @st.cache_data
    def load_data():
        try:
            df = load_tourism_funding()
            
            
            # Standardize column names (handle variations)
            column_mapping = {
                'no. of projects': 'No. of Projects',
                'number of projects': 'No. of Projects',
                'projects': 'No. of Projects',
                'total projects': 'No. of Projects',
                'amt. sanctioned': 'Amt. Sanctioned',
                'amount sanctioned': 'Amt. Sanctioned',
                'sanctioned amount': 'Amt. Sanctioned',
                'amt. released': 'Amt. Released',
                'amount released': 'Amt. Released',
                'released amount': 'Amt. Released',
                'amt. utilised': 'Amt. Utilised',
                'amount utilised': 'Amt. Utilised',
                'utilised amount': 'Amt. Utilised',
                'status - ongoing': 'Status - Ongoing',
                'ongoing': 'Status - Ongoing',
                'status - completed': 'Status - Completed',
                'completed': 'Status - Completed',
                'name of the state': 'Name of the State',
                'state': 'Name of the State',
                'state/ut': 'Name of the State'
            }
            
            # Rename columns to standard names (case insensitive)
            df.columns = df.columns.str.lower().map(lambda x: column_mapping.get(x, x))
            
            # Clean numeric columns
            numeric_cols = ['Amt. Sanctioned', 'Amt. Released', 'Amt. Utilised', 'No. of Projects']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(',', '').astype(float)
                else:
                    st.warning(f"Column not found: {col}")
            
            return df
        
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    # Load data
    df = load_data()

    if not df.empty:
        # Check for required columns
        required_columns = ['Name of the State', 'No. of Projects', 
                          'Amt. Sanctioned', 'Amt. Released', 'Amt. Utilised']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            st.info("Please check your data file contains these columns with similar names.")
            return
        
        # Sidebar controls
        st.sidebar.header("Filters")
        selected_state = st.sidebar.selectbox(
            "Select State",
            ["All States"] + sorted(df['Name of the State'].unique().tolist())
        )

        show_completed = st.sidebar.checkbox("Show Completed Projects", value=True)
        show_ongoing = st.sidebar.checkbox("Show Ongoing Projects", value=True)
        
        # Filter data based on selections
        if selected_state != "All States":
            df_filtered = df[df['Name of the State'] == selected_state]
        else:
            df_filtered = df.copy()
        
        # Filter by project status (if columns exist)
        status_cols = []
        if show_completed and 'Status - Completed' in df_filtered.columns:
            status_cols.append('Status - Completed')
        if show_ongoing and 'Status - Ongoing' in df_filtered.columns:
            status_cols.append('Status - Ongoing')
        
        if status_cols:
            df_filtered = df_filtered[df_filtered[status_cols].any(axis=1)]

        # Main dashboard
        st.header("Funding Overview")
        
        # Key metrics (with safe calculations)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", int(df_filtered['No. of Projects'].sum()))
        with col2:
            st.metric("Total Sanctioned (₹)", f"{df_filtered['Amt. Sanctioned'].sum():,.2f}")
        with col3:
            st.metric("Total Released (₹)", f"{df_filtered['Amt. Released'].sum():,.2f}")
        with col4:
            released_total = df_filtered['Amt. Released'].sum()
            if released_total > 0:
                utilisation = (df_filtered['Amt. Utilised'].sum() / released_total) * 100
                st.metric("Utilisation Rate", f"{utilisation:.1f}%")
            else:
                st.metric("Utilisation Rate", "N/A")

        # Visualization tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "Funding Distribution", 
            "Project Status", 
            "State Comparison", 
            "Raw Data"
        ])

        with tab1:
            st.subheader("Funding Distribution Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    df_filtered, 
                    values='Amt. Sanctioned', 
                    names='Name of the State',
                    title='Sanctioned Amount by State'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_filtered.groupby('Name of the State').sum().reset_index(),
                    x='Name of the State',
                    y=['Amt. Sanctioned', 'Amt. Released', 'Amt. Utilised'],
                    title='Funding Breakdown by State',
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Project Status Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'Status - Ongoing' in df_filtered.columns and 'Status - Completed' in df_filtered.columns:
                    status_counts = df_filtered[['Status - Ongoing', 'Status - Completed']].sum()
                    fig = px.pie(
                        values=status_counts,
                        names=['Ongoing', 'Completed'],
                        title='Project Status Distribution'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Status columns not available for visualization")
            
            with col2:
                fig = px.scatter(
                    df_filtered,
                    x='Amt. Sanctioned',
                    y='Amt. Utilised',
                    color='Name of the State',
                    size='No. of Projects',
                    title='Sanctioned vs Utilised Amounts',
                    hover_data=['Name of the State']
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("State-wise Comparison")
            
            # Calculate utilisation percentage (with zero division protection)
            df_comparison = df_filtered.groupby('Name of the State').sum().reset_index()
            df_comparison['Utilisation %'] = (df_comparison['Amt. Utilised'] / 
                                             df_comparison['Amt. Released'].replace(0, np.nan)) * 100
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    df_comparison.sort_values('Amt. Sanctioned', ascending=False),
                    x='Name of the State',
                    y='Amt. Sanctioned',
                    title='Total Sanctioned Amount by State'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_comparison.sort_values('Utilisation %', ascending=False),
                    x='Name of the State',
                    y='Utilisation %',
                    title='Fund Utilisation Rate by State'
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab4:
            st.subheader("Raw Data")
            st.dataframe(df_filtered, use_container_width=True)

app()