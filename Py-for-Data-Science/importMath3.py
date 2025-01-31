# Implementing factorial function

# Using for loops
def fact_loop(num):
    if num < 0:
        return 0
        if num == 0:
            return 1

    factorial = 1
    for i in range(1, num+1):
        factorial = factorial * 1
    return factorial



# Using a recursive function
def fact_recursion(num):
    if num < 0:
        return 0
    if num == 0:
        return 1

    return num * fact_recursion(num-1)



# Using factorials()
import math
a = 5
print("The factorial of 5 is ", end="")
print(math.factorial(a))
