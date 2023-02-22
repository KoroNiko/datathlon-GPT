import ast
import numpy as np
import pandas as pd

from environment.settings import config
from sqlalchemy import select, text, and_, or_
from sqlalchemy.sql import Select
from utils import connections
from utils import database

database_dir = config['DATABASE_DIR']
# dataset_dir = config['DATASET_DIR']

NUM_COLORS = 10

def get_categories():
    ''' Get the categories from the database for the first dropdown '''
    query = select(database.Category)
    with connections.session_db() as con:
        # get the category names, cast them to list and sort them
        categories = sorted(pd.read_sql_query(sql=query, con=con.connection()).name.to_list())
    return categories