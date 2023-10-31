import os
import numpy as np
import pandas as pd

f_path = "E:\\cv_work_3\\Bert\\output"
files = os.listdir(f_path)
data = []
type = [0, 1, 2, 3, 4, 5, 6]
for file in files:
    weight = []
    path = f_path + "\\" + file
    r_file = open(path,'r',encoding='utf-8')
    file_content = r_file.readlines()
    file_content = file_content[1:]
    num, target = [], []
    dict = {}
    for sample in file_content:
        r_s = sample.split('\t')
        s_num, s_target = int(r_s[0]), int(r_s[1][0])
        dict[s_num] = s_target
        num.append(s_num)
        target.append(s_target)
    for i in range(len(type)):  # 按照不同的列，根据不同的指标转换为极大型指标，
        weight.append(target.count(i))
    data.append(weight)
#调整指标
def dataDirection_1(datas):
    '''极小型指标 -> 极大型指标'''
    return np.max(datas) - datas  # 套公式
def dataDirection_2(datas, x_best):
    '''中间型指标 -> 极大型指标'''
    temp_datas = datas - x_best
    M = np.max(abs(temp_datas))
    answer_datas = 1 - abs(datas - x_best) / M  # 套公式
    return answer_datas
def dataDirection_3(datas, x_min, x_max):
    '''区间型指标 -> 极大型指标'''
    M = max(x_min - np.min(datas), np.max(datas) - x_max)
    answer_list = []
    for i in datas:
        if (i < x_min):
            answer_list.append(1 - (x_min - i) / M)  # 套公式
        elif (x_min <= i <= x_max):
            answer_list.append(1)
        else:
            answer_list.append(1 - (i - x_max) / M)
    return np.array(answer_list)

def cal_ew(data0):
    # 返回每个样本的指数
    # 样本数，指标个数
    n, m = np.shape(data0)
    # 一行一个样本，一列一个指标
    # 下面是归一化
    maxium = np.max(data0, axis=0)
    minium = np.min(data0, axis=0)
    data = (data0 - minium) * 1.0 / (maxium - minium)
    ##计算第j项指标，第i个样本占该指标的比重
    sumzb = np.sum(data, axis=0)
    data = data / sumzb
    data[np.isnan(data)] = 0
    # 对ln0处理
    a = data * 1.0
    a[np.where(data == 0)] = 0.0001
    #    #计算每个指标的熵
    e = (-1.0 / np.log(n)) * np.sum(data * np.log(a), axis=0)
    e[np.isnan(e)] = 0
    #    #计算权重
    w = (1 - e) / np.sum(1 - e)
    w[np.isnan(w)] = 0
    recodes = np.sum(data * w, axis=1)
    return recodes

#计算得分并归一化
def temp3(answer2,ew):
    list_max = np.array(
        [np.max(answer2[0, :]), np.max(answer2[1, :]), np.max(answer2[2, :]), np.max(answer2[3, :]), np.max(answer2[4, :]), np.max(answer2[5, :])])  # 获取每一列的最大值
    list_min = np.array(
        [np.min(answer2[0, :]), np.min(answer2[1, :]), np.min(answer2[2, :]), np.min(answer2[3, :]), np.min(answer2[4, :]), np.min(answer2[5, :])])  # 获取每一列的最小值
    max_list = []  # 存放第i个评价对象与最大值的距离
    min_list = []  # 存放第i个评价对象与最小值的距离
    answer_list = []  # 存放评价对象的未归一化得分
    for k in range(0, np.size(answer2, axis=1)):  # 遍历每一列数据
        max_sum = 0
        min_sum = 0
        for q in range(0, 6):  # 有六个指标
            max_sum += ew[q]*np.power(answer2[q, k] - list_max[q], 2)  # 按每一列计算Di+
            min_sum += ew[q]*np.power(answer2[q, k] - list_min[q], 2)  # 按每一列计算Di-
        max_list.append(pow(max_sum, 0.5))
        min_list.append(pow(min_sum, 0.5))
        answer_list.append((min_list[k] / (min_list[k] + max_list[k])) *100) # 套用计算得分的公式 Si = (Di-) / ((Di+) +(Di-))
        max_sum = 0
        min_sum = 0
    answer = np.array(answer_list)  # 得分归一化
    return(answer)
    #return (answer / np.sum(answer))

def score_type(ans):
    '''教学类型 类别判断：1互动2灌输3讨论'''
    a = []
    for i in range(7):  # 按照不同的列，根据不同的指标转换为极大型指标，
        answer = None
        amount = sum(ans)
        if i == 0:  # 表扬或鼓励，区间型指标
            answer = dataDirection_3(ans[:, i].reshape(-1,1),int(amount[i]*0.25),int(amount[i]*0.5))
        elif i == 1:  # 讲解，区间型指标
            answer = dataDirection_3(ans[:, i].reshape(-1,1),int(amount[i]*0.1),int(amount[i]*0.5))
        elif i == 2:  # 接受并采纳学生主张,极大型指标
            answer = np.array(ans[:, i].reshape(-1,1))
        elif i == 3:  # 接受学生情感,区间型指标
            answer = dataDirection_1(ans[:, i].reshape(-1, 1))
        elif i == 4:  # 批评或维护权威性,极小型指标
            answer = dataDirection_1(ans[:, i].reshape(-1,1))
        elif i == 5:  # 提问，区间型
            answer = dataDirection_3(ans[:, i].reshape(-1,1),int(amount[i]*0.3),int(amount[i]*0.5))
        elif i == 6:  # 指令，区间型
            answer = dataDirection_3(ans[:, i].reshape(-1,1),int(amount[i]*0.3),int(amount[i]*0.5))
        else:  # 其他,归零
            answer = dataDirection_3(ans[i], 0, 300)
        a.append(answer)
    return a

####### 正向化矩阵标准化
def temp2(datas):
    K = np.power(np.sum(pow(datas, 2), axis=1), 0.5)
    for i in range(0, K.size):
        for j in range(0, datas[i].size):
            datas[i, j] = datas[i, j] / K[i]  # 套用矩阵标准化的公式
    return datas

#转换得分为类别
def get_2classes(ans,num):
    '''将数值转换为2类别'''
    a=[]
    for i in range(len(ans)):
        if ans[i]>num:
            a.append(1)
        else:
            a.append(2)
    return a

def get_3classes(ans,num1,num2):
    '''将数值转换为3类别'''
    a=[]
    for i in range(len(ans)):
        if ans[i]>=num2:
            a.append(1)
        elif num1<ans[i]<num2:
            a.append(2)
        else:
            a.append(3)
    return a

target = np.array(data)
ew=cal_ew(target)
######类型评价
answer12 = score_type(target)
# print("socre:",answer12)
answer12 = np.array(answer12)  # 将list转换为numpy数组
answer12 = temp2(answer12)  # 数组正向化
answer12[np.isnan(answer12)] = 0
answer12 = temp3(answer12,ew)  # 标准化处理去量纲
data12 = pd.DataFrame(answer12)  # 计算得分
data12 = pd.DataFrame(get_3classes(answer12,40,70))
print(data12)