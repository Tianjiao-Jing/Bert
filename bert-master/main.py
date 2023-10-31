import os
import argparse
from moviepy.editor import AudioFileClip
import json
import jieba
from pylab import *
import pandas as pd
import seaborn as sns
import Step1_Wave2Text
import Step2_Text2Keywords

# #传参数
# parser = argparse.ArgumentParser()
# parser.add_argument("--name", default="shawroad", help="这里输入的是名字")
# parser.add_argument("--age", type=int, required=True, help="这里是年龄")
# parser.add_argument("--sex", choices=["男", "女"])
# args = parser.parse_args()
# parser.print_help()  # 当你不知道参数怎样指定，这样就会打印出参数的说明

#Wave2Text
"""
    ********************************************************************************************
    这一部分是将视频.mp4,转换成音频.wav，再将音频文件转换为文本.txt,去除停用词。
    ********************************************************************************************
"""
def Wave2Text(upload_mp4_path = "test.mp4", appid = "96d1b2e0", secret_key = "0220b2e2148e0558ac73c71792eb72a1",\
              wav_path="test.wav", ban_list = ['，', '。', '?', '!', '、', '？', '！', ' ']):

    lfasr_host = 'http://raasr.xfyun.cn/api'

    #视频提取音频
    my_audio_clip = AudioFileClip(upload_mp4_path)
    my_audio_clip.write_audiofile(wav_path)

    # 请求的接口名
    api_prepare = '/prepare'
    api_upload = '/upload'
    api_merge = '/merge'
    api_get_progress = '/getProgress'
    api_get_result = '/getResult'
    # 文件分片大小10M
    file_piece_sice = 10485760
    # api = Step1_Wave2Text.RequestApi(appid="96d1b2e0", secret_key="0220b2e2148e0558ac73c71792eb72a1", upload_file_path=r"test.wav")
    upload_file_path = wav_path
    api = Step1_Wave2Text.RequestApi(appid=appid, secret_key=secret_key,\
                                     upload_file_path=wav_path,\
                                     file_piece_sice = 10485760,\
                                     api_prepare = api_prepare,\
                                     api_upload = api_upload,\
                                     api_merge = api_merge,\
                                     api_get_progress = api_get_progress, \
                                     api_get_result = api_get_result,\
                                     lfasr_host = lfasr_host)
    api.all_api_request(appid, secret_key, upload_file_path, file_piece_sice, api_prepare,\
                 api_upload, api_merge, api_get_progress, api_get_result)
    # ban_list = ['，', '。', '?', '!', '、', '？', '！', ' ']
    ban_list = ban_list #后面可以删掉，这里只是提醒我这里改了
    bianma_file = open("result.txt", 'r', encoding='utf-8')
    result_file = open("final_result.txt", 'r', encoding='utf-8')
    for line in bianma_file:
        s_sentence = ""
        # 排除 ban_list 中的字符
        for j in range(len(line)):
            if line[j] in ban_list:
                continue
            else:
                s_sentence = s_sentence + line[j]
        result_file.write(s_sentence)
    bianma_file.close()
    result_file.close()
    os.remove("result.txt")

#Text2Keywords
"""
    ********************************************************************************************
    这一部分是将视频.mp4,转换成音频.wav，再将音频文件转换为文本.txt,去除停用词。
    ********************************************************************************************
"""
def Txt2Keywords():
    #接口地址
    url ="https://ltpapi.xfyun.cn/v1/ke"
    #开放平台应用ID
    x_appid = "96d1b2e0"
    #开放平台应用接口秘钥
    api_key = "e3ad262df5508ff6a887cd07e237442d"

    # 语言文本
    with open('result1.json', 'r', encoding='utf8')as fp:
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
        result = Step2_Text2Keywords.Get_Key(TEXT)
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

if __name__ == '__main__':
    Wave2Text()