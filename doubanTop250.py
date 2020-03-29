'''
@Description: 爬取豆瓣电影Top250
最好用动态ip，不然多几次会被限制访问
@Author: Mirrorli
@Date: 2020-03-27 20:16:00
'''
import io
import sys
import pandas as pd
import requests
import time
from lxml import html
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
# 防止命令行输出中文乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

plt.rcParams["font.sans-serif"]=["SimHei"] #用来正常显示中文标签
plt.rcParams["axes.unicode_minus"]=False #用来正常显示负号

data = defaultdict(list)

for i in range(10):
    url = "https://movie.douban.com/top250?start={}&filter=".format(i*25)
    # 设置一个请求头，不然服务器很容易判断为爬虫，而不让访问
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    print("正在抓取：{}".format(url))
    content = requests.get(url, headers=headers).content
    sel = html.fromstring(content)
    
    # 我们需要提取的信息都在class属性为info的div标签里
    for single_movie_info in sel.xpath('//div[@class="info"]'):
        # 电影名称
        title = single_movie_info.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0] 

        # 包含了除名称之外的其他信息
        info = single_movie_info.xpath('div[@class="bd"]')[0] 

        # 导演和主演
        director_and_performer = info.xpath('p[1]/text()')[0].strip()

        # 时间、地点、类型
        year_and_place_and_genre = info.xpath('p[1]/text()')[1].strip().split("/")
        # 时间
        year = year_and_place_and_genre[0].strip()
        # 地点
        place = year_and_place_and_genre[1].strip()
        # 类型
        genre = year_and_place_and_genre[2].strip()

        # 评分
        rating = info.xpath('div/span[@class="rating_num"]/text()')[0]
        # 评论用户数
        rating_num = info.xpath('div/span[last()]/text()')[0].split("人评价")[0]
        
        data["title"].append(title)
        data["director_and_performer"].append(director_and_performer)
        data["year"].append(year)
        data["place"].append(place)
        data["genre"].append(genre)
        data["rating"].append(rating)
        data["rating_num"].append(rating_num)
    time.sleep(1)
df = pd.DataFrame(data)

df["year"] = pd.to_numeric(df.year.str.replace("\(.*?\)", ""))
df["rating"] = pd.to_numeric(df.rating)
df["rating_num"] = pd.to_numeric(df.rating_num)

print(df.head())
# df.to_csv("top250.csv", encoding="utf_8_sig") //设置编码防止导出出现中文乱码