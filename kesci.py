'''
@Description: 获取和鲸社区所有项目
@Author: Mirrorli
@Date: 2020-04-13 15:53:16
'''
import io
import sys
import pandas as pd
import numpy as np
import requests
from string import Template
import json
import math
from collections import defaultdict, Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

urlTemplate = Template(
    'https://www.kesci.com/api/labs?perPage=${perPage}&page=${page}&Collapsed=${Collapsed}&sort=${sort}')

def getTotalCount():
    param = {'perPage': 1, 'page': 1, 'Collapsed': 'false', 'sort': '-SortWeight'}
    data = getSingleData(param)
    if data:
        return data['totalNum']
    else:
        return 0

def getDataFromKesci():
    totalCount = getTotalCount()
    perPage = 100
    kesciData = list()
    for i in range(math.ceil(totalCount / perPage)):
        param = {'perPage': perPage, 'page': i+1, 'Collapsed': 'false', 'sort': '-SortWeight'}
        data = getSingleData(param)
        if data and data['data']:
            kesciData.extend(data['data'])
    return kesciData

def localData():
    kesciData = getDataFromKesci()
    data = defaultdict(list)
    if kesciData:
        for i, v in enumerate(kesciData):
            data['title'].append(v['Title'])
            data['commentsCount'].append(v['CommentsCount'])
            data['createDate'].append(v['CreateDate'])
            data['forksCount'].append(v['ForksCount'])
            data['language'].append(v['Language'])
            data['shortDescription'].append(v['ShortDescription'])
            data['viewsCount'].append(v['ViewsCount'])
            data['votesCount'].append(v['VotesCount'])
            data['private'].append(v['Private'])
    return data
    
def getSingleData(param):
    url = urlTemplate.substitute(param)
    content = requests.get(url).content
    jsonObj = json.loads(content)
    if jsonObj:
        return jsonObj
    else:
        return {}

def saveAsCsv():
    data = localData()
    if data:
        df = pd.DataFrame(data)
        df.to_csv('kesci.csv', index=False, encoding="utf_8_sig")
        print('保存成功')
    else:
        print('无数据')

saveAsCsv()
