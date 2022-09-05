from dotenv import load_dotenv
import os
import logging
import warnings


load_dotenv()
logging.basicConfig(level=logging.DEBUG)
warnings.filterwarnings("ignore")

database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
port = os.environ.get('PORT')

CONNECTION = f"postgresql://{user}:{password}@{host}:{port}/{database}"

