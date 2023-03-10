from re import sub
import pages.homepage.homepage_data as homepage_data
import ast
from app import app, server, datathlonDB, db
from dash import Input, Output, State
from sqlalchemy import select, and_, or_
from utils import database
from utils import functions

import pandas as pd
import plotly.graph_objects as go


pie_fig_layout = {'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
              'xaxis': {'showgrid': False, 'visible': False},
              'yaxis': {'showgrid': False, 'visible': False}}

t_fig_layout = {
    'xaxis': {'type': 'date', 'showgrid': False},
    'xaxis': {'visible': False, 'showgrid': False}}

@app.callback(
    [
      Output(component_id='subcategory-selector', component_property='options'),
      Output(component_id='subcategory-selector', component_property='disabled'),
    ],
    Input(component_id='category-selector', component_property='value'),
)
def on_category_selection(category):
    if category is None:
        return [], True   

    query = select(database.Subcategory).join(database.Category).where(database.Category.id == category)
    df = pd.read_sql_query(sql=query, con=db.engine.connect())
    subcat_dict = df[['id', 'name']].rename(columns={'id': 'value', 'name': 'label'}).to_dict('records')
    
    return subcat_dict, False
        
    
# * Affects
# * Timeline graph
# * Artwork dropdown
# * possibly add 2 color wheels (one for the selected artwork and one for the parent category of that artwork)
@app.callback(
    [
        Output(component_id='artwork-selector', component_property='options'),
        Output(component_id='artwork-selector', component_property='disabled'),
        Output(component_id='color-pie-chart-super', component_property='figure'),
        Output(component_id='timeline', component_property='figure'),
        Output(component_id='timeline-info-p', component_property='children'),
        Output(component_id='color-info-p', component_property='children')
    ],
    Input(component_id='subcategory-selector', component_property='value'),
    State(component_id='category-selector', component_property='value')
)
def on_subcategory_selection(subcategory, category):
    if subcategory is None:
        return [], True, go.Figure(data=[], layout=pie_fig_layout), go.Figure(data=[], layout=t_fig_layout),\
            '', ''
    pass
        
    # ? Pie chart for supercluster
    # ! Possible error
    # ? get the color_id of the subcategory
    subcat_color_id = pd.read_sql_query(sql=select(database.Subcategory.color_id).where(database.Subcategory.id == subcategory),
                                        con=db.engine.connect())                                        
    
    try:
        subcat_color_id = subcat_color_id.color_id[0]
    except:
        subcat_color_id = -1
    
    query_subcat_color = select(database.Colors).join(database.Subcategory).where(database.Subcategory.color_id == subcat_color_id)
    df_colors = pd.read_sql_query(sql=query_subcat_color, con=db.engine.connect())
    rgb_colors, cluster_counts = df_colors.rgb_colors.iloc[0], df_colors.cluster_counts.iloc[0]
    fig_pie = homepage_data.generate_piechart(rgb_colors, cluster_counts)
    
    # ? Artwork list for each artist
    query_artworks = select(database.Artwork).join(database.Subcategory).where(database.Artwork.subcategory_id == subcategory)
    df_artworks = pd.read_sql_query(sql=query_artworks, con=db.engine.connect())
    artwork_options = df_artworks[['id', 'name']].rename(columns={'id': 'value', 'name': 'label'}).to_dict('records')
    # artwork_options = [{'label': 'd', 'value': '1'}]
    # print(df_artworks)
    
    # ? Timeline graph
    df_subcat = pd.read_sql_query(sql=select(database.Subcategory).where(database.Subcategory.id == subcategory), con=db.engine.connect())
    fig_timeline = homepage_data.generate_timeline_figure(df_subcat)
      
    # ? Timeline info paragraph text
    info_text = df_subcat.caption.iloc[0]
    
    # ? Color info text:
    color_text = homepage_data.get_color_information(rgb_colors, cluster_counts, title_str='Subcategory Colors')
      
    return artwork_options, False, fig_pie, fig_timeline, info_text, color_text


@app.callback(
    [
        Output(component_id='picture-info-p', component_property='children'),
        Output(component_id='color-pie-chart', component_property='figure'),
        Output(component_id='artwork-image', component_property='src'),
        # Output(component_id='color-info-p', component_property='children')
    ],
    Input(component_id='artwork-selector', component_property='value'),
    State(component_id='color-info-p', component_property='children')
)
def on_artwork_selection(artwork, color_info):
    if artwork is None:
        return 'None', go.Figure(data=[], layout=pie_fig_layout), ''
    
    print(color_info)
    
    query = select(database.Colors, database.Artwork).where(database.Artwork.id == artwork)
    df = pd.read_sql_query(sql=query, con=db.engine.connect())
    # artwork_color = select(database.Colors).join(database.Artwork).where(database.Artwork.id == artwork)
    # df_colors = pd.read_sql_query(sql=artwork_color, con=db.engine.connect())
    rgb_colors, cluster_counts = df.rgb_colors.iloc[0], df.cluster_counts.iloc[0]
    url = df.url.iloc[0]
    p_text = df.summary.iloc[0]
    
    fig_pie = homepage_data.generate_piechart(rgb_colors, cluster_counts)
    
    # ? Artwork color info text
    # color_text = homepage_data.get_color_information(rgb_colors, cluster_counts, title_str='Artwork Colors')
    # color_info.extend(color_text)

    return p_text, fig_pie, url