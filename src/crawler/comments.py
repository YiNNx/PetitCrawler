import requests
import video_list

url = "https://api.bilibili.com/x/v2/reply/main"

headers = {
    'cookie': '''_uuid=89749BC4-915F-26EC-7A84-58D10974DE38351277infoc; buvid3=9325CE85-DB9D-42E6-91A6-BCA74ECCB83D167634infoc; b_nut=1639830051; LIVE_BUVID=AUTO9716408611877552; rpdid=|(umJmYJmlYY0J'uYR|)YulJJ; buvid4=F5D509EC-7401-B7B0-464A-E55B636309A189874-022020801-CovTCvxmuQ/mZ1Amd1O0og==; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; CURRENT_QUALITY=64; nostalgia_conf=-1; fingerprint=3591514e8945926c758532a45fe3d2e8; sid=4ivymv2u; bp_video_offset_24340948=653249128266989600; bsource=search_google; b_ut=7; b_lsid=784102EB3_18064D75527; buvid_fp=bd1f88a7f5a689fbd925a4d360d2b431; innersign=1; CURRENT_FNVAL=4048; PVID=1''',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://space.bilibili.com/27534330',
}

def setParams(oid,next="1"):
    params = {
        "oid": oid,  # 视频aid
        "next": next,  # 评论分页 从1开始
        "mode": "3",  # 3:按热度排序 2：按时间排序
        "type": "1",  # 就这一个type能用好像
    }
    return params

def getCommentsList():
    vlist=video_list.getVideoList()
    for aid in vlist:
        params = setParams(aid)
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        replies = data['data']['replies']
        for r in replies:
            print(r["content"]["message"])

if __name__ == "__main__":
    getCommentsList()
