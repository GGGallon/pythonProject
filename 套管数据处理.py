import pandas as pd
import numpy as np


def compared_jiaojie(data):
    print(data.columns)
    # data_jiaojie = data[(~data['tgδ（%）.1'].isnull()) & (~data['电容量（pF）.1'].isnull())]
    # print(data_jiaojie['主变电压等级'].unique())
    data_jiaojie_group550 = data[data['主变电压等级'] == '550kV主变']
    data_jiaojie_group220 = data[data['主变电压等级'] == '220kV主变']

    data['latest_tg'] = ''
    data['latest_pf'] = ''
    data['last_tg'] = ''
    data['last_pf'] = ''
    data['strategy'] = ''

    strategy = ['（1）一个周期内2次+FDS，套管油色谱等。（2）试验异常立即更换套管',
                '（1）开展FDS，套管油色谱分析。（2）有异常立即更换', '一个周期内2次+FDS，套管油色谱等',
                '（1）开展FDS，套管油色谱分析（2）有异常立即更换', '立即更换套管', '一个试验周期开展2次试验', '立即更换套管',
                '一个试验周期开展2次试验']

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

        # 计算每一行与交接试验的结果变化值
        if data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                    # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                    # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                    change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                        data.loc[j, 'tgδ（%）.1'])
                    if (0.004 < float(data.loc[j, 'latest_tg']) < 0.005) or (change_rate > 0.3):
                        temp = []
                        if data.loc[j, 'strategy'] != '':
                            temp.append(data.loc[j, 'strategy'])
                        temp.append(strategy[0])
                        data.loc[j, 'strategy'] = temp
                    elif float(data.loc[j, 'latest_tg']) > 0.005:
                        temp = []
                        if data.loc[j, 'strategy'] != '':
                            temp.append(data.loc[j, 'strategy'])
                        temp.append(strategy[1])
                        data.loc[j, 'strategy'] = temp
            except :
                print('1')
        elif data.loc[j, '主变电压等级'] == '220kV主变':
            try:
                if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                    # change_rate_jiaojie = (data.loc[j, 'latest_tg'].astype(float) - data.loc[j, 'tgδ（%）.1'].astype(
                    # float)) / data.loc[j, 'tgδ（%）.1'].astype(float)
                    change_rate = (float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                        data.loc[j, 'tgδ（%）.1'])
                    if (0.004 < float(data.loc[j, 'latest_tg']) < 0.007) or (change_rate > 0.3):
                        temp = []
                        if data.loc[j, 'strategy'] != '':
                            temp.append(data.loc[j, 'strategy'])
                        temp.append(strategy[2])
                        data.loc[j, 'strategy'] = temp
                    elif float(data.loc[j, 'latest_tg']) > 0.007:
                        temp = []
                        if data.loc[j, 'strategy'] != '':
                            temp.append(data.loc[j, 'strategy'])
                        temp.append(strategy[3])
                        data.loc[j, 'strategy'] = temp
            except :
                print('2')
    return data  


data = pd.read_csv('C:/Users/86410/Desktop/文档/套管数据.csv', skiprows=[0])
data = compared_jiaojie(data)
