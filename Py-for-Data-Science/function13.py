def fun(x):
    x += 1
    return x

x = 2
x = fun(x + 1)
print(x)


def f(x):
    if x == 0:
        return 0
    return x+ f(x - 1)

print(f(3))