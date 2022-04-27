import requests

url = "https://api.bilibili.com/x/space/arc/search"

headers = {
    'cookie': '''_uuid=89749BC4-915F-26EC-7A84-58D10974DE38351277infoc; buvid3=9325CE85-DB9D-42E6-91A6-BCA74ECCB83D167634infoc; b_nut=1639830051; LIVE_BUVID=AUTO9716408611877552; rpdid=|(umJmYJmlYY0J'uYR|)YulJJ; buvid4=F5D509EC-7401-B7B0-464A-E55B636309A189874-022020801-CovTCvxmuQ/mZ1Amd1O0og==; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; CURRENT_QUALITY=64; nostalgia_conf=-1; fingerprint=3591514e8945926c758532a45fe3d2e8; sid=4ivymv2u; bp_video_offset_24340948=653249128266989600; bsource=search_google; b_ut=7; b_lsid=784102EB3_18064D75527; buvid_fp=bd1f88a7f5a689fbd925a4d360d2b431; innersign=1; CURRENT_FNVAL=4048; PVID=1''',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://space.bilibili.com/27534330',
}

def setParams(mid,ps="50", pn="1"):
    params = {
        "mid": mid,  # up主id
        "ps": ps,  # 条数 max=50
        "pn": pn,  # 页数
        "order": "pubdate",  # 按时间排序 click：按播放量排序
    }
    return params

def getVideoList():
    pn=1
    aid_list=[]
    bv_list=[]
    while True:
        params = setParams("50", str(pn))
        pn+=1
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        vlist = data['data']['list']['vlist']
        if vlist==[]:
            break
        print(vlist[0])
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