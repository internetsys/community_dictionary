from bs4 import BeautifulSoup as bs
import urllib.request
import urllib.request
import requests
import re
import math
import time
import json
import os
import threading
import csv
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
def do_something(urllist,be,ed,thread_index):
    if not os.path.exists(str(thread_index)+'/'):
        os.mkdir(str(thread_index)+'/')
    for num in range(be,ed):
        url = urllist[num]
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             headers=headers,
                             allow_redirects=False,
                             verify=False,
                             timeout=60)
            r.raise_for_status()
            # 设置该html文档可能的编码
            r.encoding = r.apparent_encoding
            content = r.text
            # soup = bs(content, 'html.parser')

            if('301 Moved Permanently'.lower() in content.lower() or 'Object moved'.lower() in  content.lower()):
                print(url)
                url1='https://'+url.split('://')[1]
                r = requests.get(url=url1,
                                 headers=headers,
                                 allow_redirects=False,
                                 verify=False,
                                 timeout=60)
                r.raise_for_status()
                # 设置该html文档可能的编码
                r.encoding = r.apparent_encoding
                content = r.text
                #print(content.replace('\n',' ').replace('\t',' '))
                #f1.writelines(url + ',|wutianhao|' +url1 + ',|wutianhao|' +content.replace('\n',' ').replace('\t',' ') + '\n')
                #f1.flush()
                with open(str(thread_index)+'/'+str(num)+'.txt','w',encoding='utf-8') as f:
                    f.writelines(content)
            else:
                #print(content.replace('\n',' ').replace('\t',' '))
                #f1.writelines(url + ',|wutianhao|' + url + ',|wutianhao|' +content.replace('\n', ' ').replace('\t',' ') + '\n')
                #f1.flush()
                with open(str(thread_index)+'/'+str(num)+'.txt','w',encoding='utf-8') as f:
                    f.writelines(content)

        except Exception as e:
            print(url)
            print(e)
            continue

if __name__ == '__main__':
    urls = []
    with open('../2-filter/mix/mix.txt','r',encoding='utf-8') as f:
        i = 0
        for line in f:
            i+=1
            if i > 50000:
                break
            url = line.strip().split('\t')[0]
            urls.append(url)
    with open('urls.json','w',encoding='utf-8') as f:
        json.dump(urls,f)
    print(len(urls))
    d = 10
    num = int(len(urls) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(urls, num * i, num * (i + 1), i))
            t.start()
        else:
            t = threading.Thread(target=do_something,
                                  args=(urls, num * i, len(urls) , i))
            t.start()
            






