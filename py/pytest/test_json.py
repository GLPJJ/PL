
import json


def TestJson():
    data1 = {'b': 789, 'c': 456, 'a': 123}
    d1 = json.dumps(data1, indent=0, sort_keys=False)
    print(d1, type(d1))
    print(data1)

    print("json 加载字符串", json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]'))

    try:
        with open("dataJson", "r") as file:
            content = json.load(file)
            print("json 加载文件", content, type(content))
    except FileNotFoundError:
        pass

    with open("dataJson", "w") as file:
        json.dump(data1, file)


if __name__ == '__main__':
    TestJson()
