import csv
import json
stoplist = [
    'https://whois.ipip.net',
    'https://bgp.he.net',
    'https://ipinfo.io',
    'https://www.bigdatacloud.com',
    'https://radar.qrator.net',
    'https://bgpview.io',
    'https://bgptools.eu-gb.mybluemix.net',
    'https://bgp.tools/as/',
    'http://bgp.tools/as/',
    'http://ipv4info.com',
    'https://www.linkedin.com',
    'https://www.ipqualityscore.com',
    'https://dnslytics.com',
    'https://ipgeolocation.io',
    'https://www.peeringdb.com',
    'https://asrank.caida.org',
    'https://www.datacentermap.com',
    'https://bgpv6.com',
    'https://ip.teoh.io',
    'linkedin.com',
    'https://ips.osnova.news',
    'https://zh-hant.ipshu.com',
    'https://flightaware.com',
    'https://www.dbu.edu/login/',
    'https://whatismyip.live',
    'https://www.juniper.net/',
    'https://developer.arubanetworks.com/',
    'https://stage.juniper.net',
    'ripe.net/',
    'afrinic.net/',
    'apnic.net/',
    'arin.net/',
    'lacnic.net/',
    'https://www.potaroo.net/',
    'https://bgp.potaroo.net/',
    'https://www.researchgate.net',
    'https://urlhaus.abuse.ch/',
    'http://www.fmb.la',
    'https://www.radb.net',
    'https://doczz.net/',
    'https://www.cisco.com',
    'https://www.mywot.com',
    'https://2ip.ru'
    ]

def vali(url):
    for s in stoplist:
        if url.find(s) > -1:
            return False
    return True

urls = []
url_labels = []
print('loading data...')
with open('../1-search/inputseed.csv','r',encoding='utf-8') as f:
    csv_reader1 = csv.reader(f)
    for row in csv_reader1:
        urls.append(row[0])
        url_labels.append(1)

temp = set()
with open('../1-search/search_results.json','r',encoding='utf-8') as f:
    dic = json.load(f)

for url in dic:
    if vali(url):
        temp.add(url)

pre = list(urls)
for url in temp:
    if url not in pre:
        urls.append(url)
        url_labels.append(0)
print('loading URL finished')

with open('urls.json','w') as f:
    json.dump(urls,f)

with open('url_labels.json','w') as f:
    json.dump(url_labels,f)
print(len(urls))


titles = []
title_labels = []

print('loading title data...')
with open('inputseed_title.txt','r',encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        title = '\t'.join(parts[1:])
        titles.append(title)
        title_labels.append(1)
temp2 = set()


for url in dic:
    if vali(url):
        temp2.add(dic[url])

pre = list(titles)
for title in temp2:
    if title not in pre:
        titles.append(title)
        title_labels.append(0)
print('loading title finished')

with open('titles.json','w') as f:
    json.dump(titles,f)

with open('title_labels.json','w') as f:
    json.dump(title_labels,f)
print(len(titles))


url2title = {}
title2url = {}
print('loading data...')
with open('inputseed_title.txt','r',encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        url = parts[0]
        title = '\t'.join(parts[1:])
        url2title[url] = title
        if title not in title2url:
            title2url[title] = []
        title2url[title].append(url)

temp = set()
with open('../1-search/search_results.json','r',encoding='utf-8') as f:
    dic = json.load(f)

for url in dic:
    if vali(url):
        title = dic[url]
        url2title[url] = title
        if title not in title2url:
            title2url[title] = []
        if url not in title2url[title]:
            title2url[title].append(url)

with open('url2title.json','w') as f:
    json.dump(url2title,f)

with open('title2url.json','w') as f:
    json.dump(title2url,f)









