#!python 3.6


from xml.etree import ElementTree
import os

# 当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
# 然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
# 正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper

def optionRename(path, file):
    fullpath = file_helper.join(path, file)

    pos_end = file.find(".png")
    number = int(file[pos_end-2:pos_end])
    number += 1
    str_number = "{:02d}".format(number)
    # print("str_number=",str_number);

    new_path = file[0:pos_end-2]+str_number+".png"
    print(file, ">>", new_path)
    new_full_path = file_helper.join(path, "new/"+new_path)
    # print("new_full_path=",new_full_path)
    file_helper.copy_file(fullpath, new_full_path)


def optionRenameFishId(path, file):
    fullpath = file_helper.join(path, file)

    new_file = file.replace("fish_27", "fish_32")
    new_path = file_helper.join(path, new_file)
    print(fullpath, ">>", new_path)
    file_helper.move_file(fullpath, new_path)


def optionJSRes0(path, file):
    name = file.replace(".", "_")
    ext_file = file.replace(".png", "")

    path_new = path[path.find("res"):].replace("/", "/")+"/"
    is_png = False
    if("_png" in name):
        is_png = True

    if(is_png):
        # games/fish ; platform
        print(name+": '"+path_new+ext_file+"' + cfgImageExt,")
    else:
        print(name+": '"+path_new+ext_file+"',")  # games/fish ; platform


def optionJSResLobby(path, file):
    optionJSRes1(path, file)


def optionJSResFish(path, file):
    optionJSRes1(path, file, True)


def optionJSRes1(path, file, inFish=False):
    if not inFish:
        if(file.startswith("particle_") or file.startswith("Plist")):
            return
        if "ignore" in path or path.endswith("_ignore"):
            return
    else:
        if(not file.endswith(".png") or file.startswith("Plist")):
            return

    path_new = path[path.find("res"):].replace("/", "/")+"/"
    # print(path_new)

    name = file.replace(".", "_")
    ext_file = file.replace(".png", "")

    is_png = False
    if("_png" in name):
        is_png = True

    if("_webp" in name):
        is_png = True
        name = name.replace("_webp", "_png")
        ext_file = file.replace(".webp", "")

    if(is_png):
        # games/fish ; platform
        print(name+": '"+path_new+ext_file+"' + cfgImageExt,")
    else:
        print(name+": '"+path_new+ext_file+"',")  # games/fish ; platform


def optionJSRes1_(path, file):
    name = file.replace(".", "_")
    name = name.replace("m4a", "ogg")

    ext_file = file.replace(".m4a", "")
    print("music_"+name+": 'res/games/fish/ogg/"+ext_file +
          "' + cfgAudioExt,")  # games/fish ; platform


def optionJSRes2(path, file):
    name = file.replace(".", "_")

    name = file.replace(".png", "' + cfgImageExt")
    if name.endswith("+ cfgImageExt"):
        print("'res/games/fish/fishs/"+name+",")
    else:
        print("'res/games/fish/fishs/"+name+"',")


def optionJSRes3(path, file):
    # if(file.find(".png") != -1):
    name = file.replace(".", "_")

    if("_webp" in name):
        name = name.replace("_webp", "_png")
    print(name+": 'res/games/fish/"+file+"',")

    if("ignore" in path):
        return
    path_new = path[path.find("res"):].replace("/", "/")+"/"
    # print(path_new)

    name = file.replace(".", "_")
    ext_file = file.replace(".png", "")

    is_png = False
    if("_png" in name):
        is_png = True

    if("_webp" in name):
        is_png = True
        name = name.replace("_webp", "_png")
        ext_file = file.replace(".webp", "")

    if(is_png):
        # games/fish ; platform
        print(name+": '"+path_new+ext_file+"' + cfgImageExt,")
    else:
        print(name+": '"+path_new+ext_file+"',")  # games/fish ; platform

# 修改plist文件的纹理为png->webp


def optionJSRes4(path, file):
    plist_filename = path+"/"+file
    print(plist_filename)

    if("webp" in path):
        return

    if(".plist" in file and file.startswith("Plist")):
        tree = ElementTree.parse(plist_filename)
        root = tree.getroot()
        #root = ElementTree.fromstring(content.decode("utf-8"));
        print(root.tag, root.attrib, "text=", root.text)

        # for child in root:
        # 	print(child.tag, child.attrib,"text=",child.text);

        # for cc in child:
        # print(cc.tag, cc.attrib,"text=",cc.text);
        # cc = child[2];
        # print(cc.tag, cc.attrib,"text=",cc.text);

        child = root[0]

        cc = child[3]
        print(cc.tag, cc.attrib, "text=", cc.text)

        textureFileName = cc[3]
        #print("textureFileName:",textureFileName.tag, textureFileName.attrib,"text=",textureFileName.text,type(textureFileName.text));
        textureFileName.text = textureFileName.text.replace(".png", ".webp")

        realTextureFileName = cc[5]
        #print(realTextureFileName.tag, realTextureFileName.attrib,"text=",realTextureFileName.text);
        realTextureFileName.text = realTextureFileName.text.replace(
            ".png", ".webp")
        #print("realTextureFileName:",realTextureFileName.tag, realTextureFileName.attrib,"text=",realTextureFileName.text);

        newFilePath = path+"/webp"
        try:
            os.mkdir(newFilePath)
        except FileExistsError:  # 异常捕获
            pass

        tree.write(newFilePath+"/"+file)


def optionCPP(path, file):
    if file.find(".c") != -1 or file.find(".cpp") != -1:
        print("../../../Classes/app/"+file)


def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d


def parsePlistImage(path, file):
    fullpath = path+"/"+file

    with open(fullpath, "rb") as plist_file:
        content = plist_file.read()
        root = ElementTree.fromstring(content.decode("utf-8"))

        # print(root)
        plist_dict = tree_to_dict(root[0])
        # print(plist_dict)

        for k, v in plist_dict['frames'].items():
            # print("key = ",k,type(k))
            pos = k.rfind("/")
            name = k[pos+1:]
            name = name.replace(".", "_")
            name = name.replace("res1", "res")
            print(name+": '"+k+"',")
            # YZ3_png: 'res/games/fish/YZ3' + cfgImageExt


if __name__ == '__main__':
    # 以后路径统一使用 '/ 请勿使用 '\\'

    # print(file_helper)
    # 遍历目录改文件名
    # C:\Users\JJ\Desktop\LF_boss_fish_PList.Dir
    #total = file_helper.Diskwalk("C:/Users/JJ/Desktop/LF_boss_fish_PList.Dir").walk(optionRename);
    # file = total[0]
    # path = total[1]

    # C++文件列表
    # file_helper.Diskwalk("D:/glp/GitHub/LongConnectionTCP/src/Classes/app",False).walk(optionCPP);
    # 平台 图片文件
    file_helper.Diskwalk("D:/work/GitHub/Fish/res/platform").walk(optionJSResLobby);
    # 音频文件
    # file_helper.Diskwalk("D:/glp/GitHub/fishjs/res/games/fish/ogg",False).walk(optionJSRes1_);
    # 捕鱼 游动plist文件
    # file_helper.Diskwalk("D:/glp/GitHub/Fish2/res/games/fish/fishs",False).walk(optionJSRes2);
    # 捕鱼图片文件
    # file_helper.Diskwalk("D:/work/GitHub/Fish/res/games/fish",True).walk(optionJSResFish)
    #英雄传
    # file_helper.Diskwalk("D:/work/Github/Fish2/res/games/shz",True).walk(optionJSResFish)
    # 粒子文件
    # file_helper.Diskwalk("D:/glp/GitHub/Fish2/res/games/fish/particle",False).walk(optionJSRes0);

    # 鱼图片文件名字修改
    # file_helper.Diskwalk("D:/glp/work/UI/20170919/package/fishs",False).walk(optionRenameFishId);

    # 捕鱼合图
    # parsePlistImage("D:/glp/Github/fishjs/res1/games/fish","PlistFish01.plist")
    # 大厅合图
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform01.plist")
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform02.plist")
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform03.plist")
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform04.plist")
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform05.plist")
    # parsePlistImage("D:/glp/Github/fishjs/res1/platform",
    #                 "PlistPlatform06.plist")

    def water_name(path, file):
        print(path, file)
        os.rename(path+"/"+file, path+"/"+"water_"+file)

    # file_helper.Diskwalk("C:/Users/JJ/Desktop/png",False).walk(water_name);
