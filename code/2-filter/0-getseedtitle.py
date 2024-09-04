import urllib.request
import re
import json

lines = []

with open('../1-search/inputseed.csv','r') as f:
    for line in f:
        line = line.strip()
        newl = line
        try:
            page = urllib.request.urlopen(line)
            html = page.read().decode('utf-8')
            title=re.findall('<title>(.+)</title>',html)[0]
            newl+='\t'+title
        except:
            pass
        lines.append(newl+'\n')

with open('inputseed_title.txt','w',encoding='utf-8') as f:
    for line in lines:
        f.write(line)




