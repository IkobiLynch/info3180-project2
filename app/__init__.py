from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import models 
from app import views