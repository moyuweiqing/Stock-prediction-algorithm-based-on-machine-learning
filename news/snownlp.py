import os
from snownlp import sentiment
import matplotlib.pyplot as plt
import numpy as np
import math

path = os.path.abspath('')
text = open(path + 'data1.txt')
text = text.read()
s1 = text.replace('\n', '').replace(' ', '').replace('.', '。')#去除换行

#建立情感分析
sn1 = SnowNLP(s1)
sentimentslist = []
for i in sn1.sentences:
    j = SnowNLP(i)
    sentimentslist.append(j.sentiments)
dic = {}
for i in np.arange(0, 1, 0.02):
    index = round(i, 2)
    dic[index] = 0
for i in sentimentslist:
    temp = round(math.floor(i/0.02)*0.02, 2)
    dic[temp] = dic[temp] + 1
plt.hist(sentimentslist,bins=np.arange(0,1,0.02))