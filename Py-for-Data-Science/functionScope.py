def func1():
    num = 3
    print(num)


def func2():
    global num
    double_num=num * 2
    num = 6
    print(double_num)
