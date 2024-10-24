# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 14:21:08 2022

@author: Lenovo
"""
import os
import re
import spacy
import json
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


nlp1 = spacy.load('en_core_web_sm')
nlp2 = spacy.load('en_core_web_lg')

dic = {}
top3w = []
with open('asnlist.txt','r') as f:
    for line in f:
        line = line.strip()
        top3w.append(line)
stoplist = [
    'aut-num',
    'as-name',
    'descr',
    'import',
    'export',
    'mp-import',
    'mp-export',
    'org',
    'admin-c',
    'tech-c',
    'status',
    'mnt-by',
    'created',
    'last-modified',
    'source',
    'notify',
    'member-of',
    'changed',
    'abuse-c'
    ]
policylist = [
    'import',
    'export',
    'mp-import',
    'mp-export'
    ]
communityrule = re.compile('[0-9]{1,6}:[0-9a-z]{1,6}', re.IGNORECASE)
timerule = re.compile('[0-2]?[0-9]:[0-2]?[0-9]', re.IGNORECASE)
ipv6rule = re.compile('[0-9a-f]{0,4}:[0-9a-f]{0,4}:[0-9a-f]{0,4}:[0-9a-f]{0,4}', re.IGNORECASE)
stopwords = [
    'or',
    'rs',
    'as'
    ]
lprule = re.compile('local[\s-]?pref(erence)?', re.IGNORECASE)
lprule2 = re.compile('LP=', re.IGNORECASE)
lpwords = ['lpref']
bhrule = re.compile('black([\s-])?hol(e(s|d)?|ing)', re.IGNORECASE)
bhwords = ['rtbh','remote trigger black']
pprule = re.compile('pre(\s|-)?pen', re.IGNORECASE)
pptime1= re.compile('\d(\*|x)', re.IGNORECASE)
pptime2= re.compile('(\*|x)\d', re.IGNORECASE)
ppnumdic = {}
ppnumdic['once'] = 1
ppnumdic['one'] = 1
ppnumdic['twice'] = 2
ppnumdic['two'] = 2
ppnumdic['thrice'] = 3
ppnumdic['three'] = 3
ppnumdic['four'] = 4
ppnumdic['five'] = 5
ppnumdic['six'] = 6
ppnumdic['seven'] = 7
ppnumdic['eight'] = 8
ppnumdic['nine'] = 9
ppnumdic['ten'] = 10
sarule = re.compile('(anno(u)?nc(e|ement)?|export|advertis(e)?|send)(s|d|ing)?(\s|-)(the(\s|-))?(route(\s|-))?(to(ward)?|outside|at)', re.IGNORECASE)
originrule = re.compile('originated in', re.IGNORECASE)
inforule = re.compile('(learned|received|originated|imported)\s(via|from|at|in|@)', re.IGNORECASE)
sawords= ['announc','advertis','export','no-out']
locwords = ['location']
ixpwords = ['exchange']
nooutwords = ['filter','suppression']
rels = ['transit','provider','peer','customer']
relworddic = {}
relworddic['upstream'] = 'provider'
relworddic['uplink'] = 'provider'
relworddic['transit'] = 'provider'
relworddic['provider'] = 'provider'
relworddic['peer'] = 'peer'
relworddic['customer'] = 'customer'
relworddic['downstream'] = 'customer'
stopwords = ['bogus','aggregat','rpki']
asnrule = re.compile('AS[1-9][0-9]{1,4}', re.IGNORECASE)
numrule = re.compile('[^\d][0-9]{1,3}[^\d]', re.IGNORECASE)
'''
#textCNN configuration
class TrainingConfig(object):
    epoches = 50
    evaluateEvery = 10
    checkpointEvery = 10
    learningRate = 0.001
    
class ModelConfig(object):
    embeddingSize = 100
    numFilters = 128

    filterSizes = [2, 3, 4, 5]
    dropoutKeepProb = 0.5
    l2RegLambda = 0.0

class Config(object):
    sequenceLength = 10  # 取了所有序列长度的均值
    batchSize = 128
    
    dataSource = "../small.txt"
    
    stopWordSource = "../english.txt"
    
    numClasses = 7  # 二分类设置为1，多分类设置为类别的数目
    
    rate = 0.9  # 训练集的比例
    
    training = TrainingConfig()
    
    model = ModelConfig()

    
# 实例化配置参数对象
config = Config()
'''




def localpref(inputlist):
    items = []
    for item in inputlist:
        if item != '':
            items.append(item.lower())
    sentence = ' '.join(items)
    #Set local preference 150
    lp = lprule.search(sentence)
    if lp:
        sp = lp.span()
        parts = sentence[sp[1]:].split(' ')
        if len(parts) >= 1 and parts[0].strip(',.-_').isdigit():
            return parts[0].strip(',.-_')
        if len(parts) >= 2 and parts[1].strip(',.-_').isdigit():
            return parts[1].strip(',.-_')
    #set local preference to 90
    for i in range(len(items)-1,-1,-1):
        if (items[i] == 'to' or items[i] == '=') and i < len(items)-1:
            return items[i+1].strip(',.-_')
        #Set local pref=80
        if items[i].find('=')>-1:
            return items[i][items[i].find('=')+1:].strip(',.-_')
    #Lower local preference by 15
    if 'decrease' in items or 'lower' in items:
        for i in range(len(items)):
            if items[i] == 'by' and i < len(items)-1:
                return '-'+items[i+1].strip(',.-_')
            if items[i].find('->') > -1:
                return items[i].split('->')[1].strip(',.-_')
    if 'increase' in items:
        for i in range(len(items)):
            if items[i] == 'by' and i < len(items)-1:
                return '+'+items[i+1].strip(',.-_')
    if 'lowest' in items:
        return 'lowest'
    for i in range(len(items)-1,-1,-1):
        if items[i] == 'for' and i < len(items)-1:
            return items[i+1].strip(',.-_')
    for i in range(len(items)-1,-1,-1):
        if items[i].isdigit():
            return items[i].strip(',.-_')
    if 'lower' in items or 'below' in items:
        for rel in rels:
            if rel in items:
                return 'lower than '+rel
    if 'higher' in items:
        for rel in rels:
            if rel in items:
                return 'higher than '+rel
    if 'backup' in items:
        return 'backup'
    return 'unknown'
def selectann(inputlist):
    items = []
    for item in inputlist:
        if item != '':
            items.append(item)
    sentence = ' '.join(items)
    sym = '+'
    if 'not' in items or 'NOT' in items or 'no' in items:
        sym = '-'
    sa = sarule.search(sentence)
    sp = sa.span()
    sentence = sentence[sp[1]:]
    if sentence.find('with') > -1:
        sentence = sentence[:sentence.find('with')].strip()
    return sym+sentence
def selectann2(inputlist):
    items = []
    for item in inputlist:
        if item != '':
            items.append(item)
    sentence = ' '.join(items)
    if sentence.startswith('NO-OUT-'):
        sym = '-'
        return sym+sentence[7:]
    sym = '+'
    if 'not' in items or 'NOT' in items or 'no' in items:
        sym = '-'
    for i in range(len(inputlist)):
        item = inputlist[i]
        for word in sawords:
            if item.lower().find(word):
                return sym+' '.join(inputlist[i+1:])
def selectpp(inputlist):
    items = []
    for item in inputlist:
        if item != '':
            items.append(item)
    sentence = ' '.join(items)
    for i in range(len(items)):
        if items[i] == 'to':
            return '+'+' '.join(items[i+1:])
    return None
def prepend(inputlist):
    items = []
    for item in inputlist:
        if item != '':
            items.append(item)
    sentence = ' '.join(items)
    numt = pptime1.search(sentence)
    if numt:
        sp = numt.span()
        time = int(sentence[sp[0]])
        return time
    numt = pptime2.search(sentence)
    if numt:
        sp = numt.span()
        time = int(sentence[sp[1]-1])
        return time
    for item in items:
        if item.lower() in ppnumdic:
            return ppnumdic[item.lower()]
    for item in items:
        if item.isdigit() and int(item)<15:
            return int(item)
    count = {}
    for item in items:
        if item.isdigit():
            if item not in count:
                count[item] = 0
            count[item] += 1
    tups = sorted(count.items(),key=lambda x:x[1],reverse=True)
    if len(tups)>0:
        return tups[0][1]
    if sentence.find('without') > -1 or sentence.find('not') > -1:
        return 0
    return None
def taginfo(inputlist):
    items = []
    for item in inputlist:
        if item not in ['','-',':','|',"***"]:
            items.append(item)
        for word in stopwords:
            if item.lower().find(word) > -1:
                return None
    sentence = ' '.join(items)
    inf = inforule.search(sentence)
    if inf:
        sp = inf.span()
        sentence = sentence[sp[1]:]
    prefs = ['from','learned','ORIGIN-']
    for pref in prefs:
        if sentence.find(pref) > -1:
            sentence = sentence[sentence.find(pref)+len(pref)+1:]
            break
    sentence = sentence.strip()
    if sentence == "":
        return None
    
    ret = []
    items = sentence.split(' ')
    #ASN
    for item in items:
        if asnrule.search(item):
            ret.append(['ASN',item])
    #ASN only num, pick num in top 30,000 asrank
    if len(ret) == 0:
        for item in items:
            if item.isdigit() and item in top3w:
                ret.append(['ASN',item])
                break
    #IXP
    for i in range(len(items)):
        item = items[i].strip(' ,:.-|')
        if item.endswith('ix') or item.endswith('IX') or item.endswith('RS') or item.endswith('INX'):
            if item == 'prefix':
                continue
            if len(item) == 2:
                if i > 0:
                    ret.append(['IXP',' '.join(items[i-1:i+1])])
            else:
                ret.append(['IXP',item])
        else:
            parts = item.split('-')
            for part in parts:
                if part.endswith('IX') or part.endswith('INX'):
                    ret.append(['IXP',item])
                    break
    #geolocation NLP
    geoset = set()
    orgset = set()
    
    for i in range(5):
        doc1 = nlp1(sentence)
        doc2 = nlp2(sentence)
        for ent in doc1.ents:
            if ent.label_ == 'GPE':
                geoset.add(ent.text)
            elif ent.label_ == 'ORG':
                orgset.add(ent.text)

        for ent in doc2.ents:
            if ent.label_ == 'GPE':
                geoset.add(ent.text)
            elif ent.label_ == 'ORG':
                orgset.add(ent.text)

    for geon in geoset:
        ret.append(['geo',geon])
    for orgn in orgset:
        inprior = False
        for item in ret:
            if item[1] in orgn:
                inprior = True
                break
        if not inprior:
            ret.append(['fac',orgn])
    return ret
    
    
def rulebased(items):
    sentence = ' '.join(items)
    infos = []
    #local preference
    if lprule.search(sentence) or lprule2.search(sentence):
        semantic = localpref(items)
        infos.append(['pref',semantic])
    for word in lpwords:
        if sentence.find(word) > -1:
            semantic = localpref(items)
            infos.append(['pref',semantic])
            break
    #blackholing
    if bhrule.search(sentence):
        infos.append(['blackhole',''])
        return infos
    #selctive announcement
    if sarule.search(sentence):
        semantic = selectann(items)
        infos.append(['selectann',semantic])
    else:
        for word in sawords:
            if sentence.lower().find(word) > -1:
                semantic = selectann2(items)
                infos.append(['selectann',semantic])
                break
    #prepending
    if pprule.search(sentence):
        semantic = prepend(items)
        semantic2 = selectpp(items)
        if semantic2:
            infos.append(['selectann',semantic2])
        infos.append(['prepend',semantic])
    #relationship
    if len(infos) == 0:
        relset = set()
        for word in relworddic:
            if sentence.lower().find(word) > -1:
                relset.add(relworddic[word])
        if len(relset) > 0:
            if len(relset) == 1:
                for rel in relset:
                    infos.append(['rel', rel])
            if len(relset) == 2:
                if ("peer" in relset and "provider" in relset):
                    infos.append(['rel', "provider"])
                if ("peer" in relset and "customer" in relset):
                    infos.append(['rel', "customer"])
    # info (ASN+IXP+facility+location)
    if len(infos) == 0:
        semantic = taginfo(items)
        if semantic:
            for sem in semantic:
                infos.append(sem)
    return infos

def assemble(dic,asn,val,typ,semlist):
    if asn not in dic:
        dic[asn] = {}
    if typ == 'explicit':
        val = int(val)
    for sem in semlist:
        if sem[1] == None:
            sem[1] = 'N/A'
        if sem[0] == 'pref':
            if 'pref' not in dic[asn]:
                dic[asn]['pref'] = []
            if type(sem[1]) != int and sem[1].strip().isdigit():
                sem[1] = int(sem[1].strip())
            dic[asn]['pref'].append([typ,val,sem[1]])
        elif sem[0] == 'blackhole':
            if 'blackhole' not in dic[asn]:
                dic[asn]['blackhole'] = []
            if type(sem[1]) != int and sem[1].strip().isdigit():
                sem[1] = int(sem[1].strip())
            dic[asn]['blackhole'].append([typ,val])
        elif sem[0] == 'selectann':
            if 'sel_ann' not in dic[asn]:
                dic[asn]['sel_ann'] = {}
            target = sem[1]
            if target[0] == '+':
                if 'export' not in dic[asn]['sel_ann']:
                    dic[asn]['sel_ann']['export'] = []
                dic[asn]['sel_ann']['export'].append([typ,val,target[1:].strip()])
            else:
                if 'no-export' not in dic[asn]['sel_ann']:
                    dic[asn]['sel_ann']['no-export'] = []
                dic[asn]['sel_ann']['no-export'].append([typ,val,target[1:].strip()])
        elif sem[0] == 'prepend':
            if 'prepend' not in dic[asn]:
                dic[asn]['prepend'] = []
            if type(sem[1]) != int and sem[1].strip().isdigit():
                sem[1] = int(sem[1].strip())
            dic[asn]['prepend'].append([typ,val,sem[1]])
        elif sem[0] == 'rel':
            if 'tag' not in dic[asn]:
                dic[asn]['tag'] = {}
            if 'rel' not in dic[asn]['tag']:
                dic[asn]['tag']['rel'] = []
            dic[asn]['tag']['rel'].append([typ,val,sem[1]])
        elif sem[0] == 'geo':
            if 'tag' not in dic[asn]:
                dic[asn]['tag'] = {}
            if 'loc' not in dic[asn]['tag']:
                dic[asn]['tag']['loc'] = []
            dic[asn]['tag']['loc'].append([typ,val,sem[1]])
        elif sem[0] == 'ASN':
            if 'tag' not in dic[asn]:
                dic[asn]['tag'] = {}
            if 'asn' not in dic[asn]['tag']:
                dic[asn]['tag']['asn'] = []
            if type(sem[1]) != int and sem[1].strip().isdigit():
                sem[1] = int(sem[1].strip())
            dic[asn]['tag']['asn'].append([typ,val,sem[1]])
        elif sem[0] == 'IXP':
            if 'tag' not in dic[asn]:
                dic[asn]['tag'] = {}
            if 'IXP' not in dic[asn]['tag']:
                dic[asn]['tag']['IXP'] = []
            dic[asn]['tag']['IXP'].append([typ,val,sem[1]])
        elif sem[0] == 'fac':
            if 'tag' not in dic[asn]:
                dic[asn]['tag'] = {}
            if 'fac' not in dic[asn]['tag']:
                dic[asn]['tag']['fac'] = []
            dic[asn]['tag']['fac'].append([typ,val,sem[1]])


def cleanline(line):
    line = line.strip()
    cline = ''
    i = 0
    while i < len(line):
        if line[i] != '<':
            cline+= line[i]
            i+=1
        else:
            while i < len(line) and line[i]!='>':
                i+=1
            i+=1
    cline = cline.strip()
    return cline

def parser(irrf):
    lines = f.readlines()
    last = None
    info = {}
    for lineindex in range(len(lines)):
        line = lines[lineindex].strip()
        comm = communityrule.search(line)
        v6add = ipv6rule.search(line)
        if comm:
            sp = comm.span()
            #remove time e.g.8:20am
            if (sp[1]+1) < len(line) and (line[sp[1]:sp[1]+2].lower() == 'am'\
                or line[sp[1]:sp[1]+2].lower() == 'pm'):
                    continue
            if timerule.match(comm.group()):
                continue
            #remove IPv6 addresses
            if v6add and comm.group() in v6add.group():
                continue
            #remove ASN:AS-CUSTOMERS ASN:or ASN:RS-CUSTOMERS
            value = comm.group()
            upper,lower = value.split(':')
            cline = cleanline(line)
            comm = communityrule.search(cline)
            if comm == None:
                continue
            sp = comm.span()
            #if the community value is a number
            if lower.isdigit():
                sentence = cline[:sp[0]] + cline[sp[1]:]
                sentence = sentence.strip()
                if sentence == '':
                    for indexj in range(lineindex+1,min(lineindex+6,len(lines))):
                        cline = cleanline(lines[indexj])
                        if cline != '':
                            sentence = cline
                            break
                if sentence == '':
                    continue
                items = re.split('[ .()_\t/]',sentence)
                # rule-based
                res = rulebased(items)
                if res:
                    assemble(dic,upper,lower,'explicit',res)
                #else:
                    #regex can not parse, use NLP
                    #res = NLPpredicttype(items)
                    #assemble(dic,upper,lower,'explicit',res)

                
for fn in os.listdir('./webparser/'):
    with open('./webparser/' + fn, 'r') as f:
        parser(f)

with open('semanticdic_webpage.json','w',encoding='utf-8') as f:
    json.dump(dic,f)






