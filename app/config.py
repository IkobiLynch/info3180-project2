import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://project2v3:project2v3@localhost/project2v3')
    
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://project2:project2@localhost/project2')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
