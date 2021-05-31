import os
import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper
import fishgame.fish_hotupdate


def buildXXVersion():
    # 第一步更改版本号，生成，版本文件，
    # 第二步VS编译jsc文件
    # 第三步再次执行我们的脚本文件
    version = "1.0.0.1"  # 057
    projectDir = "D:/work/Github/CreatorUpdateDemo/build/jsb-link/"  # 打包整个项目
    urlCDN = "http://192.168.0.168/ver/" #"https://fanyu123.com/bao/ver/game/"  # 正式服下载文件的CDN服务器
    urlVer = "https://fanyu123.com/bao/ver/game/"

    nginxDir = "D:/program/nginx-1.13.12/html/ver/update/"
    fishgame.fish_hotupdate.creatManifestForCreator(version,urlCDN,nginxDir,"update")
    print("完成。。。",version)

if __name__ == '__main__':
	buildXXVersion()
