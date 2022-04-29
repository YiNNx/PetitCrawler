from crawler import replies,video_info,video_list
from model import reply,video
from config import config

def saveVideoInfo(bv_list):
    for bv in bv_list:
        data=video_info.getVideoInfo(bv)
        if data==None: continue
        video.addVideo(data)
        
def saveRepliesByList(aid_list):
    for aid in aid_list:
        print('------------------------')
        print("aid:"+str(aid))
        root_list,comment_list=replies.getComments(aid)
        reply.addReply(comment_list)
        #saveSubReplies(aid,root_list)
        
def saveRepliesByAid(aid):
    print("aid:"+str(aid))
    root_list,comment_list=replies.getComments(aid)
    reply.addReply(comment_list)

def saveSubReplies(aid,root_list):
    for root in root_list:
        sub_comment_list=replies.getSubComments(aid,root)
        reply.addReply(sub_comment_list)

def crawler():
    conf=config.load()
    aid_list,bv_list=video_list.getVideoList(conf['mid'])
    saveVideoInfo(bv_list)
    
    # 爬单个视频评论
    aid=input("please input aid:")
    saveRepliesByAid(aid)
    
    # 爬所有视频评论
    # saveRepliesByList(aid_list)

if __name__=="__main__":
    crawler()
