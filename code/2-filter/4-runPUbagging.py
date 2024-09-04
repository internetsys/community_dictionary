import json

seedpages = []
with open('../1-search/inputseed.csv','r') as f:
    for line in f:
        line = line.strip()
        seedpages.append(line)


url_dic = {}
with open('URL_probalineSVC10-100-1.csv','r',encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        url,p = parts[0],parts[2]
        url_dic[url] = float(p)

url_tups = sorted(url_dic.items(),key = lambda x:x[1],reverse = True)

with open('url_result.txt','w',encoding='utf-8') as f:
    for tup in url_tups:
        if tup[0] in seedpages:
            continue
        else:
            f.write(tup[0]+'\t'+str(tup[1])+'\n')

seedpage_titles = []
with open('inputseed_title.txt','r') as f:
    for line in f:
        parts = line.strip().split('\t')
        seedpage_titles.append('\t'.join(parts[1:]))
title_dic = {}
with open('Title_probalineSVC10-100-1.csv','r',encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        title = '\t'.join(parts[:-2])
        p = parts[-1]
        title_dic[title] = float(p)

title_tups = sorted(title_dic.items(),key = lambda x:x[1],reverse = True)

with open('test_title.txt','w',encoding='utf-8') as f:
    for tup in title_tups:
        if tup[0] in seedpage_titles:
            continue
        else:
            f.write(tup[0]+'\t'+str(tup[1])+'\n')

with open('title2url.json','r',encoding='utf-8') as f:
    title2url = json.load(f)

with open('title_result.txt','w',encoding='utf-8') as f:
    for tup in title_tups:
        title = tup[0]
        if tup[0] in seedpage_titles:
            continue
        for url in title2url[title]:
            f.write(url+'\t'+str(tup[1])+'\n')