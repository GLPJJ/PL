#!python 3.4
# 遍历cocos的plist文件

import os
import sys
# pip install Pillow
from PIL import Image
from xml.etree import ElementTree
import math


def simple_make_dirs(outfile, is_file=True):
    try:
        if is_file:
            pos1 = outfile.rfind("/")
            pos2 = outfile.rfind("\\")
            pos = max(pos1, pos2)
            os.makedirs(outfile[0:pos])  # 只能创建目录
        else:
            os.makedirs(outfile)
    except FileExistsError:
        pass


def endWith(s, *endstring):
    array = map(s.endswith, endstring)
    if True in array:
        return True
    else:
        return False

# Get the all files & directories in the specified directory (path).


def get_recursive_file_list(path):
    current_files = os.listdir(path)
    all_files = []
    for file_name in current_files:
        full_file_name = os.path.join(path, file_name)
        if endWith(full_file_name, '.plist'):
            full_file_name = full_file_name.replace('.plist', '')
            all_files.append(full_file_name)

        if os.path.isdir(full_file_name):
            next_level_files = get_recursive_file_list(full_file_name)
            all_files.extend(next_level_files)
    return all_files


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


def gen_png_from_plist(plist_filename, png_filename):
    file_path = plist_filename.replace('.plist', '')
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    big_image = Image.open(png_filename)

    print("big_image = "+str(big_image))

    root = ""

    print(sys.getdefaultencoding())
    # import importlib
    # sys.setdefaultencoding("utf-8")
    # importlib.reload(sys)

    with open(plist_filename, "rb") as plist_file:
        content = plist_file.read()
        root = ElementTree.fromstring(content.decode("utf-8"))

    #root = ElementTree.fromstring(open(plist_filename, 'r').read())
    print("root=", root)
    plist_dict = tree_to_dict(root[0])

    def to_list(x): return x.replace('{', '').replace('}', '').split(',')
    for k, v in plist_dict['frames'].items():
        print("key = ", k)
        rectlist = to_list(v['frame'])

        original_width = int(rectlist[2])
        original_height = int(rectlist[3])

        print("rectlist = ", rectlist, "rotated=", v['rotated'])
        width = original_height if v['rotated'] else original_width
        height = original_width if v['rotated'] else original_height
        box = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
        )
        print("box=", box)
        sizelist = [int(x) for x in to_list(v['sourceSize'])]
        rect_on_big = big_image.crop(box)

        print("original rect_on_big=", rect_on_big)
        # rect_on_big.save(file_path+"/temp1/"+k);
        if v['rotated']:
            #print("rotate rect_on_big")
            rect_on_big = rect_on_big.rotate(90, Image.NEAREST, True)
            print("rotate 90 rect_on_big=", rect_on_big)

        temp_path = file_path+"/temp/"+k
        #print("temp_path = ",temp_path)
        # if not os.path.isdir(temp_path):
        simple_make_dirs(temp_path)
        rect_on_big.save(temp_path)  # 保存临时裁剪的原文件

        # 创建一张指定大小的PNG，RGBA模式
        result_image = Image.new('RGBA', sizelist)
        result_box_template = [
            int((sizelist[0] - original_width)/2),
            math.ceil((sizelist[1] - original_height)/2),
            0,
            0
        ]

        result_box = result_box_template[:]
        result_box[2] = result_box[0] + original_width
        result_box[3] = result_box[1] + original_height
        print("sizelist ="+str(sizelist))

        rect_offset = [int(x) for x in to_list(v['offset'])]
        offset_x = rect_offset[0]
        offset_y = rect_offset[1]
        print("rect_offset = ", rect_offset)

        print("result_box = ", result_box)
        result_box_offset = result_box_template[:]
        result_box_offset[0] += offset_x
        result_box_offset[2] = result_box_offset[0] + original_width

        result_box_offset[1] -= offset_y
        result_box_offset[3] = result_box_offset[1] + original_height

        print("result_box_offset = ", result_box_offset)

        if(v.get('sourceColorRect')):
            result_box_sec = [int(x) for x in to_list(v['sourceColorRect'])]
            result_box_sec[2] += result_box_sec[0]
            result_box_sec[3] += result_box_sec[1]
            print("result_box_sec = ", result_box_sec)
            # result_image.paste(rect_on_big,result_box_sec)

        #result_image.paste(rect_on_big, result_box)
        result_image.paste(rect_on_big, result_box_offset)

        outfile = file_path+"/"+k
        simple_make_dirs(outfile)
        print("make out file=", outfile)
        print("*"*100)
        result_image.save(outfile)


if __name__ == '__main__':
    # currtenPath = "C:/Users/JJ/Desktop/gimp"#os.getcwd()
    #currtenPath = "C:\\Users\\JJ\\Desktop\\images\\extern"
    currtenPath = "C:\\Users\\JJ\\Desktop\\UI"
    allPlistArray = get_recursive_file_list(currtenPath)
    print("allPlistArray = ", allPlistArray)
    for plist in allPlistArray:
        print("plist = "+plist+".plist")
        filename = plist
        plist_filename = filename + '.plist'
        png_filename = filename + '.png'
        if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
            gen_png_from_plist(plist_filename, png_filename)
        else:
            print("make sure you have boith plist and png files in the same directory")
