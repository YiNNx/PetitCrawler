from crawler import proxy
from config import config

url = "https://api.bilibili.com/x/space/arc/search"

cookie=config.load()['cookie']

headers = {
    'cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://www.bilibili.com/video/BV18r4y1C7xo/?spm_id_from=333.788.recommend_more_video.0',
}


def setParams(mid,ps="50", pn="1"):
    params = {
        "mid": mid,  # up主id
        "ps": ps,  # 条数 max=50
        "pn": pn,  # 页数
        "order": "pubdate",  # 按时间排序 click：按播放量排序
    }
    return params



def getVideoList(mid):
    pn=1
    aid_list=[]
    bv_list=[]
    
    
    while True:
        params = setParams(mid,"50", str(pn))
        pn+=1
        r=proxy.getResByProxy(url,headers,params)
        data = r.json()
        vlist = data['data']['list']['vlist']
        if vlist==[]:
            break
        #print(vlist[0])
        for v in vlist:
            #print(v["aid"])
            aid_list.append(v["aid"])
            bv_list.append(v["bvid"])
            
    return aid_list,bv_list

if __name__ == "__main__":
    pass

'''
data sample:

{
        "list": {
            "tlist": {
                "1": {
                    "tid": 1,
                    "count": 26,
                    "name": "动画"
                },
                "167": {
                    "tid": 167,
                    "count": 42,
                    "name": "国创"
                },
                "3": {
                    "tid": 3,
                    "count": 11,
                    "name": "音乐"
                },
                "4": {
                    "tid": 4,
                    "count": 270,
                    "name": "游戏"
                },
                "5": {
                    "tid": 5,
                    "count": 1,
                    "name": "娱乐"
                }
            },
            "vlist": [
                {
                    "comment": 2158,
                    "typeid": 172,
                    "play": 183373,
                    "pic": "http://i2.hdslb.com/bfs/archive/90686dcaa6bc5e15cccdce28dcf1152d68493dd3.jpg",
                    "subtitle": "",
                    "description": "《崩坏3》亚太锦标赛，即将于5月来袭！\n本次比赛共有上海站、台北站、首尔站、曼谷站四个分站赛，每个分站赛的冠亚军队伍将会被邀请至上海参与最终决战！\n激烈的比赛期待舰长的踊跃参与，具体赛程和报名活动请多多关注爱酱的后续公告哦~",
                    "copyright": "1",
                    "title": "《崩坏3》亚太锦标赛即将来袭！",
                    "review": 0,
                    "author": "崩坏3第一偶像爱酱",
                    "mid": 27534330,
                    "created": 1554177621,
                    "length": "01:16",
                    "video_review": 250,
                    "aid": 47980972,
                    "bvid": "BV17b411p7vU",
                    "hide_click": false,
                    "is_pay": 0,
                    "is_union_video": 0,
                    "is_steins_gate": 0,
                    "is_live_playback": 0
                },
                ...
            ]
        },
        "page": {
            "pn": 6,
            "ps": 50,
            "count": 350
        },
        "episodic_button": {
            "text": "播放全部",
            "uri": "//www.bilibili.com/medialist/play/27534330?from=space"
        }
    }
'''