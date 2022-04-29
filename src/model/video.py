import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_json(os.path.join(os.getcwd(), "env","config","default.json"))

db = SQLAlchemy(app)

class Videos(db.Model):

    __tablename__ = "videos"
    __table_args__ = {'mysql_charset' : 'utf8mb4'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bvid = db.Column(db.String(32))
    aid = db.Column(db.Integer)

    pic = db.Column(db.String(128))
    title = db.Column(db.String(128))
    pubdate = db.Column(db.Integer)
    desc = db.Column(db.String(256))
    owner = db.Column(db.Integer)  # mid

    view = db.Column(db.Integer)
    danmaku = db.Column(db.Integer)
    reply = db.Column(db.Integer)
    favorite = db.Column(db.Integer)
    coin = db.Column(db.Integer)
    share = db.Column(db.Integer)
    like = db.Column(db.Integer)
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def query(aid):
        video = Videos.query.filter(Videos.aid == aid).first()
        return video
   
def addVideo(data):
    if data==None:
        return 
    video=Videos(
        bvid = data['bvid'],
        aid = data['aid'],
        pic = data['pic'],
        title = data['title'],
        pubdate = data['pubdate'],
        #desc = data['desc'],
        owner = data['owner']['mid'],  # mid
        view = data['stat']['view'],
        danmaku = data['stat']['danmaku'],
        reply = data['stat']['reply'],
        favorite = data['stat']['favorite'],
        coin = data['stat']['coin'],
        share = data['stat']['share'],
        like = data['stat']['like'],
    )
    print(data['bvid']+"(aid:"+str(data['aid'])+"): "+data['title'])
    video.insert()
