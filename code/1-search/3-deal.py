
import csv
import re
import json




def results():

    dictlg={}
    for i in range(0, 10):
        file1 = open('Middle_results_' + str(i) + '.csv', 'r',encoding='utf-8')
        csv_reader1 = csv.reader(file1)
        for row in csv_reader1:
            str1=','.join(row)
            if(row[0]=='net'):
                print(row)
                continue
            title = re.findall(r'<title>(.*?)<\/title>', str1, re.S | re.M)
            for l in title:
                if(l!=''):
                    name=l.split('<URL>')[0]
                    if(name!=''):
                        el=l.split(name)[1]
                        urls= re.findall(r'<URL>(.*?),<\/URL>',el, re.S | re.M)
                        for url in urls:
                            dictlg[url]=name
    with open("search_results.json", "w") as f:
        json.dump(dictlg, f)
    print(len(dictlg))

if __name__ == '__main__':
    results()
