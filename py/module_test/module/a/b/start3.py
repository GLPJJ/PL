if __name__ == '__main__':

    # 当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
    # 然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
    # 正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
    import sys
    sys.path.append(__file__[:__file__.rfind("\\")]+"\\..\\..")# 引入上上层目录
    import dir_same
    print(dir_same.add(0, 8))

else:
    # import ..dir_same #invalid syntax
    import module.dir_same  # name 'dir_same' is not defined

    # from ../.. import dir_same #可行,但是不能由上层目录的脚本当主函数入口,比如直接调用start1
    # 如果既要当模块被start使用,又要被start1使用,解决方法:
    # try:
    #     from .. import dir_same #这里直接当主入口运行是会报错的
    # except ValueError as e: #attempted relative import beyond top-level package
    #     import sys
    #     sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
    #     import dir_same

    print(module.dir_same.add(0, 8))
