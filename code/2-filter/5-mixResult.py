import csv
import json

urlp = {}

with open('./url_result.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url, p = line.strip().split('\t')
        urlp[url] = float(p)

titlep = {}

with open('./titleresult.txt', 'r', encoding='utf-8') as f:
    for line in f:
        title, p = line.strip().split('\t')
        titlep[title] = float(p)

mix = {}

for url in urlp:
    if url in titlep:
        mp = (urlp[url] + titlep[url]) / 2
    else:
        mp = urlp[url]
    mix[url] = mp

tups = sorted(mix.items(), key=lambda x: x[1], reverse=True)
with open('mix_result.txt', 'w', encoding='utf-8') as f:
    for tup in tups:
        f.write(tup[0] + '\t' + str(tup[1]) + '\n')







