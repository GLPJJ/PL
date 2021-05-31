# python3

import os
import hashlib
import shutil
import tempfile
import zipfile

import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper

def join(path, new_file):
    return path+"/"+new_file

def make_dirs(dir):
    """
            依次创建父子目录
    """
    try:
        print("makedirs dir =>", dir)
        os.makedirs(dir)
    except FileExistsError:  # 异常捕获
        pass

def MergeToOneDirZip(src_dir,dest_dir):
    first_dirs = Diskwalk(src_dir, False).walk_dir()
    print(first_dirs)
    for i in range(len(first_dirs)):
        zip_name = first_dirs[i].replace(src_dir, "")+".zip"
        zip_name = zip_name[1:]
        print(zip_name)

        _, files = Diskwalk(first_dirs[i]).walk(None)
        # print(files)

        with zipfile.ZipFile(join(dest_dir, zip_name), 'w') as myzip:
            for j in range(len(files)):
                file = files[j]
                file_name = file.replace(src_dir, "")
                file_name = file_name[1:].replace("/", ".")
                file_name = file_name[:file_name.rfind(".")]
                print(zip_name, " <- ", file, file_name)
                # 指定压缩哪个文件，指定压缩文件中的目录名称
                myzip.write(file, file_name)

def MergeToOneDir(src_dir,dest_dir):
    def cp(dirpath, file):
        # print(dirpath,file)
        if file.endswith(".png"):
            file_helper.copy_file(dirpath+"/"+file,dest_dir+"/"+file)
    file_helper.Diskwalk(src_dir, True).walk(cp)

def MoveToBackDir(src_dir,dest_dir):
    def mv(dirpath, file):
        if file.endswith(".png"):
            # print(dirpath,file,dest_dir+"/"+file[0:2]+"/"+file)
            file_helper.move_file(dirpath+"/"+file,dest_dir+"/"+file[0:2]+"/"+file)
    file_helper.Diskwalk(src_dir, True).walk(mv)

if __name__ == '__main__':
    #微信小游戏资源图片统一移动一个目录压缩
    # MergeToOneDir("D:/work/Github/SmallFish/SmallFish/build/wechatgame/res/raw-assets","D:/work/UI/temp")
    # MoveToBackDir("D:/work/UI/temp/tinified","D:/work/Github/SmallFish/SmallFish/build/wechatgame/res/raw-assets")

    bundles = ["lobby","fish","shxb","yule","resources"]
    # for i in range(len(bundles)):
    #     MergeToOneDir("D:/work/Github/SmallFish/SmallFish/build/wechatgame/remote/"+bundles[i]+"/native","D:/work/UI/temp/"+bundles[i])
    for i in range(len(bundles)):
        MoveToBackDir("D:/work/UI/temp/"+bundles[i],"D:/work/Github/SmallFish/SmallFish/build/wechatgame/remote/"+bundles[i]+"/native",)
