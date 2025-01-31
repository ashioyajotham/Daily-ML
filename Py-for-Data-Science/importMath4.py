import math
number = math.floor(10.25201)
print("The floor value is ", number)

import math
a = 2,3
print("The floor of 2,3 is ", end="")
print(math.floor(a))



import math
number = math.ceil(10.25201)
print("The ceil value is ", number)

import math
a = 2,3
print("The ceil of 2,3 is ", end="")
print(math.ceil(a))


# When truncating positive numbers, trunc() behaves the same as floor() while 
# truncating neg numbers, trunc() behaves like ceil()
import math
result = math. trunc(12.32) == math.floor(12.32)
print(result)


import math
result = math. trunc(-43.24) == math.ceil(-43.24)
print(result)

