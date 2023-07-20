file = 'info.txt'
def addInfo(stuInfo):
    id = input('请输入学生ID:')
    name = input('请输入学生姓名:')
    eGrade = int(input('请输入学生英语成绩:'))
    pGrade = int(input('请输入学生Python成绩:'))
    jGrade = int(input('请输入学生Java成绩:'))
    totalGrade = eGrade+pGrade+jGrade

    stu = {'id':id,'name':name,'eGrade':eGrade,'pGrade':pGrade,'jGrade':jGrade,'totalGrade':totalGrade}
    stuInfo.append(stu)
    save(stuInfo)

def save(stuInfo):
    try:
        fp = open(file, 'a', encoding='utf-8')
    except:
        fp = open(file, 'w', encoding='utf-8')
    for i in stuInfo:
        fp.write(str(i)+ '\n')

def openFile():
    try:
        fp = open(file, 'r', encoding='utf-8')
    except:
        fp = open(file, 'w', encoding='utf-8')
    lines = fp.readlines()
    res = []
    for i in lines:
        res.append(eval(i))
    return res

def searchInfo(stuInfo):
    tempId = input('请输入查找ID:')
    for i in stuInfo:
        if i.get('id') == tempId:
            print(i)
            return
    print('该学生不存在')
    return

def delInfo(stuInfo):
    tempId = input('请输入删除ID:')
    for i in stuInfo:
        if i.get('id') == tempId:
            stuInfo.remove(i)
            return
    print('该学生不存在')
    return

def changeInfo(stuInfo):
    tempId = input('请输入修改ID:')
    for i in stuInfo:
        if i.get('id') == tempId:
            i['id'] = input('请输入学生ID:')
            i['name'] = input('请输入学生姓名:')
            i['eGrade'] = int(input('请输入学生英语成绩:'))
            i['pGrade'] = int(input('请输入学生Python成绩:'))
            i['jGrade'] = int(input('请输入学生Java成绩:'))
            i['totalGrade'] = i['eGrade'] + i['pGrade'] + i['jGrade']
            return
    print('该学生不存在')
    return

def sortInfo(stuInfo):
    print(sorted(stuInfo,key=lambda info:info['totalGrade']))
def countInfo(stuInfo):
    print('总计学生信息条数：', len(stuInfo))
def showInfo(stuInfo):
    for info in stuInfo:
        print(info)


if __name__ == '__main__':
    stuInfo = openFile()
    mainInfo = '''=================学生信息管理系统====================
-------------------功能菜单------------------------
                1.录入学生信息
                2.查找学生信息
                3.删除学生信息
                4.修改学生信息
                5.排序
                6.统计学生总人数
                7.显示学生信息
                0.退出系统
--------------------------------------------------
请选择:'''
    while(True):
        case = int(input(mainInfo))
        if case == 1:
            addInfo(stuInfo)
        elif case == 2:
            searchInfo(stuInfo)
        elif case == 3:
            delInfo(stuInfo)
        elif case == 4:
            changeInfo(stuInfo)
        elif case == 5:
            sortInfo(stuInfo)
        elif case == 6:
            countInfo(stuInfo)
        elif case == 7:
            showInfo(stuInfo)
        elif case == 0:
            break

