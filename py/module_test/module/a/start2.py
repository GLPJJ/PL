if __name__ == '__main__':

    # 当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
    # 然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
    # 正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块

    import sys
    # print(sys.path)
    # print(__file__)
    # sys.path.append(sys.path[0]+"\\..")
    # print(cur_dir)
    sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
    # print(sys.path)
    import dir_same
    print(dir_same.add(0, 7))

else:
    # import ..dir_same #invalid syntax 永远也没有这种写法

    # import module.dir_same #这样写可以被start使用(当成模块了),但是不能被start1使用(没有被当成模块)
    # print(module.dir_same.add(0,7))

    # from .. import dir_same #同样的,这个写法也只能被start使用,start1不能
    # print(dir_same.add(0,7))

    # 下面这个有点变态!! 不推荐这样,因为我们的模块本身出了问题,需要重新架构一下
    # 如果既要当模块被start使用,又要被start1使用,解决方法:
    try:
        from .. import dir_same  # 这里直接当主入口运行是会报错的
    except ValueError as e:  # attempted relative import beyond top-level package
        import sys
        sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
        import dir_same
    print(dir_same.add(0, 7))

    import module.a.b.start3  # 这个必须这么写
