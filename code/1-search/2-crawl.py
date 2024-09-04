import urllib.request
import urllib.request
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import threading
import csv
from selenium.webdriver.chrome.options import Options
import selenium

def do_something(urllist,be,ed,thread_index):
    #with open('log'+str(thread_index)+'.txt','r') as f:
        #last = f.readlines()[0].strip()
    f1 = open('Middle_results_' + str(int(thread_index)) + '.csv', 'a',encoding='utf-8')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")
    # 添加沙盒模式
    chrome_options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(chrome_options=chrome_options)
    url = 'https://cn.bing.com/search?q=hello&ensearch=1&first=1&FORM=PERE'
    browser.get(url)
    time.sleep(20)
    for num in range(be,ed):
        str1=''
        key = urllib.parse.quote(urllist[num])
        url = 'https://cn.bing.com/search?q=' + key + '&ensearch=1&first=1&FORM=PERE'
        try:
            browser.get(url)
        except selenium.common.exceptions.TimeoutException as e:
            print(e)
            continue
        time.sleep(1)
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        browser.execute_script(js)
        source_code = browser.page_source
        time.sleep(3)
        soup = bs(source_code, "html.parser")
        count = soup.findAll(class_="sb_count")
        resultnum=0
        for c in count:
            try:
                resultnum=int(c.get_text().split(' ')[1].replace(',',''))
                print(resultnum)
            except ValueError as e:
                print(e)
                continue

        if(resultnum!=0 ):
            page=int(int(resultnum)/30)+1
            if(page>100):
                page=100
            for i in range(0,page):
                url = 'https://cn.bing.com/search?q=' + key + '&ensearch=1&first='+str(i*30+1)+'&FORM=PERE'
                try:
                    browser.get(url)
                except selenium.common.exceptions.TimeoutException as e:
                    print(e)
                    continue

                time.sleep(1)
                js = 'window.scrollTo(0, document.body.scrollHeight);'
                browser.execute_script(js)
                time.sleep(3)
                browser.execute_script(js)
                time.sleep(1)
                source_code = browser.page_source
                if('There are no results for' in source_code.replace('\n','')):
                    print('当前URL检索完成')
                    break
                soup = bs(source_code, "html.parser")
                td = soup.findAll("h2")
                str1+=urllist[num]+','+str(i*30+1)+','+str(resultnum)+','
                str1pre=str1
                str2=''
                for t in td:
                    str1 += '<title>' + t.get_text() + '<URL>'
                    str2 += '<title>' + t.get_text() + '<URL>'

                    pattern = re.compile(r'href="([^"]*)"')
                    h = re.search(pattern, str(t))
                    if h:
                        for x in h.groups():
                            str1 += x + ','
                            str2 += x + ','

                    str1 += '</URL></title>,'
                    str2 += '</URL></title>,'
                str1 += '\n'
                if (str2 in str1pre):
                    print('当前URL检索完成')
                    break

        else:
            continue


        f1.writelines(str1)
        f1.flush()



if __name__ == '__main__':

    #conduct multi-thread for crawling candidate URLs



    ##input all query terms
    dicturl0 = set()
    file = open('URLrecord.csv', 'r',encoding='utf-8')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        query=row[0]
        dicturl0.add(query)

    dicturl = list(dicturl0)

    file = open('inputseed.csv', 'r', encoding='utf-8')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        if (row[0] not in dicturl):
            dicturl.append(row[0])

    ##multi-thread
    print(len(dicturl))
    d = 10
    num = int(len(dicturl) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(dicturl, num * i, num * (i + 1), i))
            t.start()
            time.sleep(20)
        else:
            t = threading.Thread(target=do_something,
                                 args=(dicturl, num * i, len(dicturl) , i))
            t.start()
