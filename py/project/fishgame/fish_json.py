
import json
import os

# 当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
# 然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
# 正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper
import math


def ChangePosition(src_name, out_name, isIphoneX=False, isReverse=False):
    try:
        print(src_name)

        with open(src_name, "r") as file:
            routes = json.load(file)
            # print(routes,type(routes))

            route = routes[0]
            # print(route,type(route))
            # print(route["points"])
            for route in routes:
                for point in route["points"]:
                    if(isReverse):
                        point["x"] = math.floor(point["x"]+560)
                        if(isIphoneX):
                            point["x"] -= 140
                        point["y"] = math.floor(point["y"]+315)
                    else:
                        point["x"] = math.floor(point["x"]-560)
                        if(isIphoneX):
                            point["x"] += 140
                        point["y"] = math.floor(point["y"]-315)

            # print(routes[0],type(routes[0]))

            with open(out_name, "w") as file2:
                json.dump(routes, file2)

    except FileNotFoundError:
        print("not find file=", src_name)
        pass


RESOURCE = "res"
RESOURCEFRAMES = "res_frames"
PUSHCNT = 0
CURGAMERESDIR = ""
USERIMAGEPLIST = False


def printCustom(msg=""):
    print(msg)


def printSpace4(ret_cnt,msg):
    # print(type(msg),len(msg))
    print(" "*((ret_cnt+1)*4)+msg)


def printSpace8(ret_cnt,msg):
    printSpace4(ret_cnt+1,msg)

def needUse(name):
    return name.startswith("use_") or name.endswith("_use")

def getCurRetName(ret_cnt):
    return ret_cnt <= 0 and "ret" or "ret"+str(ret_cnt)
    # return "ret" if ret_cnt <= 0 else "ret"+str(ret_cnt)

def getCurNodeNamePrefix(parent,cur):
    return parent+str(cur)

def getJsonPropName(name,str_parent):
    if(name == str_parent):
        if(needUse(name)):
            name = name[:-4] + "__use"
        else:
            name = name+"_"
    elif name.endswith("_nouse"):
        return "",False

    return name,True

"""
    {
        "AnchorPoint": {
          "ScaleX": 1.0,
          "ScaleY": 0.5
        },
        "Position": {
          "X": -1.91,
          "Y": 65.2554
        },
        "Scale": {
          "ScaleX": 1.0,
          "ScaleY": 1.0
        },
        "RotationSkewX": 20.0,
        "RotationSkewY": 20.0,
        "CColor": {
          "G": 16,
          "B": 32
        },
        "Size": {
          "X": 0.0,
          "Y": 0.0
        },
        "VisibleForFrame": false,
        "Alpha": 200,
        "Name": "Node_1",
        "Children":[],
        "ctype": "SingleNodeObjectData"
    }
"""


def ParseCCSNodeProp(json_content, str_node, cur_cnt, ret_cnt, name_parent, is_node=False, is_text=False
    , has_blend=False, no_color=False, no_size=False,load_as_csj=False):
    if load_as_csj :
        str_node = str_node+".node"
    # print("//"+str_node)

    printSpace8(ret_cnt,str_node+".setCascadeOpacityEnabled(true);");#自身的alpha属性是否影响子类

    # "FlipX": true,
    # "FlipY": true,

    if "FlipX" in json_content:
        printSpace8(ret_cnt,str_node+".setFlippedX(true);")

    if "FlipY" in json_content:
        printSpace8(ret_cnt,str_node+".setFlippedY(true);")

    # 设置颜色混合
    if(has_blend and "BlendFunc" in json_content):
        json_blend = json_content["BlendFunc"]
        blend_src = 1 if "Src" not in json_blend else json_blend["Src"]
        blend_dst = 771 if "Dst" not in json_blend else json_blend["Dst"]
        printSpace8(ret_cnt,str_node+".setBlendFunc(" +
                    str(blend_src)+", "+str(blend_dst)+");")

    # 设置锚点
    if(not is_node and "AnchorPoint" in json_content):
        json_anchor = json_content["AnchorPoint"]
        anchor_x = 0 if "ScaleX" not in json_anchor else json_anchor["ScaleX"]
        anchor_y = 0 if "ScaleY" not in json_anchor else json_anchor["ScaleY"]
        printSpace8(ret_cnt,
            str_node+".setAnchorPoint(cc.p("+str(anchor_x)+", "+str(anchor_y)+"));")

    # 设置位置
    if("Position" in json_content):
        json_position = json_content["Position"]
        position_x = json_position["X"]
        position_y = json_position["Y"]

        if(position_x == 0 and position_y == 0):
            pass
        else:
            printSpace8(ret_cnt,
                str_node+".setPosition(cc.p("+str(position_x)+", "+str(position_y)+"));")
    # 设置缩放
    if("Scale" in json_content):
        json_scale = json_content["Scale"]
        scale_x = json_scale["ScaleX"]
        scale_y = json_scale["ScaleY"]

        if(scale_x == 1 and scale_y == 1):
            pass
        elif(scale_x == scale_y):
            printSpace8(ret_cnt,str_node+".setScale("+str(scale_x)+");")
        else:
            printSpace8(ret_cnt,str_node+".setScaleX("+str(scale_x)+");")
            printSpace8(ret_cnt,str_node+".setScaleY("+str(scale_y)+");")
    # 设置旋转角度
    if("RotationSkewX" in json_content):
        printSpace8(ret_cnt,str_node+".setRotationX(" +
                    str(json_content["RotationSkewX"])+");")
    if("RotationSkewY" in json_content):
        printSpace8(ret_cnt,str_node+".setRotationY(" +
                    str(json_content["RotationSkewY"])+");")

    if(not no_color and "CColor" in json_content):
        json_color = json_content["CColor"]  # 设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"]
        if("G" in json_color):
            g = json_color["G"]
        if("B" in json_color):
            b = json_color["B"]

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            if(is_text):  # 如果是文字节点，则设置文字颜色
                printSpace8(ret_cnt,str_node+".setTextColor(cc.color(" +
                            str(r)+", "+str(g)+", "+str(b)+"));")
            else:
                printSpace8(ret_cnt,
                    str_node+".setColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));")

    if("VisibleForFrame" in json_content):  # 设置可见性
        printSpace8(ret_cnt,str_node+".setVisible(false);")

    if("Alpha" in json_content):  # 设置alpha值
        printSpace8(ret_cnt,str_node+".setOpacity("+str(json_content["Alpha"])+");")

    if(is_node or is_text):
        no_size = True
    if(not no_size and "Size" in json_content):  # 设置非节点的内容大小
        json_size = json_content["Size"]
        printSpace8(ret_cnt,str_node+".setContentSize(cc.size(" +
                    str(json_size["X"])+", "+str(json_size["Y"])+"));")

    # 解析子节点
    if("Children" in json_content):
        cur_cnt = ParseCCSChildren(
            json_content["Children"], str_node, cur_cnt, ret_cnt, name_parent)
    return cur_cnt


def ParseCCSNode(json_content, str_parent, cur_cnt, ret_cnt, name_parent, str_node=None):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    if(str_node):
        name = str_node

    printSpace8(ret_cnt,"var "+name+" = new cc.Node();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    else:
        printSpace8(ret_cnt,"parent.addChild("+name+");")
        printSpace8(ret_cnt,name+".setPosition(pos);")
    if(needUse(name)):
        # global PUSHCNT;#申明是全局变量

        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")

        if name.startswith("FileNode_"):
            cur_cnt = 1
        else:
            cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")
    if(name.startswith("box_")):
        printSpace8(ret_cnt,name+".setName('box');")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent,True)


"""
    "FileData": {
      "Type": "Normal",
      "Path": "platform/btn_sure.png",
      "Plist": ""
    },
"""


def ParseCCSSpriteProp(json_content, name=None):
    if(not name):
        name = "FileData"
    if name not in json_content:
        return "", False 

    # 设置纹理
    str_sprite = json_content[name]["Path"]

    # printCustom(str_sprite_name)
    is_frame = False
    if json_content[name]["Type"] == "MarkedSubImage":#plist图片
        is_frame = True
    elif json_content[name]["Type"] == "Default":
        str_sprite = ""

    if str_sprite == "":
        return "", is_frame
    elif not is_frame:
        return "res/"+str_sprite, is_frame
    else:
        return str_sprite, is_frame
        

def ParseCCSBtn(json_content, str_parent, str_node, cur_cnt, ret_cnt, name_parent):
    printSpace8(ret_cnt,"var "+str_node+" = new ccui.Button();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+str_node+");")
    if(needUse(str_node)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,str_node+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+str_node+");")

    # 设置按钮属性
    printSpace8(ret_cnt,
        str_node+".setPressedActionEnabled(true);")#启用点击动作,只有当设置了按下的图片才有效果
    printSpace8(ret_cnt,str_node+".setZoomScale(-0.1);")#点击缩小,有点击就缩小，不用则置为0
    printSpace8(ret_cnt,str_node+".setTitleFontName(res.default_font);")
    printSpace8(ret_cnt,str_node+".setTitleFontSize(32);")
    printSpace8(ret_cnt,str_node+".setTitleText('');")
    printSpace8(ret_cnt,str_node+".setTitleColor(cc.color('#ffffff'));")

    # 设置纹理
    img_path, is_frame = ParseCCSSpriteProp(json_content)
    if is_frame:
        printSpace8(ret_cnt,str_node+".loadTextureNormal(" +
                    repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,str_node+".loadTextureNormal(" +
                    repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    return cur_cnt

def ParseCCSBtn2(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    printSpace8(ret_cnt,"var "+name+" = new ccui.Button();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    # 设置按钮属性
    printSpace8(ret_cnt,
        name+".setPressedActionEnabled(true);")#启用点击动作,只有当设置了按下的图片才有效果
    
    printSpace8(ret_cnt,name+".setTitleFontName(res.default_font);")

    if(name.startswith("btn_")):
        printSpace8(ret_cnt,name+".setZoomScale(-0.1);")
    else:
        printSpace8(ret_cnt,name+".setZoomScale(0);")

    # 设置纹理
    img_path, is_frame = ParseCCSSpriteProp(json_content,"NormalFileData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadTextureNormal(" +
                    repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadTextureNormal(" +
                    repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    img_path, is_frame = ParseCCSSpriteProp(json_content,"PressedFileData")
    if(img_path != ""):
        if is_frame:
            printSpace8(ret_cnt,name+".loadTexturePressed(" +
                        repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
        else:
            printSpace8(ret_cnt,name+".loadTexturePressed(" +
                        repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".setZoomScale(-0.1);")#点击缩小,有点击就缩小，不用则置为0

    img_path, is_frame = ParseCCSSpriteProp(json_content,"DisabledFileData")
    if(img_path != ""):
        if is_frame:
            printSpace8(ret_cnt,name+".loadTextureDisabled(" +
                        repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
        else:
            printSpace8(ret_cnt,name+".loadTextureDisabled(" +
                        repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    if("Scale9Enable" in json_content):
        scale9_x = 0 if(
            "Scale9OriginX" not in json_content) else json_content["Scale9OriginX"]
        scale9_y = 0 if(
            "Scale9OriginY" not in json_content) else json_content["Scale9OriginY"]
        printSpace8(ret_cnt,name+".setScale9Enabled(true);")
        printSpace8(ret_cnt,
            name+".setCapInsets(cc.rect("+str(scale9_x)+", "+str(scale9_y)+", 1, 1));")
            
    if json_content["ButtonText"] != "":
        printSpace8(ret_cnt,name+".setTitleText("+repr(json_content["ButtonText"])+");")
        printSpace8(ret_cnt,name+".setTitleFontSize("+str(json_content["FontSize"])+");")
        json_color = json_content["TextColor"]  # 设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"]
        if("G" in json_color):
            g = json_color["G"]
        if("B" in json_color):
            b = json_color["B"]

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            printSpace8(ret_cnt,name+".setTitleColor(cc.color(" +str(r)+", "+str(g)+", "+str(b)+"));")

    if("TouchEnable" not in json_content):
        printSpace8(ret_cnt,name+".setTouchEnabled(false);")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)

def ParseCCSSprite(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    is_btn = name.startswith("btn_")
    if(is_btn):
        cur_cnt = ParseCCSBtn(json_content, str_parent,name, cur_cnt, ret_cnt, name_parent)
    else:
        printSpace8(ret_cnt,"var "+name+" = new cc.Sprite();")
        if(str_parent):
            printSpace8(ret_cnt,str_parent+".addChild("+name+");")
        if(needUse(name)):
            # global PUSHCNT;
            printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
            printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
            cur_cnt += 1
            printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

        # 设置纹理
        img_path, is_frame = ParseCCSSpriteProp(json_content)
        if is_frame:
            printSpace8(ret_cnt,name+".initWithSpriteFrameName("+repr(img_path)+");")
        else:
            printSpace8(ret_cnt,name+".initWithFile("+repr(img_path)+");")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent,has_blend=not is_btn)


"""
    "Scale9Enable": true,
    "Scale9OriginX": 20,
    "Scale9OriginY": 18,
    "Scale9Width": 4,
    "Scale9Height": 19,
    "TouchEnable": true,
"""


def ParseCCSImage(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    if(name.startswith("btn_")):
        cur_cnt = ParseCCSBtn(json_content, str_parent, name, cur_cnt, ret_cnt, name_parent)
    else:
        printSpace8(ret_cnt,"var "+name+" = new ccui.ImageView();")
        if(str_parent):
            printSpace8(ret_cnt,str_parent+".addChild("+name+");")
        if(needUse(name)):
            # global PUSHCNT;
            printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
            printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
            cur_cnt += 1
            printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

        img_path, is_frame = ParseCCSSpriteProp(json_content)
        if is_frame:
            printSpace8(ret_cnt,name+".loadTexture("+repr(img_path) +
                        ", ccui.Widget.PLIST_TEXTURE);")
        else:
            printSpace8(ret_cnt,name+".loadTexture("+repr(img_path) +
                        ", ccui.Widget.LOCAL_TEXTURE);")

        # 设置九宫格
        if("Scale9Enable" in json_content):
            scale9_x = 0 if(
                "Scale9OriginX" not in json_content) else json_content["Scale9OriginX"]
            scale9_y = 0 if(
                "Scale9OriginY" not in json_content) else json_content["Scale9OriginY"]
            printSpace8(ret_cnt,name+".setScale9Enabled(true);")
            printSpace8(ret_cnt,
                name+".setCapInsets(cc.rect("+str(scale9_x)+", "+str(scale9_y)+", 1, 1));")
        else:
            printSpace8(ret_cnt,
                name+".ignoreContentAdaptWithSize(false);")#图片这里需要做忽略大小设置

        if("TouchEnable" in json_content):
            printSpace8(ret_cnt,name+".setTouchEnabled(true);")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)


# def ParseCCSLabel(json_content, str_parent, cur_cnt, ret_cnt):
#     name = getJsonPropName(json_content["Name"],str_parent);

#     ;
#         ui.setTextColor(color || cc.color("#ffffff"));
#         ui.setSystemFontName(res.default_font);
#         ui.setSystemFontSize(fsize || 36);
#         ui.setAnchorPoint(anchor || cc.p(0.5, 0.5));
#         ui.setPosition(pos || cc.p(0, 0));
#         ui.setString(text || "");

#         if (parent)
#             parent.addChild(ui);

#         return ui

"""
    "IsCustomSize": true,
    "FontSize": 30,
    "LabelText": "2人",
    "HorizontalAlignmentType": "HT_Center",
    "VerticalAlignmentType": "VT_Center",
"""


def ParseCCSText(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    isUseSystem = name.endswith("_system")
    isLabel = False
    if(name.startswith("label_")):
        isLabel = True
        printSpace8(ret_cnt,"var "+name+" = new cc.Label();")
    else:
        printSpace8(ret_cnt,"var "+name+" = new ccui.Text();")

    
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    if not isUseSystem:
        if isLabel:
            printSpace8(ret_cnt,name+".setSystemFontName(res.default_font);")
        else:
            printSpace8(ret_cnt,name+".setFontName(res.default_font);")
    if("IsCustomSize" in json_content):
        json_size = json_content["Size"]
        if(isLabel):
            # printSpace8(ret_cnt,name+".setMaxLineWidth("+str(json_size["X"])+");")
            printSpace8(ret_cnt,name+".setWidth("+str(json_size["X"])+");")
            printSpace8(ret_cnt,name+".setHeight("+str(json_size["Y"])+");")
        else:
            printSpace8(ret_cnt,name+".ignoreContentAdaptWithSize(false);")
            printSpace8(ret_cnt,name+".setTextAreaSize(cc.size(" +str(json_size["X"])+", "+str(json_size["Y"])+"));")
    if("FontSize" in json_content):
        if(isLabel):
            printSpace8(ret_cnt,name+".setSystemFontSize("+str(json_content["FontSize"])+");")
        else:
            printSpace8(ret_cnt,name+".setFontSize("+str(json_content["FontSize"])+");")
    if("LabelText" in json_content):
        printSpace8(ret_cnt,name+".setString("+repr(json_content["LabelText"])+");") #repr

    if("HorizontalAlignmentType" in json_content):
        horizontal_align = json_content["HorizontalAlignmentType"]
        if(horizontal_align == "HT_Center"):
            if(isLabel):
                printSpace8(ret_cnt,name+".setHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);")
            else:
                printSpace8(ret_cnt,name+".setTextHorizontalAlignment(cc.TEXT_ALIGNMENT_CENTER);")
        elif(horizontal_align == "HT_Right"):
            if(isLabel):
                printSpace8(ret_cnt,name+".setHorizontalAlignment(cc.TEXT_ALIGNMENT_RIGHT);")
            else:
                printSpace8(ret_cnt,name+".setTextHorizontalAlignment(cc.TEXT_ALIGNMENT_RIGHT);")

    if("VerticalAlignmentType" in json_content):
        vertical_align = json_content["VerticalAlignmentType"]
        if(vertical_align == "VT_Center"):
            if(isLabel):
                printSpace8(ret_cnt,name+".setVerticalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_CENTER);")
            else:
                printSpace8(ret_cnt,name+".setTextVerticalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_CENTER);")
        elif(vertical_align == "VT_Bottom"):
            if(isLabel):
                printSpace8(ret_cnt,name+".setVerticalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM);")
            else:
                printSpace8(ret_cnt,name+".setTextVerticalAlignment(cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM);")

    if(isLabel and "TouchEnable" in json_content):
        printSpace8(ret_cnt,name+".setTouchEnabled(true);")

    if "ShadowEnabled" in json_content:
        shadow_off_x = json_content["ShadowOffsetX"]
        shadow_off_y = json_content["ShadowOffsetY"]

        r = 255
        g = 255
        b = 255

        shadow_color = json_content["ShadowColor"]
        if("R" in shadow_color):
            r = shadow_color["R"]
        if("G" in shadow_color):
            g = shadow_color["G"]
        if("B" in shadow_color):
            b = shadow_color["B"]

        printSpace8(ret_cnt,name+".enableShadow(cc.color("+str(r)+", "+str(g)+", "+str(b)+"), cc.size(" +
                    str(shadow_off_x)+", "+str(shadow_off_y)+"));")

    if "OutlineEnabled" in json_content:
        r = 255
        g = 255
        b = 255

        outline_color = json_content["OutlineColor"]
        if("R" in outline_color):
            r = outline_color["R"]
        if("G" in outline_color):
            g = outline_color["G"]
        if("B" in outline_color):
            b = outline_color["B"]

        outline_size = 1
        if "OutlineSize" in json_content:
            outline_size = json_content["OutlineSize"]
        printSpace8(ret_cnt,name+".enableOutline(cc.color("+str(r)+", " +
                    str(g)+", "+str(b)+"), "+str(outline_size)+");")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent, is_text=True)


"""
    "CharWidth": 18,setTouchEnabled
    "CharHeight": 22,
    "LabelText": "/123456",
    "StartChar": "/",
    "LabelAtlasFileImage_CNB": {
      "Type": "Normal",
      "Path": "platform/num_active.png",
      "Plist": ""
    },
"""


def ParseCCSTextAtlas(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    img_path, is_frame = ParseCCSSpriteProp(
        json_content, "LabelAtlasFileImage_CNB")
    printSpace8(ret_cnt,"var "+name+" = new ccui.TextAtlas('"+json_content["LabelText"]+"', "
                + repr(img_path)
                + ", "+str(json_content["CharWidth"]) +
                ", "+str(json_content["CharHeight"])
                + ", '"+json_content["StartChar"]+"');")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        # printCustom("ParseCCSTextAtlas 1",cur_cnt)
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        # printCustom("ParseCCSTextAtlas 2",cur_cnt)
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent, is_text=True)


"""
    "ProgressInfo": 50,
    "ImageFileData": {
      "Type": "Normal",
      "Path": "platform/shuzhitiao2.png",
      "Plist": ""
    },
"""


def ParseCCSLoadingBar(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    printSpace8(ret_cnt,"var "+name+" = new ccui.LoadingBar();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "ImageFileData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadTexture("+repr(img_path) +
                    ", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadTexture("+repr(img_path) +
                    ", ccui.Widget.LOCAL_TEXTURE);")

    printSpace8(ret_cnt,name+".setPercent(0);")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)


def ParseCCSParticle(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    img_path, is_frame = ParseCCSSpriteProp(json_content, None)
    printSpace8(ret_cnt,"var "+name+" = cc.ParticleSystem.create("+repr(img_path)+");")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")
        printCustom(name+".stop();")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent, is_node=True, has_blend=True)


"""
    "ClipAble": true,
    "BackColorAlpha": 0,
    "ComboBoxIndex": 1,
    "SingleColor": {
      "R": 0,
      "G": 0,
      "B": 0
    },
    "FirstColor": {
      "R": 150,
      "G": 200
    },
    "EndColor": {},
    "ColorVector": {
      "ScaleY": 1.0
    },
    "Scale9Width": 1,
    "Scale9Height": 1,
    "TouchEnable": true,
"""


def ParseCCSPanel(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    printSpace8(ret_cnt,"var "+name+" = new ccui.Layout();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    # 设定裁切
    printSpace8(ret_cnt,name+".setClippingEnabled(" +
                ("true" if json_content["ClipAble"] else "false")+");")
    # 设定点击
    if("TouchEnable" in json_content):
        printSpace8(ret_cnt,name+".setTouchEnabled(true);")

    # 设定背景图片
    bg_type = 0
    if("ComboBoxIndex" in json_content):
        bg_type = json_content["ComboBoxIndex"]
    if(bg_type == 0):  # 只有图片
        if("FileData" in json_content):  # 检查纹理设置

            img_path, is_frame = ParseCCSSpriteProp(json_content)
            if is_frame:
                printSpace8(ret_cnt,name+".setBackGroundImage("+repr(img_path) +
                            ", ccui.Widget.PLIST_TEXTURE);")
            else:
                printSpace8(ret_cnt,name+".setBackGroundImage("+repr(img_path) +
                            ", ccui.Widget.LOCAL_TEXTURE);")

            # 检查九宫格设置
            if("Scale9Enable" in json_content):
                scale9_x = 0 if(
                    "Scale9OriginX" not in json_content) else json_content["Scale9OriginX"]
                scale9_y = 0 if(
                    "Scale9OriginY" not in json_content) else json_content["Scale9OriginY"]
                printSpace8(ret_cnt,name+".setBackGroundImageScale9Enabled(true);")
                printSpace8(ret_cnt,name+".setBackGroundImageCapInsets(cc.rect(" +
                            str(scale9_x)+", "+str(scale9_y)+", 1, 1));")
    elif(bg_type == 1):  # 纯色

        json_color = json_content["SingleColor"]  # 设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"]
        if("G" in json_color):
            g = json_color["G"]
        if("B" in json_color):
            b = json_color["B"]

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            printSpace8(ret_cnt,name+".setBackGroundColor(cc.color(" +
                        str(r)+", "+str(g)+", "+str(b)+"));")

        if("BackColorAlpha" in json_content):
            printSpace8(ret_cnt,name+".setBackGroundColorOpacity(" +
                        str(json_content["BackColorAlpha"])+");")
        printSpace8(ret_cnt,name+".setBackGroundColorType(ccui.Layout.BG_COLOR_SOLID);")

    else:  # 渐变色 不支持
        raise NotImplementedError()

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)


"""
    "BackGroundData": {
      "Type": "Normal",
      "Path": "platform/B7.png",
      "Plist": ""
    },
    "ProgressBarData": {
      "Type": "Normal",
      "Path": "platform/B6.png",
      "Plist": ""
    },
    "BallNormalData": {
      "Type": "Normal",
      "Path": "platform/B5.png",
      "Plist": ""
    },
"""


def ParseCCSSlider(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    printSpace8(ret_cnt,"var "+name+" = new ccui.Slider();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "BackGroundData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadBarTexture("+repr(img_path) +
                    ", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadBarTexture("+repr(img_path) +
                    ", ccui.Widget.LOCAL_TEXTURE);")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "ProgressBarData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadProgressBarTexture(" +
                    repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadProgressBarTexture(" +
                    repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "BallNormalData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadSlidBallTextures(" +
                    repr(img_path)+","+repr(img_path)+","+repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadSlidBallTextures(" +
                    repr(img_path)+","+repr(img_path)+","+repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")
    printSpace8(ret_cnt,name+".setPercent(0);")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)


"""
    "NormalBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "PressedBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "DisableBackFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_un.png",
      "Plist": ""
    },
    "NodeNormalFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_select.png",
      "Plist": ""
    },
    "NodeDisableFileData": {
      "Type": "Normal",
      "Path": "platform/checkbox_select.png",
      "Plist": ""
    },
    "TouchEnable": true,
"""


def ParseCCSCheckBox(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    printSpace8(ret_cnt,"var "+name+" = new ccui.CheckBox();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "NormalBackFileData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadTextureBackGround(" +
                    repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadTextureBackGround(" +
                    repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    img_path, is_frame = ParseCCSSpriteProp(json_content, "NodeNormalFileData")
    if is_frame:
        printSpace8(ret_cnt,name+".loadTextureFrontCross(" +
                    repr(img_path)+", ccui.Widget.PLIST_TEXTURE);")
    else:
        printSpace8(ret_cnt,name+".loadTextureFrontCross(" +
                    repr(img_path)+", ccui.Widget.LOCAL_TEXTURE);")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent, no_size=True)


def ParseCCSTextField(json_content, str_parent, str_node, cur_cnt, ret_cnt):
    str_holder = json_content["PlaceHolderText"]
    printSpace8(ret_cnt,"var "+str_node+" = new ccui.TextField("+repr(str_holder)+", res.default_font, "
                + str(json_content["FontSize"])+");")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+str_node+");")
    if(needUse(str_node)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,str_node+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+str_node+");")

    json_color = json_content["CColor"]  # 设置颜色值
    r = 255
    g = 255
    b = 255
    if("R" in json_color):
        r = json_color["R"]
    if("G" in json_color):
        g = json_color["G"]
    if("B" in json_color):
        b = json_color["B"]

    if(r == 255 and g == 255 and b == 255):
        pass
    else:
        printSpace8(ret_cnt,str_node+".setTextColor(cc.color(" +
                    str(r)+", "+str(g)+", "+str(b)+"));")
    printSpace8(ret_cnt,str_node+".setPlaceHolderColor(cc.color('#616161'));")

    printSpace8(ret_cnt,str_node+".ignoreContentAdaptWithSize(false);")
    json_size = json_content["Size"]
    printSpace8(ret_cnt,str_node+".setTextAreaSize(cc.size(" +
                str(json_size["X"])+", "+str(json_size["Y"])+"));")

    if("MaxLengthEnable" in json_content):
        printSpace8(ret_cnt,str_node+".setMaxLengthEnabled(true);")
        printSpace8(ret_cnt,str_node+".setMaxLength(" +
                    str(json_content["MaxLengthText"])+");")

    if "PasswordEnable" in json_content:
        printSpace8(ret_cnt,
            str_node+".setPasswordEnabled(true);")

    if("TouchEnable" in json_content):
        printSpace8(ret_cnt,str_node+".setTouchEnabled(true);")

    return cur_cnt


"""
    "FontSize": 26,
    "IsCustomSize": true,
    "LabelText": "input_png",
    "PlaceHolderText": "input_png",
    "MaxLengthEnable": true,
    "MaxLengthText": 10,
    "TouchEnable": true,
"""


def ParseCCSTextInput(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt
    if(name == str_parent):
        if(needUse(name)):
            name = name[:-4] + "__use"
        else:
            name = name+"_"

    if(name.startswith("tf_")):
        cur_cnt = ParseCCSTextField(json_content, str_parent, name, cur_cnt, ret_cnt, name_parent)
    else:
        json_size = json_content["Size"]
        str_bg = json_content["PlaceHolderText"]

        if str_bg == "":
            str_bg = "input_png"

        if USERIMAGEPLIST:
            printSpace8(ret_cnt,"var "+name+" = cc.EditBox.create(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"), "
                        + RESOURCEFRAMES+"."+str_bg+", ccui.Widget.PLIST_TEXTURE);")#label text的文字当作背景图片，不能为空，至少放个透明图片
        else:
            printSpace8(ret_cnt,"var "+name+" = cc.EditBox.create(cc.size("+str(json_size["X"])+", "+str(json_size["Y"])+"), "
                        + RESOURCE+"."+str_bg+", ccui.Widget.LOCAL_TEXTURE);")#label text的文字当作背景图片，不能为空，至少放个透明图片
        # input_key_use.setPlaceHolder("兑换码");
        printSpace8(ret_cnt,
            name+".setPlaceHolder('请输入');")#这里必须在addChild之前写入，否则位置不对
        if(str_parent):
            printSpace8(ret_cnt,str_parent+".addChild("+name+");")
        if(needUse(name)):
            # global PUSHCNT;
            printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
            printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
            cur_cnt += 1
            printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

        printSpace8(ret_cnt,name+".setFontName(res.default_font);")
        printSpace8(ret_cnt,name+".setFontSize("+str(json_content["FontSize"])+");")

        json_color = json_content["CColor"]  # 设置颜色值
        r = 255
        g = 255
        b = 255
        if("R" in json_color):
            r = json_color["R"]
        if("G" in json_color):
            g = json_color["G"]
        if("B" in json_color):
            b = json_color["B"]

        if(r == 255 and g == 255 and b == 255):
            pass
        else:
            printSpace8(ret_cnt,
                name+".setFontColor(cc.color("+str(r)+", "+str(g)+", "+str(b)+"));")
        printSpace8(ret_cnt,name+".setPlaceholderFontColor(cc.color('#333333'));")

        printSpace8(ret_cnt,name+".setInputFlag(cc.EDITBOX_INPUT_FLAG_SENSITIVE);")
        printSpace8(ret_cnt,
            name+".setInputMode(cc.EDITBOX_INPUT_MODE_SINGLELINE);")#单行输入

        if("MaxLengthEnable" in json_content):
            printSpace8(ret_cnt,
                name+".setMaxLength("+str(json_content["MaxLengthText"])+");")

        if "PasswordEnable" in json_content:
            printSpace8(ret_cnt,
                name+".setInputFlag(cc.EDITBOX_INPUT_FLAG_PASSWORD);")

    printSpace8(ret_cnt,
        name+".setTextHorizontalAlignment(cc.TEXT_ALIGNMENT_LEFT);")#设置靠左对齐
    printSpace8(ret_cnt,name+".setString('');")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent, no_color=True)


"""
    "IsBounceEnabled": true,
    "InnerNodeSize": {
      "Width": 540,
      "Height": 2000
    },
    "ScrollDirectionType": "Vertical",Vertical_Horizontal
    "ClipAble": true,
    "BackColorAlpha": 0,
"""


def ParseCCSScrollView(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    printSpace8(ret_cnt,"var "+name+" = new ccui.ScrollView();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    if("IsBounceEnabled" in json_content):
        printSpace8(ret_cnt,name+".setBounceEnabled(true);")

    direction = json_content["ScrollDirectionType"]
    if(direction == "Vertical"):
        printSpace8(ret_cnt,name+".setDirection(cc.SCROLLVIEW_DIRECTION_VERTICAL);")
    elif(direction == "Horizontal"):
        printSpace8(ret_cnt,name+".setDirection(cc.SCROLLVIEW_DIRECTION_HORIZONTAL);")
    else:
        printSpace8(ret_cnt,name+".setDirection(cc.SCROLLVIEW_DIRECTION_BOTH);")

    # 内部内容大小
    inner_size = json_content["InnerNodeSize"]
    printSpace8(ret_cnt,name+".setInnerContainerSize(cc.size(" +
                str(inner_size["Width"])+", "+str(inner_size["Height"])+"));")
    # 设定裁切
    printSpace8(ret_cnt,name+".setClippingEnabled(" +
                ("true" if json_content["ClipAble"] else "false")+");")

    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)


def ParseFnt(json_content, str_parent, cur_cnt, ret_cnt, name_parent):
    name,ret = getJsonPropName(json_content["Name"],str_parent);
    if (not ret) :
        return ret_cnt

    printSpace8(ret_cnt,"var "+name+" = new ccui.TextBMFont();")
    if(str_parent):
        printSpace8(ret_cnt,str_parent+".addChild("+name+");")
    if(needUse(name)):
        # global PUSHCNT;
        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        printSpace8(ret_cnt,name+".setName('"+getCurNodeNamePrefix(name_parent,cur_cnt)+"');")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt)+".push("+name+");")

    printSpace8(ret_cnt,name+".setFntFile("+repr("res/"+json_content["LabelBMFontFile_CNB"]["Path"])+");")
    printSpace8(ret_cnt,name+".setString("+repr(json_content["LabelText"])+");")
    
    return ParseCCSNodeProp(json_content, name, cur_cnt, ret_cnt, name_parent)

def ParseCCSChildren(json_children, str_parent, cur_cnt, ret_cnt, name_parent):
    for i in range(len(json_children)):
        json_content = json_children[i]
        if(json_content["ctype"] == "SingleNodeObjectData"):
            cur_cnt = ParseCCSNode(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "SpriteObjectData"):
            cur_cnt = ParseCCSSprite(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "ButtonObjectData"):
            cur_cnt = ParseCCSBtn2(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "ImageViewObjectData"):
            cur_cnt = ParseCCSImage(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "TextObjectData"):
            cur_cnt = ParseCCSText(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "TextAtlasObjectData"):
            cur_cnt = ParseCCSTextAtlas(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "LoadingBarObjectData"):
            cur_cnt = ParseCCSLoadingBar(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "ParticleObjectData"):
            cur_cnt = ParseCCSParticle(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "PanelObjectData"):
            cur_cnt = ParseCCSPanel(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "SliderObjectData"):
            cur_cnt = ParseCCSSlider(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "CheckBoxObjectData"):
            cur_cnt = ParseCCSCheckBox(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "TextFieldObjectData"):
            cur_cnt = ParseCCSTextInput(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "ScrollViewObjectData"):
            cur_cnt = ParseCCSScrollView(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "TextBMFontObjectData"):
            cur_cnt = ParseFnt(json_content, str_parent, cur_cnt, ret_cnt, name_parent)
        elif(json_content["ctype"] == "ProjectNodeObjectData"):
            if not "FileData" in json_content:
                raise Exception("json_content="+str(json_content))

            json_file = json_content["FileData"]["Path"]  # 获取到json文件

            name,ret = getJsonPropName(json_content["Name"],str_parent);

            ret_cnt_new = ret_cnt+1
            cur_cnt,load_as_csj = ParseCCSJson(CURGAMERESDIR+"/"+json_file,
                         name, str_parent, cur_cnt, ret_cnt_new, name_parent)

            cur_cnt = ParseCCSNodeProp(
                json_content, name, cur_cnt, ret_cnt_new, name_parent, True,load_as_csj=load_as_csj)
            printSpace8(ret_cnt,"}")

    return cur_cnt


def ParseCCSJson(json_file, str_node=None, str_parent=None, cur_cnt=0, ret_cnt=0, name_parent=""):
    # print("//", json_file,json_file.find("scene_ext_ignore"),str_parent,ret_cnt)
    load_as_csj = False
    if json_file.find("scene_ext_ignore") != -1:
        with open(json_file, "rb") as file: #,encoding="utf-8"
            # print("json_file=",json_file)
            # content = file.read()
            # nodes = json.loads(content.decode("utf-8"))
            nodes = json.load(file)
            root = nodes["Content"]["Content"]["ObjectData"]
            # printSpace8(ret_cnt,json_file);

            if ret_cnt == 0 and not str_parent:
                func_name = json_file[json_file.rfind("_")+1:json_file.rfind(".json")]
                func_name = "autoMakeFor" + func_name.upper()
                printSpace4(ret_cnt,func_name + ": function(parent, pos){")

                printSpace8(ret_cnt,"var "+getCurRetName(ret_cnt)+" = [];")
                ParseCCSNode(root, str_parent, 0, ret_cnt, name_parent, str_node)

                printSpace8(ret_cnt,"return ret;")
                printSpace4(ret_cnt,"},")
            else:
                printSpace4(ret_cnt,"{")

                printSpace8(ret_cnt,"var "+getCurRetName(ret_cnt)+" = [];")
                ParseCCSNode(root, str_parent, 0, ret_cnt, name_parent+str(cur_cnt)+"-", str_node)

                printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
                cur_cnt += 1
                printSpace8(ret_cnt,getCurRetName(ret_cnt-1) +
                            ".push("+getCurRetName(ret_cnt)+");")
    else:
        cur_csj_name = str_node

        json_anima = json_file[len(CURGAMERESDIR):]
        printSpace4(ret_cnt,"{")
        printSpace8(ret_cnt,"var "+cur_csj_name+" = ccs.load(" +
                    repr("res"+json_anima)+", 'res/');")

        printSpace8(ret_cnt,"/**push node "+str(cur_cnt)+" */")
        cur_cnt += 1
        printSpace8(ret_cnt,getCurRetName(ret_cnt-1) + ".push("+cur_csj_name+");")

        printSpace8(ret_cnt,"if ("+cur_csj_name+".node) {")
        printSpace8(ret_cnt+1,str_parent+".addChild("+cur_csj_name+".node, 0);")
        printSpace8(ret_cnt+1,cur_csj_name+".node.runAction("+cur_csj_name+".action);")
        printSpace8(ret_cnt,"} else {")
        printSpace8(ret_cnt+1,"Log.e('anima json load failed, file= "+json_anima+"');")
        printSpace8(ret_cnt,"}")

        load_as_csj = True

    return cur_cnt, load_as_csj


def JsonWalk(path, file):
    if(file.endswith(".json") and file.startswith("Node_")):
        ParseCCSJson(file_helper.join(path, file))


def PrintComments():
    printCustom("/**")
    printCustom("This file is auto maked by python reading ccs json file!")
    printCustom("Don't change it only the TEXT label")
    printCustom("!!!make [res.default_font] the value !!!")
    printCustom(
        "if you want a button, just rename the sprite/imageview name start with 'btn_'")
    printCustom()
    printCustom(
        "if you want a node to be return, just rename the node name end with '_use' or start with 'use_'")
    printCustom()
    printCustom("if you want a loadingbar use scale9, just do :" + """

            ui.setScale9Enabled(true);
            ui.setCapInsets(capInset);

        """+" by yourself!")
    printCustom()
    printCustom(
        "the default use of text input is EditBox,you can use TextField with name start with 'tf_'")
    printCustom()
    printCustom("*/")


def AutoParseJsonDir(path, moduleName):
    # 解析节点json
    PrintComments()
    printCustom("var "+moduleName+" = {")
    file_helper.Diskwalk(path).walk(JsonWalk)
    printCustom("};")
    printCustom()


if __name__ == '__main__':
    # 以后路径统一使用 '/ 请勿使用 '\\'

    # TestJson()
    # print(getCurRetName(1))
    # print(getCurNodeNamePrefix(2,0),getCurNodeNamePrefix(2,1))

    # 更新
    # ChangePosition("test/pfishRoutes.json","test/pfishRoutes_new.json",False,False)
    # ChangePosition("test/pfishRoutes.json","test/pfishRoutes_new_x.json",True,False)
    #还原成编辑器路径
    # ChangePosition("test/pfishRoutes-new.json","test/pfishRoutes.json",False,True)

    #压缩json文件
    def subSize(dirpath, file):
        if file.endswith(".json"):
            fullFile = dirpath+"/"+file
            print("subSize file="+fullFile)
            content = {}
            with open(fullFile, "rb") as f:
                content = json.load(f)
                # print(content,type(content))
            with open(fullFile, "w") as f2:
                json.dump(content,f2,separators=(',',':')) #取消json之间的空格
                    
    # file_helper.Diskwalk("D:/work/Github/Fish/res_main/platform/node", False).walk(subSize)
    # file_helper.Diskwalk("D:/work/Github/Fish/res_main/games/fish/node", False).walk(subSize)

    # 解析所有的node节点，转化成js函数

    USERIMAGEPLIST = False
    CURGAMERESDIR = "D:/Github/Fish/res1"
    # # 大厅
    AutoParseJsonDir(CURGAMERESDIR+"/scene_ext_ignore/vip","AutoUiForMain")
    # JsonWalk("D:/work/Github/Fish/res1/scene_ext_ignore/vip","Node_GMJB.json")

    # 捕鱼游戏
    # AutoParseJsonDir(CURGAMERESDIR+"/scene_ext_ignore/game","AutoUiForFish")

    # 深海寻宝
    # AutoParseJsonDir(CURGAMERESDIR+"/scene_ext_ignore/game2","AutoUiForShz")

    # with open("D:/work/UI/2020-06-24/text.txt","r",encoding='utf-8') as f:
    #     a = f.read()
    #     print(a,encoding="utf-8")

