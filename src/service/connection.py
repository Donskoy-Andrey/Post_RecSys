from dotenv import load_dotenv
import os
import logging
import warnings

"""
INSTALL LIBRARIES:
    pip install -r requirements.txt    

START SERVICE:
    python -m uvicorn src.service.service:app --reload --port 8899     
"""

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
warnings.filterwarnings("ignore")

database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
port = os.environ.get('PORT')

CONNECTION = f"postgresql://{user}:{password}@{host}:{port}/{database}"

