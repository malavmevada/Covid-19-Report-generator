import plotly.express as px
import json
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from datetime import date,timedelta

#Create inida map using go.Choropleth
def create_india_map(df,color,name,day):

    #load geojson file for india
    india_states = json.load(open("./data/states_india.geojson", "r"))
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    fig = go.Figure(data=go.Choropleth(
        locations=df["id"],     #common in both file (datafile and geojson file)
        z=df['total'],           #thing you want to see
        text=df['states'],         #text when hover map
        geojson=india_states,
        colorscale=color,
        autocolorscale=False,
        reversescale=True,
        marker_line_color='peachpuff',
        marker_line_width=0.5,
        colorbar_title=f'{name} Cases',

        colorbar=dict(
            thickness=15,
            len=0.55,
            bgcolor='rgba(255,255,255,0.6)',
        )
    ))

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_geos(
        visible=False,
        projection=dict(
            type='miller',
            parallels=[86.472944444, 98.172805555556],
            rotation={'lat': 24, 'lon': 80}
        ),
    )

    fig.update_layout(
        title=dict(
            text=f"{name} COVID-19 Cases in India State wise till {day}",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 70, 'l': 0, 'b': 0},
    )
    # fig.show()
    pio.write_image(fig, f'./image/{name}.png',width=800,height=700)

