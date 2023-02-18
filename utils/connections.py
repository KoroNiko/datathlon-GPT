import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from environment.settings import config

database_dir = config['DATABASE_DIR']

engine_database = db.create_engine('sqlite:///'+database_dir)
session_db = sessionmaker(engine_database)
