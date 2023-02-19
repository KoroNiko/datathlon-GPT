import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
# ZEPHYR
# JOURNAL
# ! Test values
labels = ['#a9d4cb', '#8d7d43', '#080602', '#eae0b8', '#473a1b', '#6d9b97', '#ccba86', '#6c5e31', '#86bdb9', '#ac9a5e']
values = [47745, 51759, 12770, 20736, 29278, 17374, 25540, 48025, 65659, 36854]

pie = go.Pie(labels=labels, values=values, hole=.2, marker=dict(colors=labels))

application = app.server
app.title='First test app on AWS'

def generate_card(title, text, border_color):
    card = dbc.Card(dbc.CardBody([
                html.Center(html.H3(title)),
                html.P(text),
            ]), color=border_color, outline=True)
    return card


# * App layout
layout = html.Div(children=[
    
    html.Div(id='selectors', children=[
        dcc.Dropdown(id='category-selector', options=['Artist', 'Movement', 'Century', 'Country', 'Date Range'],
                     placeholder='Select a category'),
        dcc.Dropdown(id='subcategory-selector', options=[], placeholder='Select a subcategory'),
        generate_card(title='Category information',
                      text='jean leon gerome, Alma playing chess, academicism, 19th century, france',
                      border_color='secondary')
    ], style={'width': '33%', 'display': 'inline-block'}),
    
    html.Div(id='image-data', children=[
        html.Center(html.H3('Image')),
        html.Div(children=[
            html.Center(
            html.Img(id='artwork-image', src='https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/images/Jean-L%C3%A9on+G%C3%A9r%C3%B4me/Almehs+playing+Chess+in+a+Caf%C3%A9.jpg',
                     height='100%', width='100%')
        )
        ]),
        html.Div(children=[
            generate_card(title='Picture information', 
                          text='''Arist: Vincent Van Gogh, birthplace: The Netherlands, date: 1889, 
                                  medium: oil on canvas, dimensions: 73 x 92 cm''', 
                          border_color='secondary')
        ])
        
    ], style={'display': 'inline-block'}),
    
    html.Div(id='color-information', children=[
        dcc.Graph(id='color-pie-chart', figure=go.Figure(data=[pie], layout={'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                                                                          'xaxis': {'showgrid': False, 'visible': False}, 
                                                                          'yaxis': {'showgrid': False, 'visible': False},
                                                                          'title': {'text': 'Color distribution', 'font': {'size': 20}}})),
        
        generate_card(title='Color characteristics',
                      text='''Dominant color: #a9d4cb, Movements with similar color themes: Cubism, Impressionism, 
                              Artists with similar color themes: Pablo Picasso, Vincent Van Gogh''',
                      border_color='secondary')

    ], style={'display': 'inline-block'})
], style={'display': 'flex'})



app.layout = layout



# * Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)