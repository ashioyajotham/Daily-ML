#A variable that exists outside a function has a scope inside the function body
#unless the function defines a variable of the same name

var = 2

def mult_by_var(x):
    return x * var

print(mult_by_var(7))



def mult(x):
    var = 5
    return x * var

print(mult(7))



# You can use the global keyword 
# followed by a variable name to make the variable's scope global 
var = 2
print(var)

def return_var():
    global var
    var = 5
    return var

print (return_var())
print(var)


