#!python3.4
# @ guliping

from eB import __d  # 但是可以指定引入某个私有成员或者方法
from eB import *
from eB import a
''' 模块
http://blog.csdn.net/glp3329/article/details/52713288
'''

import eA
import sys

print(sys.path)

print(dir(eA))  # 私有的方法和成员不展示
print(eA.__d)  # 虽然是私有的，但是我们可以直接访问

a()
# b()  #未引入，便会报错

b()
# print(__d) #报错，私有成员或者方法，不能通过from xxx import * 引入

print(__d)

# python模块支持在某个目录下添加 __init__.py 作为引入包的初始化函数， __all__ = ["A","B"] 指定需要加载的子模块
