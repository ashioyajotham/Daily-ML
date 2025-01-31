def fun(x):
    global y
    y = x * x
    return y

fun(2)
print(y)