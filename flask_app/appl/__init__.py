import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.BaseConfig')

db = SQLAlchemy(app)

import appl.views