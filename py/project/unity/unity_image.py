import file_helper
import os
import sys
# pip install Pillow
from PIL import Image
from xml.etree import ElementTree
import math

import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")


def simple_make_dirs(outfile, is_file=True):
    try:
        if is_file:
            pos1 = outfile.rfind("/")
            pos2 = outfile.rfind("\\")
            pos = max(pos1, pos2)
            os.makedirs(outfile[0:pos])
        else:
            os.makedirs(outfile)
    except FileExistsError:
        pass


def parseElements(path, file_path):
    if(not file_path.endswith(".atlas")):
        return
    print(path, file_path)
    full_path = path+"/"+file_path
    with open(full_path, "rb") as plist_file:
        content = plist_file.read().decode("utf-8")

        # root = ElementTree.fromstring(content.decode("utf-8"))
        contents = content.splitlines(False)
        # print(contents)

        atlass = []
        contents_index = []
        include_img_count = 0
        for i in range(0, len(contents)):
            # print(i,contents[i],contents[i]=="")
            if(contents[i] == ""):
                atlas = {"file": contents[i+1], "start": i+1, "end": i+1}
                atlass_len = len(atlass)-1
                if(atlass_len >= 0):  # 修改前值
                    atlass[atlass_len]["end"] = i
                atlass.append(atlas)
                contents_index.append(i)

        print(len(contents_index))
        # if(len(contents_index)<2):#修改前值
        atlass[len(atlass)-1]["end"] = len(contents)
        print(contents_index)
        print(atlass)
        # return

        for i in range(len(atlass)):
            atlas = atlass[i]
            png_filename = path + "/" + atlas["file"]
            # print(png_filename)
            # continue
            big_image = Image.open(png_filename)
            # print("big_image = "+str(big_image))

            print(i, atlas["start"], atlas["end"])

            for j in range(atlas["start"]+5, atlas["end"], 7):

                item_name = contents[j]
                item_name_num_shi = item_name[-2:]
                item_name_num_ge = item_name[-1:]
                if item_name_num_ge.isdigit() and (not item_name_num_shi.isdigit()):
                    item_name = item_name[:-1]+"0"+item_name_num_ge

                # print("item_name=",item_name)
                # continue

                item_rotate = contents[j+1] == "  rotate: true"

                pos_str = contents[j+2]
                pos_comma = pos_str.index(",")
                item_x = int(pos_str[5:pos_comma])
                item_y = int(pos_str[pos_comma+1:])

                pos_str = contents[j+3]
                # print("pos_str=",pos_str)
                pos_comma = pos_str.index(",")
                item_w = int(pos_str[7:pos_comma])
                item_h = int(pos_str[pos_comma+1:])

                pos_str = contents[j+4]
                pos_comma = pos_str.index(",")
                item_orig_w = int(pos_str[7:pos_comma])
                item_orig_h = int(pos_str[pos_comma+1:])

                pos_str = contents[j+5]
                pos_comma = pos_str.index(",")
                item_offset_x = int(pos_str[9:pos_comma])
                item_offset_y = int(pos_str[pos_comma+1:])

                item_detail = {
                    "rotate": item_rotate,
                    "x": item_x,  # 图片在大图中的位置x
                    "y": item_y,  # 图片在大图中的位置y
                    "w": item_w,  # 图片在大图中的大小w
                    "h": item_h,  # 图片在大图中的大小h
                    "orig_w": item_orig_w,  # 图片原始大小w
                    "orig_h": item_orig_h,  # 图片原始大小h
                    "offset_x": item_offset_x,  # 图片在大图中偏移x
                    "offset_y": item_offset_y,  # 图片在大图中偏移y
                }
                # print(item_detail)
                # continue

                k = item_name+".png"
                print("key = ", k)
                # 第一步取出图片在大图中大小位置
                rectlist = [item_x, item_y, item_w,
                            item_h]  # to_list(v['frame'])

                width = item_h if item_rotate else item_w
                height = item_w if item_rotate else item_h
                box = (  # 元组
                    item_x,
                    item_y,
                    item_x + width,
                    item_y + height,
                )
                print("box=", box)
                # [ int(x) for x in to_list(v['sourceSize']) ]
                sizelist = [item_orig_w, item_orig_h]
                # 第二部，复制指定区域的图片，保存到临时目录文件
                img_rect_on_big = big_image.crop(box)

                print("original img_rect_on_big=", img_rect_on_big)
                # img_rect_on_big.save(file_path+"/temp1/"+k);
                if item_rotate:
                    #print("rotate img_rect_on_big")
                    img_rect_on_big = img_rect_on_big.rotate(
                        -90, Image.NEAREST, True)
                    print("rotate -90 img_rect_on_big=", img_rect_on_big)

                temp_path = path+"/temp/" + k
                print("temp_path = ", temp_path)
                # if not os.path.isdir(temp_path):
                simple_make_dirs(temp_path)
                img_rect_on_big.save(temp_path)  # 保存临时裁剪的原文件

                # 创建一张指定大小的PNG，RGBA模式
                result_image = Image.new('RGBA', sizelist)
                # [ int(x) for x in to_list(v['offset']) ]
                rect_offset = [item_offset_x, item_offset_y]
                offset_x = rect_offset[0]
                offset_y = rect_offset[1]
                print("rect_offset = ", rect_offset)

                # print("result_box = ",result_box)
                result_box_offset = [0, 0, 0, 0]
                # + int((item_orig_w-item_w)/2)
                result_box_offset[0] = offset_x
                # + int((item_orig_h-item_h)/2)
                result_box_offset[1] = offset_y

                result_box_offset[2] = result_box_offset[0] + item_w
                result_box_offset[3] = result_box_offset[1] + item_h

                print("result_box_offset = ", result_box_offset)

                # if(v.get('sourceColorRect')):
                #     result_box_sec = [ int(x) for x in to_list(v['sourceColorRect']) ]
                #     result_box_sec[2] += result_box_sec[0]
                #     result_box_sec[3] += result_box_sec[1]
                #     print("result_box_sec = ",result_box_sec)
                #     #result_image.paste(img_rect_on_big,result_box_sec)

                #result_image.paste(img_rect_on_big, result_box)
                result_image.paste(img_rect_on_big, result_box_offset)

                outfile = path+"/"+k
                simple_make_dirs(outfile)
                print("make out file=", outfile)
                print("*"*100)
                result_image.save(outfile)


def parseAtlasPath(dir):
    print("开始...")
    file_helper.Diskwalk(dir, True).walk(parseElements)
    print("完成!!!")


if __name__ == '__main__':
    # for i in range(1,3):
    # 	print(i)
    # parseElements("D:/glp/Github/PL/py/ztest/unity/iimg","shz_shiqian.atlas")

    parseAtlasPath("D:/glp/Github/PL/py/ztest/unity/img")
