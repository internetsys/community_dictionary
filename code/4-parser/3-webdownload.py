import requests
import threading
import os

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
def do_something(urllist,be,ed,thread_index):
    #f1 = open('urlcontent_results' + str(int(thread_index)) + '.csv', 'a')
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
                with open('webparser/' + str(num)+'.txt','w',encoding='utf-8') as f:
                    f.writelines(content)
            else:
                #print(content.replace('\n',' ').replace('\t',' '))
                #f1.writelines(url + ',|wutianhao|' + url + ',|wutianhao|' +content.replace('\n', ' ').replace('\t',' ') + '\n')
                #f1.flush()
                with open('webparser/'+ str(num)+'.txt','w',encoding='utf-8') as f:
                    f.writelines(content)

        except Exception as e:
            print(url)
            print(e)
            continue

if __name__ == '__main__':
    if not os.path.exists('webparser/'):
        os.mkdir('webparser/')
    urls = set()
    with open('../1-search/inputseed.csv','r',encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            urls.add(url)
    with open('../3-download/filter_results.txt','r',encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            urls.add(url)
    print(len(urls))
    urls = list(urls)
    d = 1
    num = int(len(urls) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(urls, num * i, num * (i + 1), i))
            t.start()
        else:
            t = threading.Thread(target=do_something,
                                  args=(urls, num * i, len(urls) , i))
            t.start()
            






