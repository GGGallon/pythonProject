import pandas as pd
import numpy as np
import math

def preprocessing(data):
    data['latest_tg'] = ''
    data['latest_pf'] = ''
    data['last_tg'] = ''
    data['last_pf'] = ''
    data['strategy'] = ''

    for j in range(len(data)):
        for i in range(2, 10):  # 获取最新数据值和上一次数据
            # print(str(data.loc[j]['tgδ（%）.'+str(i)]))
            # print(str(data.loc[j]['电容量（pF）.'+str(i)]))
            if (str(data.loc[j]['tgδ（%）.' + str(i)]) != 'nan') and (str(data.loc[j]['电容量（pF）.' + str(i)]) != 'nan'):
                if data.loc[j, 'latest_tg'] != '':
                    data.loc[j, 'last_tg'] = data.loc[j, 'latest_tg']
                    data.loc[j, 'last_pf'] = data.loc[j, 'latest_pf']
                data.loc[j, 'latest_tg'] = data.loc[j]['tgδ（%）.' + str(i)]
                data.loc[j, 'latest_pf'] = data.loc[j]['电容量（pF）.' + str(i)]

    return data


def compared(data, type):
    # print(data.columns)
    # data_jiaojie = data[(~data['tgδ（%）.1'].isnull()) & (~data['电容量（pF）.1'].isnull())]
    # print(data_jiaojie['主变电压等级'].unique())

    strategy = ['（1）一个周期内2次+FDS，套管油色谱等。（2）试验异常立即更换套管',
                '（1）开展FDS，套管油色谱分析。（2）有异常立即更换', '一个周期内2次+FDS，套管油色谱等',
                '（1）开展FDS，套管油色谱分析（2）有异常立即更换', '立即更换套管', '一个试验周期开展2次试验', '立即更换套管',
                '一个试验周期开展2次试验']

    for j in range(len(data)):
        # 计算每一行与交接试验的结果变化值
        if data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                        # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                        # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                            data.loc[j, 'tgδ（%）.1'])
                elif type == 2:
                    if str(data.loc[j, 'last_tg']) != '':
                        # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                        # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.5) or (change_rate > 0.3):
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('500kV介损介于0.4%到0.5%或者与上次试验比较增速超过30%：' + strategy[0])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif float(data.loc[j, 'latest_tg']) > 0.5:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('500kV介损大于0.5%：' + strategy[1])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('1', e)

######################################################################################################
        elif data.loc[j, '主变电压等级'] == '220kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                        # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                        # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(data.loc[j, 'tgδ（%）.1'])
                elif type == 2:
                    if str(data.loc[j, 'last_tg']) != 'nan':
                        # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                        # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.7) or (change_rate > 0.3):
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('220kV及以下介损介于0.4%到0.7%或者与上次试验比较增速超过30%：' + strategy[2])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif float(data.loc[j, 'latest_tg']) > 0.7:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('220kV及以下介损大于0.7%：' + strategy[3])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('2', e)

######################################################################################################
        if data.loc[j, '主变电压等级'] == '220kV主变' or data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    change_rate = abs(float(data.loc[j, 'latest_pf']) - float(data.loc[j, '电容量（pF）.1'])) / float(
                        data.loc[j, '电容量（pF）.1'])
                elif type == 2:
                    change_rate = abs(float(data.loc[j, 'latest_pf']) - float(data.loc[j, 'last_pf'])) / float(
                        data.loc[j, 'last_pf'])
                if 0.02 < change_rate < 0.03:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('220kV及以上电容增大2%到3%：'+strategy[5])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif change_rate > 0.03:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append('220kV及以上电容增大2%到3%：' + strategy[4])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('3', e)
        # if data.loc[j, '主变电压等级'] < 126kV:
    return data


data = pd.read_csv('C:/Users/86410/Desktop/文档/套管数据.csv', skiprows=[0])
data = preprocessing(data)
data = compared(data, 1)
data.to_csv('整合数据.csv', index=False, encoding='gbk')
