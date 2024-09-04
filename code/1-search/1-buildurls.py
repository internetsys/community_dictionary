from collections import defaultdict

lines = set()

with open('orgnamenew.csv','r',encoding='utf-8',errors='ignore') as f:
    for line in f:
        parts = line.strip().split(',')
        lines.add('bgp communities AS'+parts[0]+'|'+parts[1]+'\n')

asns = []
with open('20240301.ppdc-ases.txt','r',encoding='utf-8') as f:
    lines = f.read().splitlines()
    for line in lines[2:]:
        tmp_asn = line.split(" ")
        for asn in tmp_asn:
            if asn not in asns:
                asns.append(asn)

for asn in asns:
    lines.add('bgp communities AS' + asn + '\n')

with open('lgrecord.csv','r',encoding='utf-8',errors='ignore') as f:
    for line in f:
        line = line.replace('looking glass','bgp communities')
        lines.add(line)


with open('URLrecord.csv','w',encoding='utf-8') as f:
    for line in lines:
        f.write(line)
