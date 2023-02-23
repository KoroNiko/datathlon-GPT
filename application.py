import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

# ? Other liked themes
# ZEPHYR
# JOURNAL

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
application = app.server
app.title='First test app on AWS'

import os

application.config['SQLALCHEMY_DATABASE_URI'] = '''mysql+pymysql://admin:XNQD6TkkB665b9p@last-database-gpt.c8s8i66l2ado.us-east-1.rds.amazonaws.com/main'''


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

# application.config['SQLALCHEMY_DATABASE_URI'] = '''mysql+pymysql://admin:XNQD6TkkB665b9p@last-database-gpt.c8s8i66l2ado.us-east-1.rds.amazonaws.com/main'''
application.config['SQLALCHEMY_DATABASE_URI'] = f'''mysql+pymysql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}/{DATABASES['NAME']}'''


layout = html.Div(children=[
    html.Div(children=[
        html.H2(DATABASES['NAME']), 
        html.H2(DATABASES['USER']), 
        # html.H2(DATABASES['PASSWORD']), 
        # html.H2(DATABASES['HOST']), 
        # html.H2(DATABASES['PORT']), 
        html.H2('SUCCESS'),
        html.H2(str(application.config['SQLALCHEMY_DATABASE_URI'])),
        
    ])
])

app.layout = layout


# * Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)
