import module.dir_same
import module.a.dir_child
import module.a.b.dir_child_child

print(module.dir_same.add(0, 1))
print(module.a.dir_child.add(0, 2))
print(module.a.b.dir_child_child.add(0, 3))

# 已经引入的模块不会再次引入
import module.start1
import module.a.start2
import module.a.b.start3

# 如果存在一个start目录(与我们脚本名字一样),我们要引入start目录的文件,那么start目录里面,必须含有__init__.py文件
#import start.xx as xx
