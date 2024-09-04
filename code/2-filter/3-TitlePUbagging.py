import csv
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from random import shuffle
import json
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from baggingPU import BaggingClassifierPU
import pandas as pd
import joblib

with open('titles.json','r') as f:
    titles = json.load(f)

with open('title_labels.json','r') as f:
    labels = json.load(f)
    
cv = CountVectorizer(lowercase=True)

cv.fit(titles)
print(len(cv.get_feature_names()))

cv_fit_all = cv.transform(titles)

def bagging(cv_fit_all,labels,c,t,k):
    ###bagging model
    print('Training...',str(c),str(t),str(k))
    bc = BaggingClassifierPU(
        SVC(class_weight='balanced',C=c,probability=True,kernel='linear'),
        n_estimators=t,  # 1000 trees as usual
        max_samples = int(sum(labels)*k), # Balance the positives and unlabeled in each bag
        n_jobs = -1           # Use all cores
    )
    ##这是训练集合得到的模型
    bc.fit(cv_fit_all, labels)
    joblib.dump(bc, 'bcT' + str(t) + 'K' + str(K) + '.pkl')
    file=open('Title_probalineSVC'+str(c)+'-'+str(t)+'-'+str(k)+'.csv','w',encoding = 'utf-8')
    probility=bc.predict_proba(cv_fit_all)
    for i in range(0,len(probility)):
        file.writelines(titles[i])
        for key in probility[i]:
            file.writelines('\t'+str(key))
        file.writelines('\n')


T=[100]

K=[1]

for t1 in T:
    for k1 in K:
        bagging(cv_fit_all,labels,10,t1,k1)














