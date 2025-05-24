import plotly.express as px
import pandas as pd
from textwrap import wrap

def create_india_map(df):
    # Wrap long text for better hover display
    df['HOVER_TEXT'] = df.apply(lambda x: 
        f"<b>{x['Destination']}</b><br>"
        f"<i>{x['State']}</i><br><br>"
        f"{'<br>'.join(wrap(x['CULTURAL_IMPORTANCE'], width=50))}", 
        axis=1)
    
    fig = px.scatter_mapbox(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="Destination",
        hover_data={
            "State": True,
            "HOVER_TEXT": True,
            "LATITUDE": False,
            "LONGITUDE": False
        },
        color_discrete_sequence=["#589b77"],
        zoom=4,
        height=1000
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 20.5937, "lon": 78.9629},
        margin={"r":0,"t":0,"l":0,"b":0},
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=14,
            font_family="Arial"
        )
    )
    
    fig.update_traces(
        marker=dict(size=12, opacity=0.8),
        hovertemplate="%{customdata[1]}<extra></extra>"
    )
    
    return fig