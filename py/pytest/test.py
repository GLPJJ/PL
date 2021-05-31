def getJsonPropName(name, str_parent):
    if(name == str_parent):
        if(name.endswith("_use")):
            name = name[:-4] + "__use"
        else:
            name = name+"_"
    return name


print(getJsonPropName("FileNode_2_use", "FileNode_2_use"))
