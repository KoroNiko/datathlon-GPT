import dash
import dash_core_components as dcc
from dash import html

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

application = app.server
app.title='First test app on AWS'

########### Set up the layout
app.layout = html.Div(children=[
    html.Center(html.H1(children='Hello GPT')),
    html.Center(html.H2(children='We are going to win those CoolBlue vouchers! (maybe)'))
])

########### Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)