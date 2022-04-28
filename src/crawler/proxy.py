import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5001/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5001/delete/?proxy={}".format(proxy))

def getResByProxy(url,headers,params):
    retry_count = 5
    pro = get_proxy().get("proxy")
    print("proxy:"+pro)
    while retry_count > 0:
        try:
            r = requests.get(url, headers=headers, params=params,proxies={"http": "http://{}".format(pro)})
            return r
        except Exception:
            print('oops')
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(pro)
    return None