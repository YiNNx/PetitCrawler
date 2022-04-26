'''
warm-up

先写个简单的尝试一下！
将 https://ksmeow.moe/ 任意年份blog爬到本地并存为markdown (好恶趣味啊我

'''

import re
import os
import requests
import html2text
# from bs4 import BeautifulSoup

headers={
    'cookie': '_ga=GA1.2.878310733.1642922575',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'referer': 'https://ksmeow.moe/',
}


def saveMd(html,filepath,title):
    with open(filepath+"%s.md"%title,"w",encoding="utf-8") as file:
        markdown =html2text.html2text(html).replace('-\n', '-')
        file.write(markdown)


def getHtml(title):
    url='https://ksmeow.moe/%s/'%title

    r=requests.get(url,headers=headers)
    r.encoding='utf-8'

    html = r.content.decode('utf-8').replace('\xa9', '')

    pattern = re.compile("<div class=\"entry-header\">(.*?)</div></div></div></div>", re.S)
    html = pattern.findall(html)[0]

    return html


def getTitles(year,month):
    r=requests.get("https://ksmeow.moe/%s/%s/"%(year,month),headers=headers)
    r.encoding='utf-8'
    html = r.content.decode('utf-8').replace('\xa9', ' ')

    pattern=re.compile(r'<div class="entry-thumb"> <a href="https://ksmeow.moe/(.*?)/">')
    titles = pattern.findall(html)
    
    return titles


def newFilePath(year):
    path=os.getcwd()
    newPath=path+"\\sample\\"+year+"\\"

    if not os.path.exists(newPath):               
        os.makedirs(newPath)          
    return newPath


def blogCrawler(year):
        path=newFilePath(str(year))
        for month in range(1,13):
            if month<10: m="0"+str(month)
            else: m=str(month)
            print("month: %s"%m)

            titles=getTitles(str(year),m)

            for title in titles:
                
                print(title)
                res=getHtml(title)

                saveMd(res,path,title)


if __name__=='__main__':
    year=input("please input the year:")
    blogCrawler(year)


'''
def test_soup():
    r=requests.get("https://ksmeow.moe/mit-6-837-dynamics-kinematics-rotation-interpolation/",headers=headers)
    
    content = r.content

    r.encoding='utf-8'
    # 转换成字符串类型
    html = content.decode('utf-8').replace('\xa9', ' ')

    with open("ksblog-mit-6-837.html","w",encoding="utf-8") as file:
         file.write(html)

    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    #2.获取内容
    #获取标题对象
    print(soup.title)
    #获取文本内容
    article=soup.select('.single-content')[0].text

    with open("article.md","w",encoding="utf-8") as file:
     file.write(article)
'''