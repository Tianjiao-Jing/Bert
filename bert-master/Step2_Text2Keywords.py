#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import jieba
import base64
from pylab import *
import pandas as pd
import seaborn as sns

#接口地址
url ="https://ltpapi.xfyun.cn/v1/ke"
#开放平台应用ID
x_appid = "10068772"
#开放平台应用接口秘钥
api_key = "96a1ec00b33e323afb73790a05ed327e"

def Get_Key(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    return result.decode('utf-8')

if __name__ == '__main__':
    # 语言文本
    with open('final_result.txt', 'r', encoding='utf8')as fp:
        lines = fp.readlines()  # readline是指按照行来读，readlines一次性读完，返回一个列表
        TEXT = ""
        for line in lines:
            TEXT += line[0:-1]

    #文本分段
    Text_List = []
    for i in range(10):#分成了10个部分去提取关键词
        text = TEXT[int(i * (len(TEXT) / 10)):int((i + 1) * (len(TEXT) / 10))]
        Text_List.append(text)

    k, v = [], []
    mydata = pd.DataFrame()
    count = 0
    # 对每个文本段进行处理
    for TEXT in Text_List:
        # 文本段计数
        count += 1
        # 关键词提取
        result = Get_Key(TEXT)
        result1 = json.loads(result)
        r_result = result1['data']['ke']
        # 词频统计
        words_lcut_all = jieba.lcut(TEXT)
        tf = len(words_lcut_all)
        cipin = dict()
        for i in r_result:
            w = i['word']
            x = 0
            for j in range(len(TEXT) - len(w) + 1):
                if TEXT[j:j + len(w)] == w:
                    x += 1
            # 词频保留三位有效数字
            cipin[w] = round(x / tf, 3)
        # 词频排序
        cipin = sorted(cipin.items(), key=lambda x: x[1])
        cipin = dict(cipin)
        # 整理为pd.DataFrame格式的数据
        # 数据结构为两列一组，第一列为关键词，第二列为词频，以此类推
        key1, value1 = '关键词' + str(count), '词频' + str(count)
        k.append(key1)
        v.append(value1)
        mydata[key1] = pd.Series(list(cipin.keys()))
        mydata[value1] = pd.Series(list(cipin.values()))
    # 对于缺省值补零
    mydata = mydata.fillna(0)

    # 预设图像各种信息
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,  # 子图上的标题字体大小
              # 'legend.fontsize': med,  # 图例的字体大小
              'figure.figsize': (med, small),  # 画布大小
              'axes.labelsize': med,  # 标签的字体大小
              'xtick.labelsize': med,  # x轴标尺的字体大小
              'ytick.labelsize': med,  # y轴标尺的字体大小
              'figure.titlesize': large}  # 整个画布的标题字体大小
    plt.rcParams.update(params)  # 设定各种默认属性
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('seaborn-whitegrid')  # 设置整体风格
    sns.set_style('white')
    fig = plt.figure(figsize=(5, 10), dpi=120, facecolor='w', edgecolor='k')
    for cc in range(len(k)):
        # 准备标签列表与颜色列表
        # 准备标签时去除标签中的缺省值0
        r = list(mydata[k[cc]])
        categories = []
        for rr in r:
            if rr != 0:
                categories.append(rr)
        # print(categories)
        colors = [plt.cm.tab10(i / float(len(categories) - 1)) for i in range(len(categories))]

        # 布置画布
        for i, category in enumerate(categories):
            plt.scatter(cc, i, data=mydata[v[cc]][i]
                        , s=mydata[v[cc]][i] * 140000  # 需要对比的属性
                        , c=np.array(colors[i]).reshape(1, -1)  # 点的颜色
                        , edgecolors=np.array(colors[i]).reshape(1, -1)  # 点的边缘颜色
                        , alpha=(i + 1) / len(categories)  # 透明度
                        , linewidths=.5)  # 点的边缘线的宽度
            # 在这里调整气泡上的文字
            plt.annotate(category, xy=(cc-0.1, i), fontproperties='SimHei')

    # 在这里调整坐标轴
    plt.xlabel('时间', fontproperties='SimHei')
    plt.ylabel('词频', fontproperties='SimHei')
    plt.xticks(fontsize=12, fontproperties='SimHei')
    plt.yticks(fontsize=12, fontproperties='SimHei')
    # 在这里设置刻度间隔
    ax = plt.gca()
    dx = MultipleLocator(1)  # x轴每1一个刻度
    dy = MultipleLocator(1)  # y轴每1一个刻度
    ax.xaxis.set_major_locator(dx)
    ax.yaxis.set_major_locator(dy)
    # 在这里调整标题
    plt.title('展示', fontsize=22, fontproperties='SimHei')
    # lgnd = plt.legend(prop = {'family':'SimHei'}, fontsize=12)
    plt.show()  # 显示图像