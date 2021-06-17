import os
from zipfile import ZipFile

def get_dir_files(dir):
    files = []
    allChileFiles = []
    for dirpath, dirnames, filenames in os.walk(dir):
        print("dirpath=",dirpath)
        # print("dirnames=",dirnames)
        # print("filenames=",filenames)

        for file in filenames:
            dirpath = dirpath.replace("\\", "/")

            fullPath = dirpath+"/"+file
            
            files.append(file)
            fullpath = dirpath+"/"+file #os.path.join(dirpath, file)
            allChileFiles.append(fullpath)
    # return files
    return allChileFiles

def zip_dir(zipFile,dir):
    allchildren = get_dir_files(dir)
    for i in range(len(allchildren)):
        zipFile.write(allchildren[i])


def fish_zip_main(first,dir):
    '''
    @first 是否第一次上传到服务器
    '''
    with ZipFile('fish.zip', 'w') as myzip:
        if first:
            #总体配置文件
            zip_dir(myzip,'conf') #@注意：具体环境更换对应环境的配置文件；目前是龙珠版生产环境
            #捕鱼配置文件
            zip_dir(myzip,'fishCfg') #@注意：具体环境更换对应环境的配置文件；目前是龙珠版生产环境

            #源代码
            zip_dir(myzip,'3rd')
            zip_dir(myzip,'lualib')
            zip_dir(myzip,'skynet')
            #没有后缀会当成目录，我们这里指定绝对路径
            myzip.write(dir+"Makefile","Makefile")

            #维护辅助命令
            myzip.write('fish-server-cmd.py')

            #shell脚本
            myzip.write('build-skynet-main.sh')
            myzip.write('sh-build-linux.sh')
            myzip.write('sh-center.sh')
            myzip.write('sh-stop.sh')
        
        #常用的service
        zip_dir(myzip,'service')
        

def fish_zip_test():
    #压缩文件到压缩包
    with ZipFile('test.zip', 'w') as myzip:
        myzip.write('coin.py') #压缩文件
        zip_dir(myzip,'test') #压缩子目录

    #解压缩到指定目录
    # myzip.extractall('test')

if __name__ == '__main__':
    #@注意：win32直接双击执行即可，如果用cmd需要cd到对应的目录

    # print(os.path.join("a","b"))
    # fish_zip_test()
    fish_zip_main(True,"D:/Github/fishing_server/skynet_lailai/")

    #解压缩命令unzip fihs.zip
    #chmod +xxx ./build-skynet-main.sh
