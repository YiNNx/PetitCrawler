import json
import re
from crawler import proxy
import requests
from config import config
from model import reply,video

cookie=config.load()['cookie']

headers = {
    'cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://www.bilibili.com/video/BV18r4y1C7xo/?spm_id_from=333.788.recommend_more_video.0',
}

url_video_list = "https://api.bilibili.com/x/space/arc/search"
url_reply = "https://api.bilibili.com/x/v2/reply/main"
url_sub_reply = "https://api.bilibili.com/x/v2/reply/reply"


''' Video List Crawler '''

def setVideoParams(mid,ps="50", pn="1"):
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
        params = setVideoParams(mid,"50", str(pn))
        pn+=1
        r=proxy.getResByProxy(url_video_list,headers,params)
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


''' Video Detail Crawler '''

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


''' Reply Crawler '''


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
        r = proxy.getResByProxy(url_reply,headers,params)
        if r==None: 
            next-=1
        data = r.json()
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
        r = requests.get(url_sub_reply, headers=headers, params=params)
        data = r.json()

        if data['data']==None: break
        replies = data['data']['replies']

        for r in replies:
            if int(r['like'])>3000:
                sub_comment_list.append(r)
    return sub_comment_list


''' Save Data '''


def saveVideoInfo(bv_list):
    for bv in bv_list:
        data=getVideoInfo(bv)
        if data==None: continue
        video.addVideo(data)
        

def saveRepliesByList(aid_list):
    r_c=1
    a_c=1
    for aid in aid_list:
        print('================================')
        print(a_c)
        a_c+=1
        if a_c>100: break
        print("aid:"+str(aid))
        root_list,comment_list=getComments(aid)
        for comment in comment_list:
            print("--------------------")
            print("comment_count:"+str(r_c))
            r_c+=1
            countEmoji(comment)
            reply.addReply(comment)
            
        #saveSubReplies(aid,root_list)
        
def saveRepliesByAid(aid):
    print("aid:"+str(aid))
    root_list,comment_list=getComments(aid)
    for comment in comment_list:
        reply.addReply(comment)

def saveSubReplies(aid,root_list):
    for root in root_list:
        sub_comment_list=getSubComments(aid,root)
        reply.addReply(sub_comment_list)

count={}

def countEmoji(comment):
    pattern = re.compile("\[.*?\]", re.S)
    res = pattern.findall(comment['content']['message'])
    for item in res:
        if item in count:
            count[item]+=comment['like']
        else: count[item]=comment['like']

def main():
    conf=config.load()
    aid_list,bv_list=getVideoList(conf['mid'])
    # saveVideoInfo(bv_list)
    
    # 爬单个视频评论
    # aid=input("please input aid:")
    # saveRepliesByAid(aid)
    
    # 爬所有视频评论
    saveRepliesByList(aid_list)
    
    sortedCount = sorted(count.items(), key=lambda d:d[1], reverse=True)
    print(sortedCount)

if __name__=="__main__":
    main()