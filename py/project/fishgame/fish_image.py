import fish_hotupdate
import os
import sys
import time
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper


IMAGE_KEY = "key"


def optionJSRes5(path, file):
    if(".webp" not in file):
        return

    fullpath = file_helper.join(path, file)

    new_path = path.replace("/zhitu-des/webp", "")
    new_path = new_path.replace("res1", "res")
    new_file = file.replace(".webp", ".png")
    new_fullpath = file_helper.join(new_path, new_file)
    print(fullpath, ">>", new_fullpath)

    file_helper.make_dirs(new_path)
    # file_helper.move_file(fullpath, new_fullpath)
    file_helper.copy_file(fullpath, new_fullpath)


def encFile(path, file):

    if file[-4:] != ".png" and file[-4:] != ".jpg" and file[-5:] != ".webp" and file[-4:] != ".jsc":
        return
    if(file == "loading.js"):
        return

    fullpath = file_helper.join(path, file)
    print("cur file = ", fullpath)
    with open(fullpath, "rb+") as fp:
        data = fp.read()
        dataLen = len(data)
        # print(type(data))
        newData = bytearray(dataLen)  # 申明字节数组
        print("len = ", dataLen)
        for i in range(len(data)):

            # ord()函数主要用来返回对应字符的ascii码，ord('a') = 97
            # chr()主要用来表示ascii码对应的字符他的输入时数字，可以用十进制，也可以用十六进制 chr(97) = 'a'
            tempData = data[i] ^ ord(IMAGE_KEY[i % len(IMAGE_KEY)])
            #data[i] = tempData
            newData[i] = tempData
            # print("i=",i,",dataLen=",dataLen,"data=",data[i],"newData=",newData[i])

        # 另存为
        # with open(fullpath+".copy","wb") as fp1:
        #   fp1.write(newData)
        #   fp1.flush()
        # 保存到自己
        fp.seek(0)
        fp.write(newData)
        fp.flush()


def png2Jpg(path, file):
    filePath = path + "/" + file
    newFilePath = filePath.replace(".png", ".jpg")
    file_helper.move_file(filePath, newFilePath)


def temp(path, recursive=False):
    # 图片处理的一些列操作 后缀.webp改成.png

    # 遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path, True).walk(optionJSRes5)
    # 移除智图留下的残余文件
    file_helper.remove_dir(path+"/zhitu-des")
    # 加密图片
    print("开始加密图片文件...")
    # 临时文件加密
    file_helper.Diskwalk(path, recursive).walk(encFile)
    print("加密图片文件完成")


def main(path):
    # 图片处理的一些列操作 后缀.webp改成.png

    # 移除默认图片
    file_helper.remove_dir(path+"/res1/Default")
    # 遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path+"/res1", True).walk(optionJSRes5)
    # 移除智图留下的残余文件
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/platform/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/fishs/zhitu-des");
    # 加密图片
    print("开始加密图片文件...")
    file_helper.Diskwalk(path+"/res", True).walk(encFile)
    print("加密图片文件完成")


def enc_jss(path):
    print("开始加密jsc文件...")
    file_helper.Diskwalk(path, True).walk(encFile)
    print("完成加密jsc文件...")


def lailaifish_manifest_gen(dir,version, force, test, urlCDN, urlVer):
    # 生成捕鱼更新包 manifest
    # 必须是已经加密过的jsc和图片资源

    if not test:
        urlVer = urlVer or "https://fanyu123.com/bao/ver/game/"
        fish_hotupdate.createManifestEx(urlCDN,
                         urlVer,
                         dir+"frameworks/runtime-src/proj.win32/Release.win32/Resources",
                         dir,
                         "update", version, force)  # "1.0.8"
    else:
        urlCDN = urlCDN or "https://www.fanyu123.cn/ver3/game/"
        fish_hotupdate.createManifestEx(urlCDN,
                         "https://www.fanyu123.cn/ver3/game/",
                         dir+"frameworks/runtime-src/proj.win32/Release.win32/Resources",
                         dir,
                         "update", version, force)  # "1.0.8"

def productGen(ver, dir, urlCDN, urlVer, isTest=True, onlyVer=True):
    version = ver
    projectDir = dir

    # 打包整个项目
    file_helper.write_str_to_file(projectDir+"src/ver.js", """
var Ver = {
    version: """+repr(version)+""",//auto write by python
    test: """+(str(isTest).lower())+"""
};
    """)
    print("Write ver.js")
    if onlyVer:
        return

    # enc_jss("D:/glp/Github/fishjs/third_part/jsc/src")
    enc_jss(projectDir+"third_part/jsc/src")
    file_helper.remove_dir(projectDir+"third_part/jsc_ios/src")
    file_helper.copy_dir(projectDir+"third_part/jsc/src",
                         projectDir+"third_part/jsc_ios/src")
    file_helper.remove_file(
        projectDir+"/third_part/jsc_ios/src/app.jsc")  # ios目录不需要这个文件

    # release路径js替换成jsc
    file_helper.remove_dir(
        projectDir+"frameworks/runtime-src/proj.win32/Release.win32/Resources/script")
    file_helper.remove_dir(
        projectDir+"frameworks/runtime-src/proj.win32/Release.win32/Resources/src")
    try:
        file_helper.remove_file(
            projectDir+"frameworks/runtime-src/proj.win32/Release.win32/Resources/main.js")
    except Exception as e:
        pass
    try:
        file_helper.remove_file(
            projectDir+"frameworks/runtime-src/proj.win32/Release.win32/Resources/main_ios.js")
    except Exception as e:
        pass
    file_helper.copy_dir(projectDir+"third_part/jsc/script", projectDir +
                         "frameworks/runtime-src/proj.win32/Release.win32/Resources/script")
    file_helper.copy_dir(projectDir+"third_part/jsc/src", projectDir +
                         "frameworks/runtime-src/proj.win32/Release.win32/Resources/src")

    print(version+"更新包生成。。。")
    # 然后执行manifest生成脚本
    lailaifish_manifest_gen(dir,version, True, isTest, urlCDN, urlVer)


def publish():
    # 第一步更改版本号，生成，版本文件，
    # 第二步VS编译jsc文件
    # 第三步再次执行我们的脚本文件
    version = "2.0.2.211"  # 057
    # projectDir = "D:/work/Github/Fish/"  # 打包整个项目
    projectDir = "D:/Github/Fish/"  # 打包整个项目
    urlCDN = "https://fanyu123.com/bao/ver/game/"  # 正式服下载文件的CDN服务器
    urlVer = "https://fanyu123.com/bao/ver/game/"
    isTest = False
    isOnlyVer = False # True#

    if isTest:
        urlCDN = "https://www.fanyu123.cn/ver3/game/"
        urlVer = "https://www.fanyu123.cn/ver3/game/"
    if isOnlyVer:
        productGen(version, projectDir, urlCDN, None, isTest)
        print("完成。。。",version,"Test=",isTest,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        print("移除之前的更新文件中。。。")
        work_dir = projectDir+"frameworks/runtime-src/proj.win32/Release.win32/"
        file_helper.remove_dir(work_dir+"game")
        productGen(version, projectDir, urlCDN, urlCDN, isTest, False)

        print("移动热更新文件中。。。")
        file_helper.make_dirs(work_dir+"game/update")
        file_helper.move_file(work_dir+"Resources/res/manifest/project_platform.manifest",
                              work_dir+"game/project_platform.manifest")
        file_helper.move_file(work_dir+"Resources/res/manifest/version_platform.manifest",
                              work_dir+"game/version_platform.manifest")
        file_helper.move_file(work_dir+"Resources/project.json",work_dir+"game/update/project.json")
        file_helper.move_dir(work_dir+"Resources/res",work_dir+"game/update/res")
        file_helper.move_dir(work_dir+"Resources/script",work_dir+"game/update/script")
        file_helper.move_dir(work_dir+"Resources/src",work_dir+"game/update/src")
        print("完成。。。",version,"Test=",isTest,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

if __name__ == '__main__':
    # 以后路径统一使用 '/ 请勿使用 '\\'

    # 运行一次是加密，运行第二次是解密
    IMAGE_KEY = "aaazhejiangfanyu2018"  # 主包加密
    # IMAGE_KEY = "spzhejiangfanyu2018" #sp渠道加密

    # main("D:/glp/GitHub/Fish2")
    # 加密增加的图片文件
    # temp("D:/work/UI/temp",False);#是否遍历子目录
    publish()
    # 编译工程 最后一步，加密jsc，跟苹果斗智斗勇
    # enc_jss("D:/glp/Github/Fish2/third_part/jsc/1")#打包单独的jsc
    # enc_jss("D:/glp/Github/Fish2/frameworks/runtime-src/proj.win32/Release.win32/jsc")

    #测试异或
    # print(ord('F'),ord('y'),0x27^ord('F'),0x5c^ord('y'))
    # print("{0:x} {1:x}".format(0x61^ord('F'),0x23^ord('y')))
    # print("{0:x}".format(16))
