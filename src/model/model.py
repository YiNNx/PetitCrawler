from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

db = SQLAlchemy(app)

class Videos(db.Model):
    __tablename__ = "videos"
    
class Comments(db.Model):
    __tablename__ = "comments"
