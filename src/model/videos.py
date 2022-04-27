from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config.from_object(config)


db = SQLAlchemy(app)

class Videos(db.Model):

    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    bvid = db.Column(db.String(32))
    aid = db.Column(db.Integer)

    pic = db.Column(db.String(128))
    title = db.Column(db.String(128))
    pubdate = db.Column(db.Integer)
    desc = db.Column(db.String(256))
    owner = db.Column(db.Integer) #mid

    view= db.Column(db.Integer)
    danmaku= db.Column(db.Integer)
    reply= db.Column(db.Integer)
    favorite= db.Column(db.Integer)
    coin= db.Column(db.Integer)
    share= db.Column(db.Integer)
    like= db.Column(db.Integer)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    
    def query(aid):
        video = Videos.query.filter(Videos.aid==aid).first()
        return video

    
