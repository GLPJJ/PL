import pandas  # pip install pandas
import random

indexs = [0]
columns = ["a", "b", "c"]
cols = []
for i in range(3):
    cols.append(int(random.random()*100))
print(cols)

print("*"*100)
data = [[1, 2, 3]]  # 传入DataFrame的必须是二维数组
df = pandas.DataFrame(data, columns=columns)
print(df)

print("*"*100)
df = pandas.DataFrame(columns=columns)
for i in range(3):
    df.insert(1, i, cols)  # 意思是插入列的意思
print(df)

print("*"*100)
df = pandas.DataFrame(columns=columns)
df.set_value(0, "a", columns)  # 插入指定位置的一个值
df.set_value(2, "b", 5)
print(df)
