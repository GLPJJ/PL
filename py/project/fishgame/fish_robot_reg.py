import file_helper
import os
import json
import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")


def dealWithName(path):
    with open(path, "rb") as f:
        data = []
        for line in f:
            # print(line)
            newline = line[0:-2]
            newlineUtf8 = newline.decode('utf-8')
            # print(newline,newlineUtf8)
            data.append(newlineUtf8)
            # print(data)
        print(data)
        str = json.dumps(data, indent=0, sort_keys=False)
        print(str)


if __name__ == '__main__':
    dealWithName("C:/Users/Administrator/Desktop/names.txt")
