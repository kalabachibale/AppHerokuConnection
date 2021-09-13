
####################### Libraries:

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import os
import flask
import folium
import psycopg2
import psycopg2.extras
from flask import Flask
from folium import plugins

####################### Heroku Postgres credentials:

DB_HOST = "ec2-54-83-137-206.compute-1.amazonaws.com"
DB_NAME = "dap843a1d3ps5h"
DB_USER = "tshfxhtoyeduqt"
DB_PASS = "014b8fccc95890b13555dffff636824be3dc668fbe692537df58828ae532fe22"

############### Postgres Connection:

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
sql = "SELECT * FROM hotspot;"
data = pd.read_sql_query(sql, conn)
data = data.drop(['index'], axis=1)
data.head()
print(data.head())


############### Folium Map:

app = Flask(__name__)

@app.route('/')
def index():

    KZN = folium.Map(location=[-28.503833,
                           30.8875009],
                 zoom_start=7,
                 control_scale=True)

    Unrest_marker_cluster = plugins.marker_cluster.MarkerCluster(name='Hotspot Towns', show=False).add_to(KZN)

    for lat, lon, Town in zip(data["Latitude"].values.tolist(),
                          data["Longitude"].values.tolist(),
                          data["Town"].values.tolist()):
        folium.Marker(location=[lat, lon],
                  popup=folium.Popup('Hotspot Town: ' + Town
                                     , min_width=300, max_width=300, height=300),
                  icon=folium.Icon(color="red", icon="fire", prefix="fa"),
                  ).add_to(Unrest_marker_cluster)

## layer Control:

    folium.LayerControl().add_to(KZN)

## Mini Map:

    minimap = plugins.MiniMap()
    minimap.add_to(KZN)



# KZN.save("index.html")


    return KZN._repr_html_()
#
#
#
if __name__ == '__main__':
    app.run()
#
#
# KZN.save("index.html")




