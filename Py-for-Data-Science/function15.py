def fun(x, y):
    if x == y:
        return x
    else:
        return fun(x, y - 1)

print(fun(0, 3))

def fun(x):
    if x % 2 == 0:
        return 1
    else:
        return 2

print(fun(fun(2)))