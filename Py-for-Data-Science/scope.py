def scope_test ():
    x = 123

x = scope_test()
print(x)


def my_function():
    print('Do I know tht variable?', var)

var = 1
my_function()
print(var)



# You can use the global keyword 
# followed by a variable name to make the variable's scope global 
def my_function():
    global var
    var = 2
    print("Do I know that variable?", var)

var = 1
my_function()
print(var)


def my_function(n):
    print("I got", n)
    n += 1
    print("I have", n)

var = 1
my_function(var)
print(var)