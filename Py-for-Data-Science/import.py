import math

#If you want to (or have to) import more than one module, 
# you can do it by repeating the import clause (preferred)

import math
import sys

# or  by listing the modules after the import keyword

import math, sys


import math
print(math.sin(math.pi/2))



import math

def sin(x):
    if 2 * x == pi:
        return 0.99999999
    else:
        return None
    
pi = 3.14

print(sin(pi/2))
print(math.sin(math.pi/2))


#You are not only allowed to import a module as a whole, but to import only indvidual entities from it.
# In this case, the imported entities must not be prefixed when used
#The most general form of the above statement allows you to import all entities offered by a module

from math import*
from math import sin, pi # In such cases, we don't use the dot operators

print(sin(pi/2))

pi = 3.14

def sin (x):
    if 2 * x == pi:
        return 0.99999999
    else:
        return None

print(sin(pi / 2))
