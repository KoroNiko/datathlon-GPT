import ast
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from environment.settings import config
from sqlalchemy import select, text, and_, or_
from sqlalchemy.sql import Select
# from utils import connections
from app import datathlonDB, db, server
from utils import database
from utils import functions

# ! datetime libs import if needed

database_dir = config['DATABASE_DIR']
# dataset_dir = config['DATASET_DIR']

NUM_COLORS = 30

fig_layout = {'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
              'xaxis': {'showgrid': False, 'visible': False},
              'yaxis': {'showgrid': False, 'visible': False}}

annotation_font_size = 16


def get_categories():
    ''' Get the categories from the database for the first dropdown '''
    query = select(database.Category)
    # get the category names, cast them to list and sort them
    with server.app_context():
        df = pd.read_sql_query(sql=query, con=db.engine.connect())
        df = df.rename(columns={'name': 'label', 'id': 'value'})
        # categories = datathlonDB.execute(query).scalars().all()
        # categories = sorted(pd.read_sql_query(sql=query, con=db.engine).name.to_list())

    print(df.to_dict('records'))
 
    # return ['1']
    return df.to_dict('records')

def generate_piechart(rgb_colors: str, cluster_counts: str):
    labels = functions.rgb2hex(ast.literal_eval(rgb_colors))
    values = list(map(lambda x: x[1], sorted(ast.literal_eval(cluster_counts).items())))
    subcat_pie = go.Pie(labels=labels, values=values, hole=.2, marker=dict(colors=labels))   
    return go.Figure(data=[subcat_pie], layout=fig_layout)

def generate_timeline_figure(df):
    fig = go.Figure()
    fig.update_xaxes(type='date', showgrid=False)
    fig.update_yaxes(visible=False, showgrid=False)
    
    start_date = df.start_date.iloc[0]
    end_date = df.end_date.iloc[0]
    
    with server.app_context():
        query = select(database.Events).where(and_(database.Events.start_date >= start_date, database.Events.end_date <= end_date))
        df_events = pd.read_sql_query(sql=query, con=db.engine.connect())
        df_events.start_date = df_events.start_date.apply(lambda x: pd.Timestamp(year=x, month=1, day=1))
        df_events.end_date = df_events.end_date.apply(lambda x: pd.Timestamp(year=x, month=1, day=1))
        # ! get min events
        events_start = df_events.start_date.min()
        events_end = df_events.end_date.max()
        timeline_range = pd.date_range(start=events_start, end=events_end, freq='M')
    
    # invisible line to set xaxis
    fig.add_trace(go.Scatter(x=timeline_range, y=[0]*len(timeline_range), mode='lines', line=dict(width=0), marker=dict(opacity=0)))
    
    for i, row in df_events.iterrows():
        fig.add_vline(x=row.start_date, line_width=3, line_dash='dash', 
                      line_color='LightSkyBlue')
        
        fig.add_vline(x=row.end_date, line_width=3, line_dash='dash', 
                      line_color='LightSkyBlue')
        
        fig.add_annotation(x=row.start_date, y=2, text=row['name']+' start', showarrow=False, textangle=-90, font={'size': annotation_font_size})
        fig.add_annotation(x=row.end_date, y=2, text=row['name']+' end', showarrow=False, textangle=-90, font={'size': annotation_font_size})
        
    # for i, row in df_events.iterrows():
    #     fig.add_vrect(x0=row.start_date, x1=row.end_date, fillcolor="LightSkyBlue", opacity=0.25, 
    #                   line_width=0, hovertext=row['name'])
    
    # print(df_events)
    # print(timeline_range)
    
    return fig