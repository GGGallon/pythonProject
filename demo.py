#print()--->1.数字 2.字符串 3.表达式 4.将数据输出到文件
fp = open('C:/Users/86410/Desktop/demo.txt', 'a+')
print('Hello Python', file=fp)
fp.close()
#转义字符
print('\'--')
print('hello\rworld')
#
import keyword
print(keyword.kwlist)
#进制
print(8)
print(0b1000)
print(0o10)
print(0x8)
#浮点数
from decimal import Decimal
print(Decimal('2.2')+Decimal('1.1'))
#int(),float(),str()互相转
#取余：一正一负按公式计算：余数=被除数-除数*商
#赋值运算符
'''
id:xxx
type:yyy
value:zzz
'''
a=10
b=10
print(id(a), id(b))
a += 1
print(id(a), id(b))
#布尔运算符and,or,not,in,not in
#位运算符&,|,<<,>>(溢出舍弃，低位补0)
#while计算0-100之间的偶数和
res = 0
count = 0
while count <= 100:
    if count % 2 == 0:
        res += count
    count+=1
print(res)
#水仙花数
for i in range(100, 999):
    if int(i/100)**3 + int(i/10%10)**3 + (i%10)**3 == i:
        print(i, sep=',')
#else的搭配：if-else,while-else,for-else
#列表操作：查找某个元素---List.index(str),列表切片---list[start,stop,step],列表增加---list.append(),list.extend(),list.insert(),切片
#列表删除:list.remove(item),list.pop(index),切片,list.clear,del list
#列表排序:list.sort()
#列表生成式：[i for i in range(1,10)]

#字典查找:dic['key'],dic.get('key)
#字典删除:del dic['key'],字典新增:dic['key'] = value
#获取字典视图：dic.key(),dic.value().dic.item()
#字典生成式{item:price for item,price in zip(items,prices)}

#集合添加s.add(item),s.update({item1,item2})/s.update([item1,item2])
#集合删除s.remove(item)抛异常,s.discard(item)无异常
#集合判断是否是子集s.issubset(s1),是否是超集s1.issupset(s),两个集合是否有交集s.isdisjoint(s1)
#集合求交集 s1 & s2,并集 s1 | s2,差集 s1-s2,对称差集s1^s2
#集合生成式{i for i in range(10)}
s={1,2,3,4,5,6}
s.update({7,8,9})
print(s)
#字符串查找str.index(),str.rindex()
#字符串常用：str.upper(),str.lower(),str.title()
#字符串分割:str.split()
#字符串判断:
#字符串替换:str.replace('str1','str2'),'|'.join(列表或者元组)
#格式化字符串:'我是%s,今年%d岁'%(name,age)  / ‘我的名字{0},今年{1}岁,请叫我{0}’.format(name,age)  /  f'我叫{name},今年{age}岁'

n1 = [1, 2, 3]
print(id(n1))
n1.append(4)
print(id(n1))

#关键字传参*或者**
#斐波那契数列
def f1(num):
    if num == 1 or num == 2:
        return 1
    return f1(num-1) + f1(num-2)

print(f1(5))
print('*************************')
#特殊方法
class Student:
    def __init__(self, name):
        self.name = name
    def __add__(self, other):
        return self.name + other.name

stu1 = Student('张三')
stu2 = Student('李四')
print(stu1+stu2)
