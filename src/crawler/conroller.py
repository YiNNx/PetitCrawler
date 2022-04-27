
from src.crawler.replies import getComments, getSubComments
from src.crawler.video_info import  getVideoInfo
from src.crawler.video_list import getVideoList

mid="27534330"

def crawler():
    aid_list,bv_list=getVideoList(mid)
    for bv in bv_list:
        getVideoInfo(bv)
    for aid in aid_list:
        root_list,comment_list=getComments(aid)
        
        for root in root_list:
            sub_comment_list=getSubComments(aid,root)

