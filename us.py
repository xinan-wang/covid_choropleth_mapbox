import pandas as pd
import plotly.express as px
import json
from urllib.request import urlopen

""" US Data"""

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

df = pd.read_csv(url, dtype={"fips":str,"deaths":'Int64'})
df.head()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
  counties = json.load(response)

fig = px.choropleth_mapbox(df,geojson=counties,locations = 'fips',color='cases',
                           color_continuous_scale='jet',
                           range_color=(100, 1500),
                           mapbox_style="carto-positron",
                           hover_name='county',                           
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'cases':'Number of Cases'},
                           animation_frame = 'date'
                          )
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

fig.write_html('county_recent.html')

