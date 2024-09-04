import re
import json
import os
            
rule = '[^0-9:][0-9]{3,6}:[0-9a-zA-Z]{1,6}[^0-9a-zA-Z:]'

with open('./urls.json','r',encoding='utf-8') as f:
    urls = json.load(f)

res = []
for i in range(10):
    print(i)
    for fn in os.listdir('./'+str(i)+'/'):
        j = False
        with open('./'+str(i)+'/'+fn,'r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if len(line) < 50 and re.search(rule,line) != None:
                    j = True
                    break
        if j:
            res.append(fn[:-4]+'\t'+urls[int(fn[:-4])])

print(len(res))

with open('filter_results.txt','w',encoding='utf-8') as f:
    for line in res:
        f.write(line+'\n')





