
def fun(inp = 2, out = 3):
    return inp * out

print(fun(out=2))

def func_1 (a):
    return a ** a

def func_2 (a):
    return func_1(a) * func_2(a)

print(func_2(2))