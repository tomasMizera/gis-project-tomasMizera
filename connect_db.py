# IPython database connection
# Run this script as: 
# 	python -i connect_db.py  OR ipython -i connect_db.py
# to stay in interpreter


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pdtuser:pdtpassword@localhost:5432/pdtdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

