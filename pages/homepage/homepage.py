import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from pages.homepage.homepage_data import get_categories

# ? Other liked themes
# ZEPHYR
# JOURNAL

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.title='First test app on AWS'

# ! Test values
labels = ['#a9d4cb', '#8d7d43', '#080602', '#eae0b8', '#473a1b', '#6d9b97', '#ccba86', '#6c5e31', '#86bdb9', '#ac9a5e']
values = [47745, 51759, 12770, 20736, 29278, 17374, 25540, 48025, 65659, 36854]

# *** Constants ###############################################################################################################
pie = go.Pie(labels=labels, values=values, hole=.2, marker=dict(colors=labels))
fig_layout = {'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
              'xaxis': {'showgrid': False, 'visible': False},
              'yaxis': {'showgrid': False, 'visible': False}}

fig_timeline = go.Figure()
fig_timeline.update_xaxes(type='date', showgrid=False)
fig_timeline.update_yaxes(visible=False, showgrid=False)


img_link = 'https://kuleuven-datathon-2023.s3.eu-central-1.amazonaws.com/images/Jean-L%C3%A9on+G%C3%A9r%C3%B4me/Almehs+playing+Chess+in+a+Caf%C3%A9.jpg'
div_style = lambda x: {'width': x, 'vertical-align': 'top', 'display': 'inline-block'}

padding_px = '5px '
div_container_style = {'padding': (padding_px * 4).rstrip()}
# *** #########################################################################################################################


# * Functions #################################################################################################################
def generate_card(p_id, title, text, border_color):
    card = dbc.Card(children=dbc.CardBody([
                html.Center(html.H3(title)),
                html.P(id=p_id, children=[text]),
            ]), color=border_color, outline=True)
    return card

def generate_div_container(div_id, div_children, div_style):
    return html.Div(id=div_id, children=div_children, style=div_style)

# * ###########################################################################################################################

# * Layout ####################################################################################################################
homepage_layout = html.Div(children=[
    # ! ROW 1
    html.Div(id='row-1', children=[
        html.Div(id='row-1-left', children=[
            html.Center(html.H3('Selections'))
        ], style=div_style('20%'), className='aligned-divs'),
        html.Div(id='row-1-center', children=[
            html.Center(html.H3('Timeline'))
        ], style=div_style('55%'), className='aligned-divs'),
        html.Div(id='row-1-right', children=[
            html.Center(html.H3('Color information'))
        ], style=div_style('25%'), className='aligned-divs')
    ]),
    # ! ROW 2
    html.Div(id='row-2', children=[
        html.Div(id='row-2-left', children=[
            generate_div_container(div_id='dropdown-1-container',
                                   div_children=[dcc.Dropdown(id='category-selector', options=get_categories(),
                                                              placeholder='Select a category')],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='dropdown-2-container',
                                   div_children=[dcc.Dropdown(id='subcategory-selector', options=[], placeholder='Select a subcategory',
                                                              disabled=True)],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='dropdown-3-container',
                                   div_children=[dcc.Dropdown(id='artwork-selector', options=[], placeholder='Select an artwork',
                                                              disabled=True)],
                                   div_style=div_container_style),
                        
            # ? Date picker will not be used (probably)
            # generate_div_container(div_id='dropdown-3-container',
            #                        div_children=[dcc.DatePickerRange(id='date-picker', start_date_placeholder_text='Start date',
            #                                                          end_date_placeholder_text='End date')],
            #                        div_style=div_container_style),
            
            
            generate_div_container(div_id='image-container',
                                   div_children=[html.Center(html.Img(id='artwork-image', height='100%', width='100%', src=img_link))],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='left-card-container',
                                   div_children=[
                                       generate_card(p_id='picture-info-p',
                                                     title='Picture information',
                                                     text=''' Artist: Vincent Van Gogh, birthplace: The Netherlands, date: 1889,  
                                                              medium: oil on canvas, dimensions: 73 x 92 cm ''',
                                                     border_color='secondary')],
                                   div_style=div_container_style)
            
            
        ], style=div_style('15%'), className='aligned-divs'),
        html.Div(id='row-2-center', children=[
            generate_div_container(div_id='timeline-container',
                                   div_children=[dcc.Graph(id='timeline', figure=fig_timeline, config={'displayModeBar': True})],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='center-card-container',
                                   div_children=[
                                       generate_card(p_id='timeline-info-p',
                                                     title='Timeline information',
                                                     text=''' jean leon gerome, Alma playing chess, academicism, 19th century, france ''',
                                                     border_color='secondary')],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='color-card-container',
                                   div_children=[
                                       generate_card(p_id='color-info-p',
                                                     title='Color characteristics',
                                                     text=''' Dominant color: #a9d4cb, Movements with similar color themes: Cubism, Impressionism,
                                                              Artists with similar color themes: Pablo Picasso, Vincent Van Gogh ''',
                                                     border_color='secondary')],
                                   div_style=div_container_style)
            
        ], style=div_style('60%'), className='aligned-divs'),
        html.Div(id='row-2-right', children=[
            generate_div_container(div_id='color-information-container-super',
                                   div_children=[dcc.Graph(id='color-pie-chart-super', figure=go.Figure(data=[], layout=fig_layout))],
                                   div_style=div_container_style),
            
            generate_div_container(div_id='color-information-container',
                                   div_children=[dcc.Graph(id='color-pie-chart', figure=go.Figure(data=[], layout=fig_layout))],
                                   div_style=div_container_style)
            
        ], style=div_style('25%'), className='aligned-divs'),
    ]),
    # ! ROW 3
    html.Div(id='row-3', children=[
        html.Div(id='row-3-left', children=[
        #     generate_div_container(div_id='left-card-container',
        #                            div_children=[
        #                                generate_card(title='Picture information',
        #                                              text=''' Artist: Vincent Van Gogh, birthplace: The Netherlands, date: 1889,  
        #                                                       medium: oil on canvas, dimensions: 73 x 92 cm ''',
        #                                              border_color='secondary')],
        #                            div_style=div_container_style)
            
        ], style=div_style('20%'), className='aligned-divs'),
        html.Div(id='row-3-center', children=[
        #     generate_div_container(div_id='center-card-container',
        #                            div_children=[
        #                                generate_card(title='Timeline information',
        #                                              text=''' jean leon gerome, Alma playing chess, academicism, 19th century, france ''',
        #                                              border_color='secondary')],
        #                            div_style=div_container_style)
        # 
        ], style=div_style('55%'), className='aligned-divs'),
        html.Div(id='row-3-right', children=[
            # generate_div_container(div_id='right-card-container',
            #                        div_children=[
            #                            generate_card(title='Color characteristics',
            #                                          text=''' Dominant color: #a9d4cb, Movements with similar color themes: Cubism, Impressionism,
            #                                                   Artists with similar color themes: Pablo Picasso, Vincent Van Gogh ''',
            #                                          border_color='secondary')],
            #                        div_style=div_container_style)
            
        ], style=div_style('25%'), className='aligned-divs')
    ])
])
# * Layout ####################################################################################################################