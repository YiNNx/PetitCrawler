from flask import request
from crawler import crawler
import json
from model.video import app

@app.route('/video', methods=[ 'GET'])
def getVideo():
    bv=request.args.get('bv')

    data_v=crawler.getVideoInfo(bv)
    _,data_c=crawler.getComments(data_v["aid"])
    res=initResponse(data_v,data_c)
    return json.dumps(res)

def initResponse(data_v,data_c):
    video={
        "bvid": data_v['bvid'],
        "aid": data_v['aid'],
        "pic": data_v['pic'],
        "title": data_v['title'],
        "pubdate": data_v['pubdate'],
        "desc": data_v['desc'],
        "owner": data_v['owner']['mid'], 
        "view": data_v['stat']['view'],
        "danmaku": data_v['stat']['danmaku'],
        "reply": data_v['stat']['reply'],
        "favorite": data_v['stat']['favorite'],
        "coin": data_v['stat']['coin'],
        "share": data_v['stat']['share'],
        "like": data_v['stat']['like'],
    }
    comments=[]
    for c in data_c:
        comment={
            "rpid": c['rpid'],
            "mid": c['mid'],
            "uname": c['member']['uname'],
            "content": c['content']['message'],
            "ctime": c['ctime'],
            "like": c['like'],
            "rcount": c['rcount'],
        }
        comments.append(comment)
    res={
        "video_info":video,
        "comments":comments
    }
    return res