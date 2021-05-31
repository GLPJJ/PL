import json
import os
# 当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
# 然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
# 正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper
"""
本文件是依赖python3
"""


def main(src_dir, dst_dir):
    new_dir = src_dir+"_hotupdate"
    update_dir = src_dir+"/../update"

    print(">> 删除原来的热更新目录")
    file_helper.remove_dir(new_dir)
    print(">> 创建新的目录")
    file_helper.make_dirs(new_dir)

    arra_a1 = []
    arra_b1 = []

    def src_func(dirpath, file):
        arra_a1.append(file_helper.join(dirpath[len(src_dir):], file))

    def dst_func(dirpath, file):
        arra_b1.append(file_helper.join(dirpath[len(dst_dir):], file))

    arra_temp_a1, arra_a2 = file_helper.Diskwalk(src_dir).walk(src_func)
    arra_temp_b1, arra_b2 = file_helper.Diskwalk(dst_dir).walk(dst_func)

    # print(arra_temp_a1)
    # # print("*"*100)
    # # print(arra_a1)
    # # print("*"*100)
    # # print(arra_a2)
    # # return
    # print("*"*100)
    # print(arra_b1)
    # return

    arra_c = []
    for i, b1 in enumerate(arra_b1):
        # print(">>",i,b1)
        # filterLst = [b1.endswith(x) for x in [".lib",".exp",".gitignore",".pdb",".exe",".dll"]];
        # if True in filterLst:
        # 	continue

        filter = False
        for x in [".lib", ".exp", ".gitignore", ".pdb", ".exe", ".dll", ".zip", "main.js", ".mp3", ".bat", ".jsc", ".manifest"]:
            if b1.endswith(x):
                filter = True
                break

        if filter:
            # print("continue")
            continue

        file_b = arra_b2[i]
        if b1 in arra_a1:
            file_a = arra_a2[arra_a1.index(b1)]

            md5_a = file_helper.md5_file(file_a)
            md5_b = file_helper.md5_file(file_b)
            # print(file_a ," == " ,file_b)
            # print(md5_a ," == " ,md5_b ,md5_a == md5_b)

            if md5_a != md5_b:
                print(">> Modi append file ", file_b)
                print(file_a, " <==> ", file_b)
                print(md5_a, " == ", md5_b, md5_a == md5_b)
                arra_c.append(file_b)
        else:
            print(">> New  append file ", file_b)
            arra_c.append(file_b)

    # print(">> 源文件展示")
    # print(arra_c)

    arra_c_to = [x.replace(dst_dir, new_dir) for x in arra_c]
    # print(">> 目标文件展示")
    # print(arra_c_to)

    # return
    print(">> 开始拷贝文件")
    for i, v in enumerate(arra_c):
        print(">>", i, v, arra_c_to[i])
        file_helper.copy_file(v, arra_c_to[i])

    print(">> 移除game_2")
    file_helper.remove_dir(new_dir+"/src/game/game_2_hide")
    print(">> 移除update目录")
    file_helper.remove_dir(new_dir+"/../update")

    print(">> 拷贝资源到热更新目录update")

    def copy_res_no_js(dirpath, file):
        # print("*"*100)
        # print(dirpath,file)
        if dirpath.startswith(new_dir+"/src"):  # js 不用拷贝
            pass
        elif dirpath.startswith(new_dir+"/script"):  # js 不用拷贝
            pass
        elif file == "jscompile.bat":
            pass
        else:  # 资源拷贝
            dirpath_new = dirpath.replace(new_dir, update_dir)
            # print(dirpath_new)
            file_helper.copy_file(file_helper.join(
                dirpath, file), file_helper.join(dirpath_new, file))
    file_helper.Diskwalk(new_dir).walk(copy_res_no_js)
    print(">> 写入JS加密脚本 需要python27")

    text = """	
	echo 当前盘符：%~d0
	echo 当前路径：%cd%
	echo 当前执行命令行：%0
	echo 当前bat文件路径：%~dp0
	echo 当前bat文件短路径：%~sdp0

	%~d0
	cd %~dp0
	cocos jscompile -s . -d ../update
			"""
    jscompile_bat = file_helper.join(new_dir, "jscompile.bat")
    file_helper.write_str_to_file(jscompile_bat, text)
    print(">> 请手动改成python27,并双击", jscompile_bat)

    # js_compile_cmd = "cocos jscompile -s "+new_dir+"/src -d "+new_dir+"/../update"
    # os.system(js_compile_cmd) #cocos 脚本需要python27环境

    print(">> 脚本生成的 update 在上层目录中")
    print(">> 对jsc进行加密")
    print(">> 待脚本执行后，前往update目录，打包成最新版本的zip(当前版本是1.0.7,就是'1.0.7.zip'),这就是我们的更新包了,移除src和res目录")
    print(">> 执行本脚本中的createManifestEx函数，project.mainifest和version.manifest就生成了")


curAssetCnt = 0


def createManifestEx(urlCDN, url, src, dest, update, ver, force, project=True):
    """
        @url 域名地址
        @src 文件release存放位置
        @dest 当前项目地址
        @update 更新版本的搜索路径
        @ver 更新版本
    """
    project_manifest = "project_platform.manifest"
    version_manifest = "version_platform.manifest"

    manifest = {
        "packageUrl": urlCDN,
        "remoteManifestUrl": url+project_manifest,
        "remoteVersionUrl": url+version_manifest,
        "version": ver,
        "assets": {},
        "searchPaths": [update]  # "update"
    }

    def walk_dir(path, file):
        full_path_file = path+"/"+file

        print("walk_dir", path, file)

        if(file == "game.zip" or file == "Release.win32.zip"):
            return
        if(file.endswith(".js.map")):  # 解释文件不记录
            file_helper.remove_file(full_path_file)
            return
        if(file.endswith(".manifest")):  # 配置文件不记录
            return
        if(file.endswith(".lib")):  # 配置文件不记录
            return
        if(file.endswith(".dll")):  # 配置文件不记录
            return
        if(file.endswith(".gitignore")):  # 配置文件不记录
            return
        if(file.endswith(".bat")):  # 配置文件不记录
            return
        if(file.endswith(".pdb")):  # 配置文件不记录
            return
        if(file.endswith(".exp")):  # 配置文件不记录
            return
        if(file.endswith(".exe")):  # 配置文件不记录
            return
        if(file == "main.jsc" or file == "main_ios.jsc"):
            return

        # print(path,file);
        new_path_dir = path[len(src)+1:]
        print(new_path_dir, new_path_dir == "")
        new_path_file = file if new_path_dir == "" else new_path_dir+"/"+file
        print(new_path_file)

        # {"size":7418,"md5":"7551284fcba1c5543c0454526bb8991a"}
        asset = {
            "path": update+"/"+new_path_file,
            "size": file_helper.file_size(full_path_file),
            "md5": file_helper.md5_file(full_path_file,True),
            "compressed": file.endswith(".zip")}
        print(asset)

        manifest["assets"][new_path_file] = asset

    # 遍历目录
    file_helper.Diskwalk(src).walk(walk_dir)

    cur_manifest_file_src = src+"/res/manifest/"+project_manifest
    cur_ver_manifest_file_src = src+"/res/manifest/"+version_manifest
    if project:
        cur_manifest_file_dest = dest+"/res/manifest/"+project_manifest
        cur_main_manifest_file_dest = dest+"/res_main/manifest/"+project_manifest
        # if(force or not file_helper.is_file_exits(cur_manifest_file_src)):

        # 工程目录
        file_helper.write_str_to_file(cur_manifest_file_dest, json.dumps(
            manifest, indent=0, sort_keys=False))
        # git 工程目录
        file_helper.write_str_to_file(cur_main_manifest_file_dest, json.dumps(
            manifest, indent=0, sort_keys=False))
    else:
        cur_manifest_file_src = src+"/../"+project_manifest
        cur_ver_manifest_file_src = src+"/../"+version_manifest

    # Debug目录
    file_helper.write_str_to_file(cur_manifest_file_src, json.dumps(
        manifest, indent=0, sort_keys=False))

    # 版本校验
    del manifest["assets"]
    del manifest["searchPaths"]
    manifest["forceUpdate"] = force
    file_helper.write_str_to_file(cur_ver_manifest_file_src, json.dumps(
        manifest, indent=0, sort_keys=False))

    print("当前项目资源生成完毕："+ver)

def creatManifestForCreator(version, url, src, update):
    """
    @version 新的版本号
    @url 域名地址
    @src 当前项目地址
    @update 更新版本的搜索路径
    """
    manifest = {
        "packageUrl": url,
        "remoteManifestUrl": url+"project.manifest",
        "remoteVersionUrl": url+"version.manifest",
        "version": version,
        "assets": {},
        "searchPaths": []  # "update"
    }

    def walk_dir(path, file):
        full_path_file = path+"/"+file

        if(file.endswith(".js.map")):  # 解释文件不记录
            file_helper.remove_file(full_path_file)
            return
        if(file.endswith(".manifest")):  # 配置文件不记录
            return

        # print(path,file);
        new_path_dir = path[len(src):]
        print(new_path_dir, new_path_dir == "")
        new_path_file = file if new_path_dir == "" else new_path_dir+"/"+file
        print(new_path_file)

        # {"size":7418,"md5":"7551284fcba1c5543c0454526bb8991a"}
        asset = {
            "path": update+"/"+new_path_file,
            "size": file_helper.file_size(full_path_file),
            "md5": file_helper.md5_file(full_path_file),
            "compressed": file.endswith(".zip")}
        print(asset)

        manifest["assets"][new_path_file] = asset

    # 遍历脚本目录
    file_helper.Diskwalk(src+"src").walk(walk_dir)
    # 遍历资源目录
    file_helper.Diskwalk(src+"assets").walk(walk_dir)

    cur_manifest_file_src = src+"assets/main/project.manifest"
    # if(force or not file_helper.is_file_exits(cur_manifest_file_src)):
    # creator 工程目录
    file_helper.write_str_to_file(cur_manifest_file_src, json.dumps(
        manifest, indent=0, sort_keys=False))

    #备份
    file_helper.write_str_to_file(src+"../project.manifest", json.dumps(manifest, indent=0, sort_keys=False))
    del manifest["assets"]
    del manifest["searchPaths"]
    file_helper.write_str_to_file(src+"../version.manifest", json.dumps(manifest, indent=0, sort_keys=False))

    print("当前项目资源生成完毕："+version)

if __name__ == '__main__':
    # 以后路径统一使用 '/ 请勿使用 '\\'

    import sys

    version = "2.0.0.9"
    if len(sys.argv) > 1:
        str_ver = sys.argv[1]
        version = str_ver[str_ver.find("-v=")+3:]

    print(version+"更新包生成。。。")
    # 来来捕鱼更新包配置文件
    # createManifestEx(None,None,
    #      dir+"frameworks/runtime-src/proj.win32/Release.win32/Resources",
    #      dir,"update", version, force)  # "1.0.8"
    creatManifestForCreator("2.0.2.161","http://192.168.0.168/fish/"
        ,"C:/nginx-1.17.10/html/fish/update/","update")

    """
		额。。。有点繁琐，先这样吧。。

		首次运行需要自己创建一个简单的manifest放到工程中

		1 creator构建 把修改的资源发布到目录
		2 运行脚本 读取修改的资源，修改project.manifest的内容
	"""
    # dir_src = "D:/glp/Github/CreatorTest/build/jsb-default"
    # dir_dest = "D:/glp/Github/CreatorTest"
    # package_url = "http://192.168.0.18:8080/CreatorTest/"