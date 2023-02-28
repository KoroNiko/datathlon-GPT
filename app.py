import dash
import dash_bootstrap_components as dbc
import flask
import os
from flask_sqlalchemy import SQLAlchemy


from dash import html, dcc
# from pages.homepage.homepage import homepage_layout

server = flask.Flask(__name__)

app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.JOURNAL])

app.title = 'Datathlon - GPT'
# app.layout = homepage_layout

server.config['SQLALCHEMY_DATABASE_URI'] = '''mysql+pymysql://<username>:<password>@last-database-gpt.c8s8i66l2ado.us-east-1.rds.amazonaws.com/main'''

db = SQLAlchemy()
db.init_app(server)
datathlonDB = db.session
