import os 
from dotenv import dotenv_values

# No need to set environment variables on computer
env_path = os.getcwd()+'/environment/.env'
config = dotenv_values(env_path)