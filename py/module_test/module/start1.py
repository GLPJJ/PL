if __name__ == '__main__':  # 当我们脚本是主入口的时候
    # 这里虽然pylint报错了，其实我们可以这样操作的
    import dir_same  # 对于同级目录,我们python脚本可以直接引入
    import a.dir_child  # 对于子目录,我们可以通过加目录点的方式引入
    import a.b.dir_child_child  # 同理对于更深的子目录

    print(dir_same.add(0, 4))
    print(a.dir_child.add(0, 5))
    print(a.b.dir_child_child.add(0, 6))

    # import a.start2  # 报错,由于start2需要引入当前目录的脚本dir_same,导致beyond top-level package
    # 简单的理解就是我们引入的模块不能再引入当前目录的脚本,这不符合python设计的初衷
    # 粗暴的方式就是通过捕获异常的方式,再以主入口的方式引入

else:  # 当我们是以模块的方式被引入的时候,我们需要从模块顶层目录开始引入
    import module.dir_same
    import module.a.dir_child
    import module.a.b.dir_child_child

    print(module.dir_same.add(0, 4))
    print(module.a.dir_child.add(0, 5))
    print(module.a.b.dir_child_child.add(0, 6))

    import module.a.start2
