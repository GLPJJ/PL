#!python3.4
# @ guliping

import tempfile
import shutil
import os
import math
import sys
"""
IO，标准IO，文件IO
"""

print("命令行参数")
for i in range(len(sys.argv)):
    print("sys[", i, "]=", sys.argv[i])

# 格式化字符串输出  str.format()
# str()： 函数返回一个用户易读的表达形式。
# repr()： 产生一个解释器易读的表达形式。
s1 = "Hello World\n"
print(str(s1), repr(s1))

for x in range(1, 3):
    print('{0:2d} {1:4d} {2:4d}'.format(x, x*x, x*x*x))
print("{0:.3f}".format(1.5))  # 类似c中的printf
print("{0:02d}".format(1))

# 位置参数与关键字参数
# 等价于print("{},{}".format("apple","pen"))
print("{0},{1}".format("apple", "pen"))
print("{1},{0}".format("apple", "pen"))
print("{1},{0},{all}".format("apple", "pen", all="applepen"))  # 关键字参数只能放在位置参数后面

table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
print('Runoob: {0[Runoob]:d}; Google: {0[Google]:d}; '
      'Taobao: {0[Taobao]:d}'.format(table))


# '!a' (使用 ascii()), '!s' (使用 str()) 和 '!r' (使用 repr())
# 可以用于在格式化某个值之前对其进行转化:
print('常量 PI 的值近似为： {}。'.format(math.pi))
# 常量 PI 的值近似为： 3.141592653589793。
print('常量 PI 的值近似为： {!r}。'.format(math.pi))
# 常量 PI 的值近似为： 3.141592653589793。

# 需要在解释器环境中
# print("读取键盘读入")
#s2 = input("请输入：");
#print ("你输入的内容是: ", s2)

print("*"*60)

# 文件IO
"""
open(filename, mode)
filename：filename 变量是一个包含了你要访问的文件名称的字符串值。
mode：mode决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。
这个参数是非强制的，默认文件访问模式为只读(r)。
"""

f = open("zzz_io_test", "w")  # r rb r+ rb+ w wb w+ wb+ a ab a+ ab+
v_writed = f.write("Hello World \n\tfrom python")
f.flush()
print("写入字节数:", v_writed)
f.close()

f1 = open("zzz_io_test", "r")
s3 = f1.read()  # f.read(size) siez 指定读取大小，如果没有传，读取文件全部内容
f1.close()
print("读取全部文件内容:", s3, repr(s3))

f2 = open("zzz_io_test", "r")
s4 = f2.readline()

# tell() 返回文件对象当前所处的位置, 它是从文件开头开始算起的字节数
print("当前位置", f2.tell())

'''
f.seek(offset, from_what) 函数。 
offset 可以为正负值
from_what 的值(默认0), 如果是 0 表示开头, 如果是 1 表示当前位置, 2 表示文件的结尾
'''
f2.seek(0)
print("当前位置", f2.tell())
f2.seek(0, 2)  # r文本格式读取的时候，位置参数是1或2时，偏移只能是0，否则报错
print("当前位置", f2.tell())
f2.close()
print("读取文件一行内容", s4)

f2_1 = open("zzz_io_test", "rb")
f2_1.seek(0)  # 文件开始位置
print("当前位置", f2_1.tell())
f2_1.seek(-2, 2)  # 文件末尾位置
print("当前位置", f2_1.tell())
f2_1.seek(-5, 1)  # 文件指针当前位置
print("当前位置", f2_1.tell())
f2_1.close()

f3 = open("zzz_io_test", "r")
s5 = f3.readlines()
f3.close()
print("读取文件所有行", s5)

f4 = open("zzz_io_test", "r")
for line in f4:
    print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
f4.close()

print()
print("*"*60)
'''
通常我们操作文件的时候使用with关键字，它可以帮我们关闭文件。
'''
with open("zzz_io_test", "r") as f5:
    for line in f5:
        print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
        print()
        print("f5 文件关了吗？", f5.closed)


# pickle模块，支持python基本数据到保存文件的序列化和反序列化


'''
了解了文件之后，我们需要对目录操作进一步的深入
东西很多，但是常用的就那么几个，我们一个一个学习
'''

print("*"*60)
'''
修改访问权限
os.chmod(path, mode, *, dir_fd=None, follow_symlinks=True) 
修改当前工作路径
os.chdir(path) 
展示当前路径下的文件目录列表，不包含'.' ; '..'
os.listdir(path='.')
'''
print(os.listdir())
'''
创建目录
os.mkdir(path, mode=0o777, *, dir_fd=None) 
'''
try:
    os.mkdir("dir_test")
except FileExistsError:  # 异常捕获
    pass
'''
创建目录列表，根据name
os.makedirs(name, mode=0o777, exist_ok=False) 
'''
try:
    os.makedirs("dir_test/a/a.txt")  # 只能创建目录
except FileExistsError:
    pass

# 查看文件是否存在，是否是文件或是目录
print("zzz_io_test 存在吗？ "+str(os.path.exists("zzz_io_test")) +
      ","+str(os.path.isfile("zzz_io_test")))
print(os.path.isdir("zzz_io_test"))

'''
删除文件，如果是目录会报错
os.remove(path, *, dir_fd=None) 
'''
os.remove("zzz_io_test")  # 删除文件
'''
递归删除空目录
os.removedirs(name) 
'''
os.removedirs("dir_test/a/a.txt")
'''
修改文件名或者目录名
os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None) 
递归修改目录名
os.renames(old, new) 
'''
# try:
# 	os.mkdir("dir_test")
# except FileExistsError: #异常捕获
# 	pass
try:
    os.rename("dir_test", "dir_test_1")
except FileNotFoundError:
    pass
'''
替换文件，如果dst是目录则会报错
os.replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None) 
删除空目录
os.rmdir(path, *, dir_fd=None) 
'''
try:
    os.rmdir("dir_test")
except FileNotFoundError:
    pass

'''
查看文件或者目录状态,返回一个class os.stat_result 
os.stat(path, *, dir_fd=None, follow_symlinks=True) 

终止
os.abort() 

执行一段程序，和调用者在同一个进程中。
os.execl(path, arg0, arg1, ...) 
os.execle(path, arg0, arg1, ..., env) 
os.execlp(file, arg0, arg1, ...) 
os.execlpe(file, arg0, arg1, ..., env) 
os.execv(path, args) 
os.execve(path, args, env) 
os.execvp(file, args) 
os.execvpe(file, args, env) 

退出with n
os._exit(n) 

执行程序，在新的进程中
os.spawnl(mode, path, ...) 
os.spawnle(mode, path, ..., env) 
os.spawnlp(mode, file, ...) 
os.spawnlpe(mode, file, ..., env) 
os.spawnv(mode, path, args) 
os.spawnve(mode, path, args, env) 
os.spawnvp(mode, file, args) 
os.spawnvpe(mode, file, args, env) 

执行系统脚本
os.system(command) 
'''
print("**************************拷贝目录")

# 拷贝目录与文件


def copyFile(src_path, dst_path):
    # filename1 = tempfile.mktemp (".txt")
    open(dst_path, "w").close()

    # if(os.path.isfile(dst_path)):
    # 	os.remove(dst_path)

    #dst_path = src_path + ".copy"
    print(src_path, "=>", dst_path)

    # 拷文件
    shutil.copy(src_path, dst_path)
    if os.path.isfile(dst_path):
        print(dst_path, "Copy Success")


def copyDir(src_path, dst_path):
    # 拷贝目录
    #dirname1 = tempfile.mktemp (".dir")
    os.mkdir(dst_path)
    # dst_path = src_path + ".copy"
    print(src_path, "=>", dst_path)

    shutil.copytree(src_path, dst_path)
    if os.path.isdir(dst_path):
        print(dst_path, "Copy Success")

# copyFile("test/testCopy","test/testCopy_")


print("**************************遍历目录结构")
# 遍历所有目录结构


def visitDir(path, func=None):
    retPaths = []  # 文件路径列表
    retFiles = []  # 文件名列表

    for dirpath, dirnames, filenames in os.walk(path):
        print("dirpath=", dirpath, ",dirnames=",
              dirnames, ",filenames=", filenames)

        for file in filenames:
            retFiles.append(file)
            fullpath = os.path.join(dirpath, file)
            retPaths.append(fullpath)

            if(func and callable(func)):
                func(dirpath, file)

    return retFiles, retPaths


print(visitDir("."))
