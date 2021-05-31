#!python3.6
# @ guliping

# 类 python

# 定义类


class Person(object):
    """docstring for Person"""

    # 默认规则 __xx__一般都是python内建的函数； __xx表示private
    # 定义属性

    # 类的静态变量
    cls_1 = "Human1"  # 公开变量 public
    _cls_1 = "Human2"  # 公开变量 public
    __cls_1 = "Human3"  # 私有变量 private

    test = 1
    test2 = []

    # 构造函数
    def __init__(self):
        super(Person, self).__init__()

    # python的构造函数是唯一的，如果需要传递不同的参数，可以考虑使用可变长参数传递
    # 如果定义了多个构造函数，默认取用最后定义的构造函数
    def __init__(self, name, age, phone):
        super(Person, self).__init__()

        # 声明成员变量
        self.name = name
        self._phone = phone
        self.__age = age
        self.test1 = []
        class_name = self.__class__.__name__
        # print(class_name, "__init__")
        print("Person __init__")

    # 定义析构函数
    def __del__(self):
        class_name = self.__class__.__name__
        # print(class_name, "__del__")
        print("Person __del__")

    # 定义类方法
    def getPhone(self):
        return self._phone

    def getAge(self):
        return self.__age


# 查看类说明
print(Person.__doc__)

# 创建类实例
per = Person("Jack", 12, "13000000001")
print(per.name)
print(per._phone)
# print(per.__age)#这里会报错 AttributeError: 'Person' object has no attribute '__age'
print(per.getAge())


# python 中在类中定义对象和在构造函数中定义对象的结果是不一样的，如果定义在类的最外面，则表示该变量是类的静态变量，大家都可访问
# 如果只是定义在构造函数中，那么这个是实例的变量，每个实例独立
per2 = Person("Kate", 11, "13000000003")
print("per.test=", per.test)
per2.test = 2
print("在类中定义的数字(成员变量) per.test=", per.test, per2.test)
per2.test2.append("A")
print("在类中定义的列表对象(静态变量) per.test2=", per.test2, per2.test2)
per2.cls_1 = "Human4"
print("在类中定义的字符串(成员变量) per.cls_1=", per.cls_1, per2.cls_1)
per2.test1.append("A")
print("在构造函数中定义的列表对象(成员变量) per.test1=", per.test1, per2.test1)
# 及时释放对象
del per  # 这样会去调用类的析构函数

# 子类继承


class Student(Person):  # class Student(Person,P1,P2):#继承多个父类
    """docstring for Student"""

    def __init__(self, name, age, phone, id):
        # 主动调用父类构造
        super(Student, self).__init__(name, age, phone)
        self.id = id  # 学号
        class_name = self.__class__.__name__
        # print(class_name, "__init__")
        print("Student __init__")

    def __del__(self):
        class_name = self.__class__.__name__
        # print(class_name, "__del__")
        print("Student __del__")

        # 需要主动调用父类析构
        super(Student, self).__del__()

    # 重载父类方法
    def getPhone(self):
        return str(self.id)+":"+self._phone

    # python类内建方法重载
    def __repr__(self):
        # 转化为供解释器读取的形式
        # 简单的调用方法 : repr(obj)
        pass

    def __str__(self):
        # 用于将值转化为适于人阅读的形式
        # 简单的调用方法 : str(obj)
        pass

    def __cmp__(self, x):
        # 对象比较
        # 简单的调用方法 : cmp(obj, x)
        pass


stu = Student("Tom", 13, "13000000002", 1)
print(Student.__bases__)  # 查看基类
print(stu.getPhone())

print("hasattr(stu, 'name')=", hasattr(stu, 'name'))    # 如果存在 'age' 属性返回 True。
print("hasattr(stu, '_phone')=", hasattr(
    stu, '_phone'))    # 如果存在 'age' 属性返回 True。
print("hasattr(stu, '__age')=", hasattr(stu, '__age'))    # 私有变量不能外部访问

print("getattr(stu, 'test')=", getattr(stu, 'test'))    # 返回 'test' 属性的值
print(dir(stu))
setattr(stu, 'test', 8)  # 添加属性 'test' 值为 8 这里的添加属性可以把类内部定义的属性覆盖
print("stu.test=", stu.test)
print(dir(stu))
delattr(stu, 'test')   # 删除属性 'test' 如果类内部也定义了该属性，则保留该属性的原始值
print("stu.test=", stu.test)  # 如果类内部没有定义该属性，那么删除属性之后再访问是会报错了。。这里不会
# 访问对象的私有属性,其实可以通过 dir查看有哪些可以访问的属性或方法
print("stu._Person__age=", stu._Person__age)

# 判断实例关系和继承关系
print("isinstance(per2,Person)=", isinstance(per2, Person))
print("issubclass(Student,Person)=", issubclass(Student, Person))


class Point:

    x: 0
    y: 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 操作符重载
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def area(self):
        # python 抛出异常使用raise
        raise NotImplementedError("Point no area")


a = Point(1, 2)
b = Point(4, 6)
c1 = a+b
c2 = a-b
print(c1.x, c1.y)
print(c2.x, c2.y)
try:
    # python 没有像java那样给出严格的接口实现才能实例化的机制，不过我们可以通过raise一个错误来强制子类实现他们的方法
    c1.area()
except Exception as e:
    print(e)
    pass

print("*"*100)
