import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from pages.homepage.homepage import homepage_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.title = 'Datathlon - GPT'
app.layout = homepage_layout