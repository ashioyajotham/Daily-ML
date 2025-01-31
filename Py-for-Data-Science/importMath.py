import math
dir() #Using the dir() argument shows what's in the global namespace 

import math
test_int = 4
test_neg_int =  -3
test_float = 0.00
print(math.exp(test_int))   # used to calculate the power of e ie e^y
print(math.exp(test_neg_int))
print(math.exp(test_float))


from math import log10, log2, pow

print("The value of 3**4 is ", end="") #computes x**y. This function first converts 
                                       #its arguments into float and then computes the power



from math import log

print(log(2,3)) # The log of 2 with base 3
print(log2(16)) # The log of 16 with base 2
print(log10(1000)) # The log of 1000 with base 10



import math
print(math.e) # Returns the Euler's constant



import math
print(math.pi) # Returns a more precise value of pi



import math
r = 4
pie = math.pi
print(pie * r * r)




import math
print(math.tau) # returns the value tau: 6.283185307179586



import math
print(math.inf) # prints the positive infinity
print(-math.inf) # prints the negative infinity


import math
print(math.inf > 10e108)
print(-math.inf < -10e108)



import math
print(math.nan) # returns a floating point nan (Not a number) value



import math
a = 15
b = 5
print("The gcd of 5 and 15 is ", end="")
print(math.gcd(b,a))


import math
a - -10
print("The absolute value of -10 is ", end="") #finding the absolute value
print(math.fabs(a))


import math
print(math.sqrt(0))
print(math.sqrt(3.5))


import math
print(math.trunc(12.32)) #Truncate downward toward zero
print(math.trunc(-43.24)) #Truncate upward toward zero
















