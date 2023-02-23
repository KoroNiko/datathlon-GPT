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

# server.config['SQLALCHEMY_DATABASE_URI'] = '''mysql+pymysql://gpt_admin:HN9gLBmeR3JiXS9@datathlondb.c8s8i66l2ado.us-east-1.rds.amazonaws.com/datathlonDB_main'''
server.config['SQLALCHEMY_DATABASE_URI'] = '''mysql+pymysql://admin:XNQD6TkkB665b9p@last-database-gpt.c8s8i66l2ado.us-east-1.rds.amazonaws.com/main'''

# DATABASES = {
#     'NAME': os.environ['RDS_DB_NAME'],
#     'USER': os.environ['RDS_USERNAME'],
#     'PASSWORD': os.environ['RDS_PASSWORD'],
#     'HOST': os.environ['RDS_HOSTNAME'],
#     'PORT': os.environ['RDS_PORT'],
# } 
# print(DATABASES)
# server.config['SQLALCHEMY_DATABASE_URI'] = f'''mysql+pymysql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}/{DATABASES['NAME']}'''

db = SQLAlchemy()
db.init_app(server)
datathlonDB = db.session