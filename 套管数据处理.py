import pandas as pd


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


def compared_vertical(data, type):
    # print(data.columns)
    # data_jiaojie = data[(~data['tgδ（%）.1'].isnull()) & (~data['电容量（pF）.1'].isnull())]
    # print(data_jiaojie['主变电压等级'].unique())

    strategy = ['（1）一个周期内2次+FDS，套管油色谱等。（2）试验异常立即更换套管',
                '（1）开展FDS，套管油色谱分析。（2）有异常立即更换', '一个周期内2次+FDS，套管油色谱等',
                '（1）开展FDS，套管油色谱分析（2）有异常立即更换', '立即更换套管', '一个试验周期开展2次试验', '立即更换套管',
                '一个试验周期开展2次试验', '要求查明原因']

    for j in range(len(data)):
        # 计算每一行与交接试验的结果变化值
        # if j == 10:
        #     print('a')
        if data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    # 与交接试验数据比较
                    if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(
                            data.loc[j, 'tgδ（%）.1'])
                        title = '与交接试验比较--'
                elif type == 2:
                    # 与上一次试验数据比较
                    if str(data.loc[j, 'last_tg']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, 'tgδ（%）.2']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）'])) / float(
                            data.loc[j, 'tgδ（%）'])
                        title = '与最早一次试验比较--'
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.5) and (change_rate > 0.3):
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'500kV介损介于0.4%到0.5%并且与上次试验比较增速超过30%：' + strategy[0])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif float(data.loc[j, 'latest_tg']) > 0.5:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'500kV介损大于0.5%：' + strategy[1])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('1', e)

######################################################################################################
        elif data.loc[j, '主变电压等级'] == '220kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, 'tgδ（%）.1']) != 'nan':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）.1'])) / float(data.loc[j, 'tgδ（%）.1'])
                        title = '与交接试验比较--'
                elif type == 2:
                    if str(data.loc[j, 'last_tg']) != 'nan':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'last_tg'])) / float(
                            data.loc[j, 'last_tg'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, 'tgδ（%）.2']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_tg']) - float(data.loc[j, 'tgδ（%）'])) / float(
                            data.loc[j, 'tgδ（%）'])
                        title = '与最早一次试验比较--'
                if (0.4 < float(data.loc[j, 'latest_tg']) < 0.7) and (change_rate > 0.3):
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'220kV及以下介损介于0.4%到0.7%并且与上次试验比较增速超过30%：' + strategy[2])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif float(data.loc[j, 'latest_tg']) > 0.7:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'220kV及以下介损大于0.7%：' + strategy[3])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('2', e)

######################################################################################################
        if data.loc[j, '主变电压等级'] == '220kV主变' or data.loc[j, '主变电压等级'] == '500kV主变':
            try:
                if type == 1:
                    if str(data.loc[j, '电容量（pF）.1']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_pf']) - float(data.loc[j, '电容量（pF）.1'])) / float(
                            data.loc[j, '电容量（pF）.1'])
                        title = '与交接试验比较--'
                elif type == 2:
                    if str(data.loc[j, 'last_pf']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_pf']) - float(data.loc[j, 'last_pf'])) / float(
                            data.loc[j, 'last_pf'])
                        title = '与上一次试验比较--'
                elif type == 3:
                    # 与最早一次试验数据比较
                    if str(data.loc[j, '电容量（pF）.2']) != '':
                        change_rate = abs(float(data.loc[j, 'latest_pf']) - float(data.loc[j, '电容量（pF）.2'])) / float(
                            data.loc[j, '电容量（pF）.2'])
                        title = '与最早一次试验比较--'
                if 0.02 < change_rate < 0.03:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'220kV及以上电容增大2%到3%：'+strategy[5])
                    data.loc[j, 'strategy'] = '。'.join(temp)
                elif change_rate > 0.03:
                    temp = []
                    if data.loc[j, 'strategy'] != '':
                        temp.append(data.loc[j, 'strategy'])
                    temp.append(title+'220kV及以上电容增大3%以上：' + strategy[4])
                    data.loc[j, 'strategy'] = '。'.join(temp)
            except Exception as e:
                print('3', e)
        # if data.loc[j, '主变电压等级'] < 126kV:
    return data


def compared_horizontal(data):
    itemsName =data['变电站'].unique()
    try:
        for item in itemsName:
            subData = data[data['变电站'] == item]
            subItemName = subData['主变编号'].unique()
            for subItem in subItemName:
               temp = subData[subData['主变编号'] == subItem][:3]
               index = temp.index
               for i in index:
                    for j in index:
                    # 介损：某相增长其中任一相的30%
                        if i != j:
                            rate = abs((float(temp.loc[i, 'latest_tg']) - float(temp.loc[j, 'latest_tg'])) /
                                   float(temp.loc[j, 'latest_tg']))
                            # print(rate)
                            if rate > 0.3:
                                res = []
                                if temp.loc[index[0], 'strategy'] != '':
                                    res.append(temp.loc[index[0], 'strategy'])
                                res.append('介损某相增长任一项的30%：要求查明原因')
                                # print(index)
                                data.loc[index[0], 'strategy'] = '。'.join(res)
            # group = data[]
    except Exception as e:
        print(e)
    return data


data = pd.read_csv('C:/Users/86410/Desktop/文档/套管数据.csv', skiprows=[0])
data = preprocessing(data)
data = compared_vertical(data, 1)
data = compared_vertical(data, 2)
data = compared_vertical(data, 3)
# data = compared_horizontal(data)
data.to_csv('整合数据.csv', index=False, encoding='gbk')
