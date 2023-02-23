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
    ],
    Input(component_id='subcategory-selector', component_property='value'),
    State(component_id='category-selector', component_property='value')
)
def on_subcategory_selection(subcategory, category):
    if subcategory is None:
        return [], True, go.Figure(data=[], layout=pie_fig_layout), go.Figure(data=[], layout=t_fig_layout  )
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
    
    # ! move this to homepage data when done
    # start_date = df_subcat.start_date.iloc[0]
    # end_date = df_subcat.end_date.iloc[0]
    
    # query = select(database.Events).where(and_(database.Events.start_date >= start_date, database.Events.end_date <= end_date))
    # df_events = pd.read_sql_query(sql=query, con=db.engine.connect())
    
    # print(df_events)
    # !

    
    return artwork_options, False, fig_pie, fig_timeline