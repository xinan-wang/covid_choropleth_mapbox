import plotly.express as px
import json
from urllib.request import urlopen

""" UK Data"""

from uk_covid19 import Cov19API

ltla = [
    "areaType=ltla"
]

utla = [
    "areaType=utla"
]

data = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "cases": "newCasesBySpecimenDate"
}

apil = Cov19API(
    filters=ltla,
    structure=data
)

apiu = Cov19API(
    filters=utla,
    structure=data
)

df_l = apil.get_dataframe()
df_u = apiu.get_dataframe()

df = df_l.append(df_u).drop_duplicates(subset=['areaName', 'date'])
print(df.head())

df.loc[df['areaName']=='Buckinghamshire', 'areaCode'] = 'E06000060'

df_today = df[df['date']=='2021-05-01']
df_today

with urlopen('https://opendata.arcgis.com/datasets/db23041df155451b9a703494854c18c4_0.geojson') as f:
    l_a = json.load(f)

fig = px.choropleth_mapbox(df_today, geojson=l_a,
                           featureidkey = 'properties.LAD20CD',
                           locations = 'areaCode',
                           color='cases',
                           color_continuous_scale='jet',
                           range_color=(0,max(df_today.cases)),
                           mapbox_style="carto-positron",
                           hover_name='areaName',                           
                           zoom=4, center = {"lat": 55, "lon": -2},
                           opacity=0.5,
                           labels={'case':'Number of Cases'}
                          )
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})



