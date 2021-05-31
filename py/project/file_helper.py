# python 3.4

"""
一，
1.包名、模块名、局部变量名，函数

全小写+下划线式 
或者 首字母小写驼峰

example：this_is_var
或者 ： thisIsVar

3.全局变量

全大写+下划线式驼峰

example：GLOBAL_VAR

二，类，
1.类名
首字母大写式驼峰
example：ClassName()
2.属性和方法
首字母小写驼峰
example:myPicture


三，关于下划线

以单下划线开头，是弱内部使用标识，from M import * 时，将不会导入该对象（python 一切皆对象）。
以双下划线开头的变量名，主要用于类内部标识类私有，不能直接访问。模块中使用见上一条。
双下划线开头且双下划线截尾的命名方法尽量不要用，这是标识
"""

import os
import hashlib
import shutil
import tempfile
import zipfile


def get_curpy_dir(file):
    return file[:file.rfind("\\")]


def md5_str(str):
    return hashlib.md5(bytes(str, "utf_8")).hexdigest()


def md5_file(file_path,upper=False):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code)#.upper()
    if upper:
        return md5.upper()
    return md5


def write_str_to_file(file, str):
    v_writed = 0
    with open(file, "w") as f:  # r rb r+ rb+ w wb w+ wb+ a ab a+ ab+
        v_writed = f.write(str)
        f.flush()
        # print("写入字节数:",v_writed)
    return v_writed


def copy_file(src_path, dst_path):
    """ 拷贝文件 """
    try:
        pos_1 = dst_path.rfind("/")
        pos_2 = dst_path.rfind("\\")
        pos = max(pos_1, pos_2)
        dir_dir = dst_path[0:pos]
        # print("需要创建的目录:",dir_dir)

        os.makedirs(dir_dir)  # 只能创建目录
    except FileExistsError:
        pass
    open(dst_path, "w").close()

    # if(os.path.isfile(dst_path)):
    # 	os.remove(dst_path)

    #dst_path = src_path + ".copy"
    print(src_path, "=>", dst_path, end=" : ")

    # 拷文件
    shutil.copy(src_path, dst_path)
    if os.path.isfile(dst_path):
        print("Copy Success")
    else:
        print("Copy Fail")


def copy_dir(src_path, dst_path):
    """拷贝目录"""
    if(os.path.exists(dst_path)):
        raise RuntimeError(dst_path+" is exists")

    # dst_path = src_path + ".copy"
    print(src_path, "=>", dst_path)

    shutil.copytree(src_path, dst_path)
    if os.path.isdir(dst_path):
        print(dst_path, "Copy Dir Success")


def move_file(src_file, dst_file):
    print(src_file, "->", dst_file)
    try:
        os.rename(src_file, dst_file)
        print("Move Success")
    except FileNotFoundError:
        pass
    except FileExistsError:
        # 文件已经存在
        # print(dst_file)
        os.remove(dst_file)  # 先移除文件
        os.rename(src_file, dst_file)  # 再尝试移动
        print("Move Success")
        # raise RuntimeError();


def move_dir(src_dir, dst_dir):
    print(src_dir, "->", dst_dir)
    shutil.move(src_dir, dst_dir)


def file_size(file):
    with open(file, "r") as f:  # r rb r+ rb+ w wb w+ wb+ a ab a+ ab+
        f.seek(0, 2)
        return f.tell()
    return 0


def is_file_exits(file):
    return os.path.exists(file) and os.path.isfile(file)


def is_dir_exits(path):
    return os.path.exists(path) and os.path.isdir(path)


def join(path, new_file):
    return path+"/"+new_file


class Diskwalk(object):
    def __init__(self, path, recursive=True):
        """ 
                构造函数 
                @path       指定目录
                @recursive  是否遍历子目录
        """
        self.path = path
        self.recursive = recursive

    def walk(self, func=None):
        """ 
                遍历目录和文件
                @func(dirpath, file)       指定回调, 回传当前路径和文件

                @return     返回 文件名数组,全路径文件名数组  一一对应
        """
        path_collection = []
        files = []
        for dirpath, dirnames, filenames in os.walk(self.path):

            # print("dirpath=",dirpath)
            # print("dirnames=",dirnames)
            # print("filenames=",filenames)

            for file in filenames:
                dirpath = dirpath.replace("\\", "/")
                if(func and callable(func)):
                    func(dirpath, file)

                files.append(file)
                # fullpath=os.path.join(dirpath,file)
                fullpath = dirpath+"/"+file #join(dirpath, file)
                path_collection.append(fullpath)

            if(not self.recursive):
                break

        return files, path_collection

    def walk_dir(self, func=None):
        """ 
                遍历目录不遍历文件
                @func(dirpath, dirname)       指定回调, 回传当前路径和文件

                @return     返回 所有子目录
        """
        path_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path):

            # print("dirpath=",dirpath)
            # print("dirnames=",dirnames)
            # print("filenames=",filenames)

            dirpath = dirpath.replace("\\", "/")
            for dirname in dirnames:
                if(func and callable(func)):
                    func(dirpath, dirname)

                fullpath = dirpath+"/"+dirname #join(dirpath, dirname)
                path_collection.append(fullpath)

            if(not self.recursive):
                break

        return path_collection


def make_dirs(dir):
    """
            依次创建父子目录
    """
    try:
        print("makedirs dir =>", dir)
        os.makedirs(dir)
    except FileExistsError:  # 异常捕获
        pass


def remove_file(file):
    os.remove(file)  # 删除文件


def remove_dir(dir):
    """
            删除目录中的所有内容
    """
    file_names, file_paths = Diskwalk(dir).walk()
    for i in range(len(file_paths)):
        os.remove(file_paths[i])
    dir_paths = Diskwalk(dir).walk_dir()
    # print(dir_paths);
    for i in range(len(dir_paths)-1, -1, -1):
        try:
            print("remvoe dir =>", dir_paths[i])
            os.rmdir(dir_paths[i])
        except FileNotFoundError:
            pass
    try:
        print("remvoe dir =>", dir)
        os.rmdir(dir)
    except FileNotFoundError:
        pass


def main():
    # print("**************************遍历目录文件结构")
    # print("结果数组=", Diskwalk(".").walk())
    # print("**************************遍历目录目录结构")
    # testDir = "D:\\glp\\work"
    # print("结果数组=", Diskwalk(testDir).walk_dir())
    # remove_dir(testDir)

    # r w a
    # with zipfile.ZipFile('D:/glp/cocos/spam.zip', 'a') as myzip:
    #     myzip.write('D:/glp/cocos/eggs.txt', 'D:/glp/cocos/eggs.txt')
    #     myzip.write('D:/glp/cocos/eggs1.txt', "eggs1.txt")

    dir = "D:/glp/Github/Fish2/frameworks/runtime-src/Classes"
    def walk1(dirpath, file):
        if file.endswith(".h"):
            print("${RUNTIME_SRC_ROOT}/Classes"+dirpath[len(dir):]+"/"+file)

    Diskwalk(dir).walk(walk1)

if __name__ == '__main__':
    main()
