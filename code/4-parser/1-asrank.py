
asns = []
with open('20240301.ppdc-ases.txt','r',encoding='utf-8') as f:
    lines = f.read().splitlines()
    for line in lines[2:]:
        tmp_asn = line.split(" ")
        for asn in tmp_asn:
            if asn not in asns:
                asns.append(asn)

with open('asns.txt','w',encoding='utf-8') as f:
    for asn in asns:
        f.write(asn+'\n')

with open('asns.sh','w',encoding='utf-8') as f:
    for asn in asns:
        f.write('whois -h whois.radb.net AS'+asn+' >> IRR_Data/'+asn+'.txt\n')


asnlist = []

with open('20240301.ppdc-ases.txt','r') as f:
    for line in f:
        line = line.strip()
        if line.find('#') > -1:
            continue
        parts = line.split(' ')
        asnlist.append(parts[0])

with open('asnlist.txt','w') as f:
    for i in range(0,30000):
        f.write(asnlist[i]+'\n')

