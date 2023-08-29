from tkinter.ttk import Combobox

import matplotlib
import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def preprocessing(data):
    # 数据预处理，得到最新一次和上一次介损和电容
    data['latest_tg'] = ''
    data['latest_pf'] = ''
    data['last_tg'] = ''
    data['last_pf'] = ''
    data['strategy'] = ''

    for j in range(len(data)):
        data.loc[j, 'flag_tg'] = 0
        data.loc[j, 'flag_pf'] = 0
        for i in range(2, 10):  # 获取最新数据值和上一次数据
            # print(str(data.loc[j]['tgδ（%）.'+str(i)]))
            # print(str(data.loc[j]['电容量（pF）.'+str(i)]))
            if (str(data.loc[j]['tgδ（%）.' + str(i)]) != 'nan') and (str(data.loc[j]['电容量（pF）.' + str(i)]) != 'nan'):
                if data.loc[j, 'latest_tg'] != '':
                    data.loc[j, 'last_tg'] = data.loc[j, 'latest_tg']
                    data.loc[j, 'last_pf'] = data.loc[j, 'latest_pf']
                data.loc[j, 'latest_tg'] = data.loc[j, 'tgδ（%）.' + str(i)]
                data.loc[j, 'latest_pf'] = data.loc[j, '电容量（pF）.' + str(i)]

    return data


def compared_vertical(data, type, problems_count):
    strategy = ['（1）一个周期内2次+FDS，套管油色谱等。',
                '（1）开展FDS，套管油色谱分析。', '一个周期内2次+FDS，套管油色谱等',
                '（1）开展FDS，套管油色谱分析', '立即更换套管', '一个试验周期开展2次试验', '立即更换套管',
                '一个试验周期开展2次试验', '要求查明原因']

    for j in range(len(data)):
        # 计算每一行与交接试验的结果变化值
        if j == 2034:
            print('')
        change_rate = 0
        if data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    # 与交接试验数据比较
                    if str(data.loc[j, 'tgδ（%）.1']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                            data.loc[j, 'tgδ（%）.1'])
                        title = '与交接试验比较--'
                elif type == 2:
                    # 与上一次试验数据比较

                    if str(data.loc[j, 'last_tg']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, 'tgδ（%）.2']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）'])) / float(
                            data.loc[j, 'tgδ（%）'])
                        title = '与最早一次试验比较--'
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.5) and (change_rate > 0.3) and data.loc[j, 'flag_tg'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '500kV介损介于0.4%到0.5%并且与上次试验比较增速超过30%：' + strategy[0])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题一')
                elif float(data.loc[j, 'latest_tg']) > 0.5 and data.loc[j, 'flag_tg'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '500kV介损大于0.5%：' + strategy[1])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题二')
            except Exception as e:
                print('1', e)

        ######################################################################################################
        elif data.loc[j, '主变电压等级'] == '220kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, 'tgδ（%）.1']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                            data.loc[j, 'tgδ（%）.1'])
                        title = '与交接试验比较--'
                elif type == 2:
                    # if data.loc[j, '变电站'] == '220kV谷立变':
                    #     print('a')
                    if str(data.loc[j, 'last_tg']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, 'tgδ（%）.2']) != '':
                        change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）'])) / float(
                            data.loc[j, 'tgδ（%）'])
                        title = '与最早一次试验比较--'
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.7) and (change_rate > 0.3) and data.loc[j, 'flag_tg'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '220kV及以下介损介于0.4%到0.7%并且与上次试验比较增速超过30%：' + strategy[2])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题三')
                elif float(data.loc[j, 'latest_tg']) > 0.7 and data.loc[j, 'flag_tg'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '220kV及以下介损大于0.7%：' + strategy[3])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题四')
            except Exception as e:
                print('2', e)

        ######################################################################################################
        change_rate = 0
        if data.loc[j, '主变电压等级'] == '220kV主变' or data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, '电容量（pF）.1']) != '':
                        change_rate = (float(data.loc[j, 'latest_pf']) - float(data.loc[j, '电容量（pF）.1'])) / float(
                            data.loc[j, '电容量（pF）.1'])
                        title = '与交接试验比较--'
                elif type == 2:

                    if str(data.loc[j, 'last_pf']) != '':
                        change_rate = (float(data.loc[j, 'latest_pf']) - float(data.loc[j, 'last_pf'])) / float(
                            data.loc[j, 'last_pf'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, '电容量（pF）.2']) != '':
                        change_rate = (float(data.loc[j, 'latest_pf']) - float(data.loc[j, '电容量（pF）.2'])) / float(
                            data.loc[j, '电容量（pF）.2'])
                        title = '与最早一次试验比较--'
                if 0.02 < change_rate < 0.03 and data.loc[j, 'flag_pf'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '220kV及以上电容增大2%到3%：' + strategy[5])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题五')
                elif change_rate > 0.03 and data.loc[j, 'flag_pf'] == 1:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title + '220kV及以上电容增大3%以上：' + strategy[4])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                    problems_count.append('问题六')
            except Exception as e:
                print('3', e)
        # if data.loc[j, '主变电压等级'] < 126kV:
    return data


def compared_horizontal(data, problems_count):
    group_a_index = ['A', 'B', 'C']
    group_b_index = ['Am', 'Bm', 'Cm']
    group_c_index = ['Oa', 'Ob', 'Oc']
    group_d_index = ['a*', 'x', 'b*', 'y', 'c*', 'z']

    itemsName = data['变电站'].unique()

    for item in itemsName:

        subData = data[data['变电站'] == item]
        subItemName = subData['主变编号'].unique()
        for subItem in subItemName:
            groupA = []
            groupB = []
            groupC = []
            groupD = []

            temp = subData[subData['主变编号'] == subItem]
            index = temp.index

            for m in index:
                if temp.loc[m, '所属相别'] in group_a_index:
                    groupA.append(m)
                elif temp.loc[m, '所属相别'] in group_b_index:
                    groupB.append(m)
                elif temp.loc[m, '所属相别'] in group_c_index:
                    groupC.append(m)
                elif temp.loc[m, '所属相别'] in group_d_index:
                    groupD.append(m)

            # indexA = groupA.index()
            # indexB = groupB.index()
            # indexC = groupC.index()
            # indexD = groupD.index()

            list_all = {'groupA': {'list': groupA, 'avg_tg': 0, 'avg_pf': 0}, 'groupB': {'list': groupB, 'avg_tg': 0, 'avg_pf': 0}, 'groupC': {'list': groupC, 'avg_tg': 0, 'avg_pf': 0}, 'groupD': {'list': groupD, 'avg_tg': 0, 'avg_pf': 0}}
            for list in list_all.values():
                count_tg = 0
                count_pf = 0
                if len(list.get('list')) < 2:
                    continue
                for i in list.get('list'):
                    for j in list.get('list'):
                        # 介损：某相增长其中任一相的30%
                        if i != j:
                            try:
                                rate_tg = ((float(temp.loc[i, 'latest_tg']) - float(temp.loc[j, 'latest_tg'])) /
                                           float(temp.loc[j, 'latest_tg']))
                                count_tg += rate_tg

                                rate_pf = ((float(temp.loc[i, 'latest_pf']) - float(temp.loc[j, 'latest_pf'])) /
                                           float(temp.loc[j, 'latest_pf']))
                                count_pf += rate_pf
                            except Exception as e:
                                print(e)

                            if rate_tg > 0.3:
                                data.loc[i, 'flag_tg'] = 1
                            if rate_pf > 0.03:
                                data.loc[i, 'flag_pf'] = 1
                list['avg_tg'] = count_tg / (len(list.get('list')) * (len(list.get('list'))-1))
                list['avg_pf'] = count_pf / (len(list.get('list')) * (len(list.get('list'))-1))

            for m in index:
                try:
                    if temp.loc[m, '所属相别'] == 'O':
                        change_O_pf = (float(temp.loc[m, 'latest_pf']) - float(temp.loc[m, 'last_pf']))/float(temp.loc[m, 'last_pf'])
                        change_O_tg = (float(temp.loc[m, 'latest_tg']) - float(temp.loc[m, 'last_tg']))/float(temp.loc[m, 'last_tg'])
                        if change_O_pf - list_all.get('groupA').get('avg_pf') > 0.03:
                            temp.loc[m, 'flag_pf'] = 1
                        if change_O_tg - list_all.get('groupA').get('avg_tg') > 0.3:
                            temp.loc[m, 'flag_tg'] = 1
                    elif temp.loc[m, '所属相别'] == 'Om':
                        change_Om_pf = (float(temp.loc[m, 'latest_pf']) - float(temp.loc[m, 'last_pf']))/float(temp.loc[m, 'last_pf'])
                        change_Om_tg = (float(temp.loc[m, 'latest_tg']) - float(temp.loc[m, 'last_tg']))/float(temp.loc[m, 'last_tg'])
                        if change_Om_pf - list_all.get('groupB').get('avg_pf') > 0.03:
                            temp.loc[m, 'flag_pf'] = 1
                        if change_Om_tg - list_all.get('groupB').get('avg_tg') > 0.3:
                            temp.loc[m, 'flag_tg'] = 1
                except Exception as e:
                    print(e)
        # try:
        #     print()
        # except Exception as e:
        #     print(e)
        # # group = data[]

    return data


def get_bad(data, problems_count):
    def delt():
        if Lstbox1.curselection() != ():
            Lstbox1.delete(Lstbox1.curselection())

    def show():
        item_count = data['序号'].count()
        bad_count = bad_item['序号'].count()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.pie([bad_count, item_count - bad_count], labels=['bad_item', 'norman_item'], autopct='%1.1f%%')
        ax.axis('equal')

        plt.show()

    def show2():
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['font.family']=['SimHei']
        # 解决中文字体下坐标轴负数的负号显示问题
        plt.rcParams['axes.unicode_minus'] = False

        dic = {}
        for key in problems_count:
            dic[key] = dic.get(key, 0) + 1
        print(dic)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(problems_count)
        ax.set_title('different sample sizes')

        plt.show()

    def second_wind():
        def display():
            kv_list = ['220kV', '500kV']
            place_list = ['贵阳', '遵义', '六盘水', '安顺', '凯里', '都匀', '兴义', '毕节', '铜仁']
            # print(comb.current())
            current_data = data[data['供电局'] == place_list[comb2.current()]]
            current_data = current_data[current_data['变电站'].str.contains(kv_list[comb.current()])]

            bad_data = current_data[current_data['strategy'] != '']

            item_count = current_data['序号'].count()
            bad_count = bad_data['序号'].count()

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.pie([bad_count, item_count - bad_count], labels=['bad_item', 'norman_item'], autopct='%1.1f%%')
            ax.axis('equal')

            plt.show()

        win2 = Toplevel(root)
        win2.geometry('200x120')
        win2.title('选项')
        lb = Label(win2, text='电压等级(kV)：')
        lb.place(relx=0, rely=0)
        comb = Combobox(win2, values=['220', '500'], width=10)
        comb.place(relx=0.4, rely=0)

        lb2 = Label(win2, text='供电局：')
        lb2.place(relx=0, rely=0.3)
        comb2 = Combobox(win2, values=['贵阳', '遵义', '六盘水', '安顺', '凯里', '都匀', '兴义', '毕节', '铜仁'],
                         width=10)
        comb2.place(relx=0.4, rely=0.3)

        btClose = Button(win2, text='查询', command=display)
        btClose.place(relx=0.7, rely=0.5)

    root = Tk()
    root.title('预警信息')
    root.geometry('1300x700')  # 这里的乘号不是 * ，而是小写英文字母 x

    frame1 = Frame(root, relief=RAISED)
    frame1.place(relx=0.0)

    frame2 = Frame(root, relief=GROOVE)
    frame2.place(relx=0.8)

    Lstbox1 = Listbox(frame1, width=130, height=40, font='华文新魏')
    Lstbox1.pack()

    btn1 = Button(frame2, text='处理预警', command=delt, width=20, height=3)
    btn1.pack(fill=X)

    btn2 = Button(frame2, text='可视化展示', command=show, width=20, height=3)
    btn2.pack(fill=X)

    btn3 = Button(frame2, text='数据透视', command=second_wind, width=20, height=3)
    btn3.pack(fill=X)

    btn4 = Button(frame2, text='数据透视2', command=show2, width=20, height=3)
    btn4.pack(fill=X)
    # comb = Combobox(frame2, values=['220kV', '550kV'], width=20)
    # comb.pack(fill=X)

    bad_item = data[data['strategy'] != '']
    index = bad_item.index
    for item in range(len(bad_item)):
        Lstbox1.insert(END, bad_item.loc[index[item], '变电站'] + '—' + bad_item.loc[index[item], '主变编号'] + '—' +
                       bad_item.loc[index[item], '所属相别'] + '——————' + bad_item.loc[index[item], 'strategy'])
    root.mainloop()


# [介损介于0.4%到0.7%并且与上次试验比较增速超过30%, 介损大于0.7%并且与上次试验比较增速超过30%]
# [介损介于0.4%到0.5%并且与上次试验比较增速超过30%, 介损大于0.5%并且与上次试验比较增速超过30%]
# [电容增大2%-3%, 电容增大3%以上]
problems_count = []
data = pd.read_csv('C:/Users/86410/Desktop/文档/套管数据.csv', skiprows=[0])
data = preprocessing(data)
data = compared_horizontal(data, problems_count)
data = compared_vertical(data, 1, problems_count)
data = compared_vertical(data, 2, problems_count)
data = compared_vertical(data, 3, problems_count)

get_bad(data, problems_count)
data.to_csv('整合数据7.csv', index=False, encoding='gbk')
