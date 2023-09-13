from pylab import *
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox


def cal():
    res = []
    try:
        for t in my_list:
            res.append(math.sqrt(2) * ib * math.sin(100 * math.pi * t - math.pi / 2) + math.sqrt(2) * ib * math.exp(
                -t / (tdc / 1000)))
    except Exception as e:
        print(e)
    return res


def processing():
    output = {'data1': 0, 'data2': 0, 'data3': 0}
    index_1 = -1
    index_2 = -1
    count = int((t_opening + t_protect) / 0.00001)
    try:
        if res[count] < res[count+1]: #上升沿
            for j in range(count, len(res)):
                count += 1
                if res[j+1] < res[j]:
                    break

        for i in range(count, len(res) - 1):
            if index_1 < 0:
                if res[i + 1] > res[i] and res[i] < 0 and res[i + 1] > 0:
                    if abs(res[i]) < abs(res[i + 1]):
                        index_1 = i
                    else:
                        index_1 = i + 1
            else:
                if res[i + 1] < res[i] and res[i] > 0 and res[i + 1] < 0:
                    if abs(res[i]) < abs(res[i + 1]):
                        index_2 = i
                    else:
                        index_2 = i + 1
                    break
    except Exception as e:
        print(e)
    output['data1'] = round(max(res[index_1:index_2]), 4)
    output['data2'] = (index_2 - index_1) * 0.01
    output['data3'] = output['data1'] * output['data2']
    return output


start = 0
end = 0.08
step = 0.00001
my_list = [i for i in range(int(start / step), int(end / step))]
my_list = [x * step for x in my_list]

# 实例化
root = tk.Tk()
root.withdraw()
# 获取文件夹路径
f_path = filedialog.askopenfilename()
print('\n获取的文件地址：', f_path)

# file = pd.read_excel('C:/Users/86410/Desktop/新建文件夹/附件3：220kV及以上断路器校核清单及校核结果提交模板.xlsx',
#                      sheet_name='220kV', header=[0, 1])
file = pd.read_excel(f_path, sheet_name='220kV', header=[0, 1])
# print(file.columns)
for index in range(len(file)):
    ib = file.loc[index, ('短路电流计算数据', '短路电流交流分量有效值Ib/kA')]  # 短路电流交流分量有效值
    tdc = file.loc[index, ('短路电流计算数据', '时间常数τdc/ms')]  # 短路电流直流分量时间常数

    t_protect = 10 / 1000  # 继保时间10ms
    t_opening = file.loc[index, ('型式试验数据', '设备最短分闸时间/ms')] / 1000  # 开关最短分闸时间

    res = cal()
    # plt.plot(my_list, res)
    # show()

    dic = processing()
    file.loc[index, ('MATLAB计算结果', '熄弧大半波电流峰值')] = dic['data1']
    file.loc[index, ('MATLAB计算结果', '最后大半波时间/ms')] = dic['data2']
    file.loc[index, ('MATLAB计算结果', '短路电流计算值熄弧大半波电流峰值与熄弧大半波电流持续时间乘积/kA*ms')] = dic['data3']

    try:
        if file.loc[index, ('型式试验数据', '额定开断电流/kA')] > file.loc[index, ('220kV及以上变电站母线短路电流', '三相接地短路电流（kA）')]:
            file.loc[index, ('校核结果', '短路开断电流是否满足要求')] = '是'
        else:
            file.loc[index, ('校核结果', '短路开断电流是否满足要求')] = '否'
        if file.loc[index, ('型式试验数据', '额定开断电流/kA')] > file.loc[index, ('短路电流计算数据', '短路电流交流分量有效值Ib/kA')]:
            file.loc[index, ('校核结果', '交流分量是否超标')] = '否'
        else:
            file.loc[index, ('校核结果', '交流分量是否超标')] = '是'
        if file.loc[index, ('型式试验数据', '额定开断电流/kA')] > file.loc[index, ('短路电流计算数据', '时间常数τdc/ms')]:
            file.loc[index, ('校核结果', '直流分量是否超标')] = '否'
        else:
            file.loc[index, ('校核结果', '直流分量是否超标')] = '是'
        if file.loc[index, ('型式试验数据', '型式试验熄弧大半波电流峰值与熄弧大半波电流持续时间乘积/kA*ms')] < \
                file.loc[index, ('MATLAB计算结果', '短路电流计算值熄弧大半波电流峰值与熄弧大半波电流持续时间乘积/kA*ms')]:
            file.loc[index, ('校核结果', '熄弧大半波峰值电流与持续时间乘积是否满足要求')] = '否'
        else:
            file.loc[index, ('校核结果', '熄弧大半波峰值电流与持续时间乘积是否满足要求')] = '是'
        if file.loc[index, ('型式试验数据', '额定峰值耐受电流/kA')] < file.loc[index, ('MATLAB计算结果', '熄弧大半波电流峰值')]:
            file.loc[index, ('校核结果', '峰值耐受电流是否满足要求')] = '否'
        else:
            file.loc[index, ('校核结果', '峰值耐受电流是否满足要求')] = '是'
    except Exception as e:
        print(e)


file.to_excel('计算结果.xlsx')
msgbox.showinfo('提示', '计算结果已生成')
