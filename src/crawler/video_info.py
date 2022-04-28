import re
import json
import requests

headers={
    'cookie': '''_uuid=89749BC4-915F-26EC-7A84-58D10974DE38351277infoc; buvid3=9325CE85-DB9D-42E6-91A6-BCA74ECCB83D167634infoc; b_nut=1639830051; LIVE_BUVID=AUTO9716408611877552; rpdid=|(umJmYJmlYY0J'uYR|)YulJJ; buvid4=F5D509EC-7401-B7B0-464A-E55B636309A189874-022020801-CovTCvxmuQ/mZ1Amd1O0og==; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; CURRENT_QUALITY=64; nostalgia_conf=-1; fingerprint=bd1f88a7f5a689fbd925a4d360d2b431; SESSDATA=5fd4e1d9,1666524290,a398b*41; bili_jct=3f66aac0fae95c86f8d0b683a727171d; DedeUserID=24340948; DedeUserID__ckMd5=7d2620def6c52431; sid=57tk8cr9; buvid_fp=bd1f88a7f5a689fbd925a4d360d2b431; b_ut=5; CURRENT_FNVAL=4048; PVID=1; bp_video_offset_24340948=653998978036138000; b_lsid=91EFE549_1806E4D52CE''',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://space.bilibili.com/27534330',
}

def getVideoInfo(bv_str):
    url='https://www.bilibili.com/video/%s/'%bv_str

    r=requests.get(url,headers=headers)
    
    r.encoding='utf-8'

    html = r.content.decode('utf-8').replace('\xa9', '')

    pattern = re.compile("\"videoData\":(.*?),\"upData\"", re.S)
    if len(pattern.findall(html))==0: return None
    data = pattern.findall(html)[0]
    video_info=json.loads(data)

    return video_info

if __name__=="__main__":
    data=getVideoInfo("BV18r4y1C7xo")


'''
data sample:

{
    "bvid": "BV1aW411P7UJ",
    "aid": 24149246,
    "videos": 1,
    "tid": 47,
    "tname": "短片·手书·配音",
    "copyright": 1,
    "pic": "http:\u002F\u002Fi0.hdslb.com\u002Fbfs\u002Farchive\u002Fed881fa267c6e3248573550d551892c99368d120.jpg",
    "title": "《崩坏3》动画短片「女王降临」",
    "pubdate": 1527739201,
    "ctime": 1527736376,
    "desc": "简介: 《崩坏3》动画短片「女王降临」正式发布！\n掌控空间、统御崩坏兽的女王终于降临了，在她经过的地方，只留下破坏和死亡……\n\n本片由miHoYo Anime出品，片中印象曲《Befall》由HOYO-MiX制作，电子唱作人尚雯婕演唱。\n视频类型: 原创动画\n相关题材: 崩坏3",
    "desc_v2": [
        {
            "raw_text": "简介: 《崩坏3》动画短片「女王降临」正式发布！\n掌控空间、统御崩坏兽的女王终于降临了，在她经过的地方，只留下破坏和死亡……\n\n本片由miHoYo Anime出品，片中印象曲《Befall》由HOYO-MiX制作，电子唱作人尚雯婕演唱。\n视频类型: 原创动画\n相关题材: 崩坏3",
            "type": 1,
            "biz_id": 0
        }
    ],
    "state": 0,
    "duration": 384,
    "rights": {
        "bp": 0,
        "elec": 0,
        "download": 1,
        "movie": 0,
        "pay": 0,
        "hd5": 0,
        "no_reprint": 1,
        "autoplay": 1,
        "ugc_pay": 0,
        "is_cooperation": 0,
        "ugc_pay_preview": 0,
        "no_background": 0,
        "clean_mode": 0,
        "is_stein_gate": 0,
        "is_360": 0,
        "no_share": 0
    },
    "owner": {
        "mid": 27534330,
        "name": "崩坏3第一偶像爱酱",
        "face": "http:\u002F\u002Fi0.hdslb.com\u002Fbfs\u002Fface\u002Ff861b2ff49d2bb996ec5fd05ba7a1eeb320dbf7b.jpg"
    },
    "stat": {
        "aid": 24149246,
        "view": 9615801,
        "danmaku": 74491,
        "reply": 33974,
        "favorite": 239353,
        "coin": 254643,
        "share": 183922,
        "now_rank": 0,
        "his_rank": 1,
        "like": 258575,
        "dislike": 0,
        "evaluation": "",
        "argue_msg": "",
        "viewseo": 9615801
    },
    "dynamic": "#崩坏3#全 新动画短片「女王降临」完整版发布！",
    "cid": 40557424,
    "dimension": {
        "width": 1920,
        "height": 1080,
        "rotate": 0
    },
    "premiere": null,
    "teenage_mode": 0,
    "no_cache": false,
    "pages": [
        {
            "cid": 40557424,
            "page": 1,
            "from": "vupload",
            "part": "0531女王降临60fps_x264",
            "duration": 384,
            "vid": "",
            "weblink": "",
            "dimension": {
                "width": 1920,
                "height": 1080,
                "rotate": 0
            }
        }
    ],
    "subtitle": {
        "allow_submit": false,
        "list": []
    },
    "is_season_display": false,
    "user_garb": {
        "url_image_ani_cut": ""
    },
    "honor_reply": {
        "honor": [
            {
                "aid": 24149246,
                "type": 3,
                "desc": "全站排行榜最高第1名",
                "weekly_recommend_num": 0
            }
        ]
    },
    "embedPlayer": "EmbedPlayer(\"player\", \"\u002F\u002Fs1.hdslb.com\u002Fbfs\u002Fstatic\u002Fplayer\u002Fmain\u002Fflash\u002Fplay.swf\", \"cid=40557424&aid=24149246&attribute=undefined&bvid=BV1aW411P7UJ&show_bv=1&pageVersion=0\")"
}
'''