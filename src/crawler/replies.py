from crawler import proxy
import requests
from config import config

url = "https://api.bilibili.com/x/v2/reply/main"
url_sub = "https://api.bilibili.com/x/v2/reply/reply"

cookie='''_uuid=89749BC4-915F-26EC-7A84-58D10974DE38351277infoc; buvid3=9325CE85-DB9D-42E6-91A6-BCA74ECCB83D167634infoc; b_nut=1639830051; LIVE_BUVID=AUTO9716408611877552; rpdid=|(umJmYJmlYY0J'uYR|)YulJJ; buvid4=F5D509EC-7401-B7B0-464A-E55B636309A189874-022020801-CovTCvxmuQ/mZ1Amd1O0og==; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; CURRENT_QUALITY=64; nostalgia_conf=-1; fingerprint=bd1f88a7f5a689fbd925a4d360d2b431; SESSDATA=5fd4e1d9,1666524290,a398b*41; bili_jct=3f66aac0fae95c86f8d0b683a727171d; DedeUserID=24340948; DedeUserID__ckMd5=7d2620def6c52431; sid=57tk8cr9; buvid_fp=bd1f88a7f5a689fbd925a4d360d2b431; b_ut=5; CURRENT_FNVAL=4048; PVID=1; bp_video_offset_24340948=653998978036138000; bsource=search_baidu; b_lsid=F5D3102510_1806EA03E85'''

headers = {
    'cookie': '''_uuid=89749BC4-915F-26EC-7A84-58D10974DE38351277infoc; buvid3=9325CE85-DB9D-42E6-91A6-BCA74ECCB83D167634infoc; b_nut=1639830051; LIVE_BUVID=AUTO9716408611877552; rpdid=|(umJmYJmlYY0J'uYR|)YulJJ; buvid4=F5D509EC-7401-B7B0-464A-E55B636309A189874-022020801-CovTCvxmuQ/mZ1Amd1O0og==; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; CURRENT_QUALITY=64; nostalgia_conf=-1; fingerprint=bd1f88a7f5a689fbd925a4d360d2b431; SESSDATA=5fd4e1d9,1666524290,a398b*41; bili_jct=3f66aac0fae95c86f8d0b683a727171d; DedeUserID=24340948; DedeUserID__ckMd5=7d2620def6c52431; sid=57tk8cr9; buvid_fp=bd1f88a7f5a689fbd925a4d360d2b431; b_ut=5; CURRENT_FNVAL=4048; PVID=1; bp_video_offset_24340948=653998978036138000; bsource=search_baidu; b_lsid=F5D3102510_1806EA03E85''',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://www.bilibili.com/video/BV18r4y1C7xo/?spm_id_from=333.788.recommend_more_video.0',
}

def setCommentsParams(aid,next="1"):
    params = {
        "oid": aid,  # 视频aid
        "next": next,  # 评论分页 从1开始
        "mode": "3",  # 3:按热度排序 2：按时间排序
        "type": "1",  
    }
    return params

def getComments(aid):
    next=1
    root_list=[]
    comment_list=[]
    conf=config.load()
    likes_min=conf['likes_min']
    likes_stop=conf['likes_stop_look_through']
    while True:
        params = setCommentsParams(aid,str(next))
        r = proxy.getResByProxy(url,headers,params)
        data = r.json()
        if data['data']==None: 
            print(data)
            break
        replies = data['data']['replies']
        if int(replies[0]['like'])<likes_stop:
            break
        
        for r in replies:
            if int(r['like'])>likes_min:
                root_list.append(r["rpid"])
                comment_list.append(r)
        next+=1
    return root_list,comment_list

def setSubCommentsParams(aid,root="0",pn="1"):
    params = {
        "oid": aid,  # 视频aid
        "pn": pn,  # 评论分页 从1开始
        "root": root, # 根评论id
        "mode": "3",  # 3:按热度排序 2：按时间排序
        "type": "1",  
    }
    return params

def getSubComments(aid,root):
    sub_comment_list=[]
    for pn in range(1,3): 
        params = setSubCommentsParams(aid,str(root),str(pn))
        r = requests.get(url_sub, headers=headers, params=params)
        data = r.json()

        if data['data']==None: break
        replies = data['data']['replies']

        for r in replies:
            if int(r['like'])>3000:
                sub_comment_list.append(r)
    return sub_comment_list

if __name__ == "__main__":
    root_list,comment_list=getComments("24149246")
    #print(comment_list[0]['member'])


'''
"replies": [
            {
                "rpid": 838382445,
                "oid": 24149246, #视频bid
                "mid": 49128862, #回复者id
                "root": 0,
                "dialog": 0,
                "rcount": 184, #回复数
                "ctime": 1528995737,
                "like": 41652
                "member": {
                    "uname": "启世天华",
                },
                "content": {
                    "message": "只有看了短片，你才会蓦然醒悟——TM的泰坦和崩坏兽不是一伙的啊！\n你们为什么打我的时候这么齐心协力。",
                },
                ...
            ]
'''



'''
data sample:
{
    "cursor": {
            "all_count": 23365,
            "is_begin": false,
            "prev": 1,
            "next": 2,
            "is_end": false,
            "mode": 3,
            "show_type": 1,
            "support_mode": [
                1,
                2,
                3
            ],
            "name": "热门评论"
        },
        "hots": null,
        "notice": null,
        "replies": [
            {
                "rpid": 109637220000,
                "oid": 768280609,
                "type": 1,
                "mid": 12727318,
                "root": 0,
                "parent": 0,
                "dialog": 0,
                "count": 566,
                "rcount": 307,
                "state": 0,
                "fansgrade": 0,
                "attr": 0,
                "ctime": 1650202629,
                "rpid_str": "109637220000",
                "root_str": "0",
                "parent_str": "0",
                "like": 84750,
                "action": 0,
                "member": {
                    "mid": "12727318",
                    "uname": "奇思妙想王有才",
                    "sex": "男",
                    "sign": "",
                    "avatar": "http://i1.hdslb.com/bfs/face/ce9808ff6bfe254056c80f45ff93a51e3c59db9d.jpg",
                    "rank": "10000",
                    "DisplayRank": "0",
                    "face_nft_new": 0,
                    "is_senior_member": 0,
                    "level_info": {
                        "current_level": 6,
                        "current_min": 0,
                        "current_exp": 0,
                        "next_exp": 0
                    },
                    "pendant": {
                        "pid": 0,
                        "name": "",
                        "image": "",
                        "expire": 0,
                        "image_enhance": "",
                        "image_enhance_frame": ""
                    },
                    "nameplate": {
                        "nid": 0,
                        "name": "",
                        "image": "",
                        "image_small": "",
                        "level": "",
                        "condition": ""
                    },
                    "official_verify": {
                        "type": -1,
                        "desc": ""
                    },
                    "vip": {
                        "vipType": 2,
                        "vipDueDate": 1652112000000,
                        "dueRemark": "",
                        "accessStatus": 0,
                        "vipStatus": 1,
                        "vipStatusWarn": "",
                        "themeType": 0,
                        "label": {
                            "path": "",
                            "text": "年度大会员",
                            "label_theme": "annual_vip",
                            "text_color": "#FFFFFF",
                            "bg_style": 1,
                            "bg_color": "#FB7299",
                            "border_color": ""
                        },
                        "avatar_subscript": 1,
                        "avatar_subscript_url": "http://i0.hdslb.com/bfs/vip/icon_Certification_big_member_22_3x.png",
                        "nickname_color": "#FB7299"
                    },
                    "fans_detail": null,
                    "following": 0,
                    "is_followed": 0,
                    "user_sailing": {
                        "pendant": null,
                        "cardbg": null,
                        "cardbg_with_focus": null
                    },
                    "is_contractor": false,
                    "contract_desc": ""
                },
                "content": {
                    "message": "不要睡在打印机旁边，不论是光固化还是fdm，都是有毒的！！通风！！通风！！！",
                    "plat": 0,
                    "device": "",
                    "members": [],
                    "jump_url": {},
                    "max_line": 6
                },
                "replies": [
                    {
                        "rpid": 109639021472,
                        "oid": 768280609,
                        "type": 1,
                        "mid": 338348625,
                        "root": 109637220000,
                        "parent": 109637220000,
                        "dialog": 109639021472,
                        "count": 0,
                        "rcount": 0,
                        "state": 0,
                        "fansgrade": 0,
                        "attr": 0,
                        "ctime": 1650203445,
                        "rpid_str": "109639021472",
                        "root_str": "109637220000",
                        "parent_str": "109637220000",
                        "like": 2925,
                        "action": 0,
                        "member": {
                            "mid": "338348625",
                            "uname": "莫揽海中月",
                            "sex": "保密",
                            "sign": "守望麦园，追风成愿",
                            "avatar": "http://i0.hdslb.com/bfs/face/211663850ce88fb5c2eee24a893d06d29266700e.jpg",
                            "rank": "10000",
                            "DisplayRank": "0",
                            "face_nft_new": 0,
                            "is_senior_member": 0,
                            "level_info": {
                                "current_level": 5,
                                "current_min": 0,
                                "current_exp": 0,
                                "next_exp": 0
                            },
                            "pendant": {
                                "pid": 0,
                                "name": "",
                                "image": "",
                                "expire": 0,
                                "image_enhance": "",
                                "image_enhance_frame": ""
                            },
                            "nameplate": {
                                "nid": 0,
                                "name": "",
                                "image": "",
                                "image_small": "",
                                "level": "",
                                "condition": ""
                            },
                            "official_verify": {
                                "type": -1,
                                "desc": ""
                            },
                            "vip": {
                                "vipType": 1,
                                "vipDueDate": 1646841600000,
                                "dueRemark": "",
                                "accessStatus": 0,
                                "vipStatus": 0,
                                "vipStatusWarn": "",
                                "themeType": 0,
                                "label": {
                                    "path": "",
                                    "text": "",
                                    "label_theme": "",
                                    "text_color": "",
                                    "bg_style": 0,
                                    "bg_color": "",
                                    "border_color": ""
                                },
                                "avatar_subscript": 0,
                                "nickname_color": ""
                            },
                            "fans_detail": null,
                            "following": 0,
                            "is_followed": 0,
                            "user_sailing": {
                                "pendant": null,
                                "cardbg": null,
                                "cardbg_with_focus": null
                            },
                            "is_contractor": false,
                            "contract_desc": ""
                        },
                        "content": {
                            "message": "这是真的，我之前在打印机旁边呆了一会，眼睛就开始不舒服了，所以一定要做好通风，尽量不要带着打印机旁边[笑哭]",
                            "plat": 0,
                            "device": "",
                            "members": [],
                            "emote": {
                                "[笑哭]": {
                                    "id": 509,
                                    "package_id": 1,
                                    "state": 0,
                                    "type": 1,
                                    "attr": 0,
                                    "text": "[笑哭]",
                                    "url": "http://i0.hdslb.com/bfs/emote/c3043ba94babf824dea03ce500d0e73763bf4f40.png",
                                    "meta": {
                                        "size": 1
                                    },
                                    "mtime": 1645206695,
                                    "jump_title": "笑哭"
                                }
                            },
                            "jump_url": {},
                            "max_line": 999
                        },
                        "replies": null,
                        "assist": 0,
                        "folder": {
                            "has_folded": false,
                            "is_folded": false,
                            "rule": ""
                        },
                        "up_action": {
                            "like": false,
                            "reply": false
                        },
                        "show_follow": false,
                        "invisible": false,
                        "reply_control": {
                            "time_desc": "9天前发布"
                        }
                    },
                    ...
    }
'''