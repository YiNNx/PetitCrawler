import os
from flask import Flask,request
from crawler import video_info,replies
from model import video
from model import reply
import json

app = Flask(__name__)
app.config.from_json(os.path.join(os.getcwd(), "env","config","default.json"))


@app.route('/video', methods=[ 'GET'])
def comments():
    bv=request.args.get('bv')

    data=video_info.getVideoInfo(bv)
    v=initVideo(data)
    _,datalist=replies.getComments(v["aid"])
    comments=[]
    for data in datalist:
       comments.append(initComment(data))
    res=initResponse(v,comments)
    return json.dumps(res)

def initVideo(data):
    video={
        "bvid": data['bvid'],
        "aid": data['aid'],
        "pic": data['pic'],
        "title": data['title'],
        "pubdate": data['pubdate'],
        "desc": data['desc'],
        "owner": data['owner']['mid'],  # mid
        "view": data['stat']['view'],
        "danmaku": data['stat']['danmaku'],
        "reply": data['stat']['reply'],
        "favorite": data['stat']['favorite'],
        "coin": data['stat']['coin'],
        "share": data['stat']['share'],
        "like": data['stat']['like'],
    }
    return video

def initComment(data):
    c={
        "rpid": data['rpid'],
        "oid": data['oid'],
        "mid": data['mid'],
        "root": data['root'],
        "dialog": data['dialog'],
        "rcount": data['rcount'],
        "ctime": data['ctime'],
        "like": data['like'],
        "uname": data['member']['uname'],
        "content": data['content']['message'],
    }
    return c
    
def initResponse(video,comments):
    res={
        "video_info":video,
        "comments":comments
    }
    return res