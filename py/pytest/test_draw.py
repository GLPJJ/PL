
# pip install matplotlib

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import time


x = [0, 1]
y = [0, 1.5]
#y = []
fig = plt.figure("盈利分析", (18, 5))
# plt.plot(x,y)
# plt.plot_date(x,y)

# x = range(3)
# y1 = [elem*2 for elem in x]
# plt.plot(x, y1)

# y2 = [elem**2 for elem in x]
# plt.plot(x, y2, 'r')

date1 = ["2017-01-01", "2017-01-02", "2017-01-03"]
date_times = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in date1]
# print(date_times[0])

y3 = [100, 200, 300]
dates = matplotlib.dates.date2num(date_times)


# 设置标题
fig.suptitle('diff', fontsize=14, fontweight='bold')
ax = fig.add_subplot(1, 1, 1)
ax.plot(dates, y3)
y4 = [200, 400, 600]
ax.plot(dates, y4, 'r')
# plt.plot_date(dates,y3)

# x轴标签旋转角度
plt.xticks(rotation=30)
# for label in ax.xaxis.get_ticklabels():
# 	label.set_rotation(45)

ax.set_xlabel("x label")
ax.set_ylabel("y label")

ax.xaxis.set_major_locator(mdates.DayLocator(
    bymonthday=range(1, 31), interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))


# plt.show()

# 画第二个图
plt.figure("b")
plt.plot(x,y)

plt.savefig("easyplot.jpg")
plt.show()
