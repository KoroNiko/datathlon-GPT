import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

# ? Other liked themes
# ZEPHYR
# JOURNAL

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.title='First test app on AWS'

import os

test = 'False'
if 'RDS_HOSTNAME' in os.environ:
    test = 'True'
    DATABASES = {
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }   

layout = html.Div(children=[
    html.Div(children=[
        html.H2(test), 
    ])
])

app.layout = layout


# * Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8080)