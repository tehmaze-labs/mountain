# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Import Flask
from .app import app

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
