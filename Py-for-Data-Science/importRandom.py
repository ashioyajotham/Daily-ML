# Importing built in module random

import random

# printing random integer between 0 and 5
print(random.randint(0,5))

# print random floating number between 0 and 1
print(random.random())

# random number between 0 and 100
print(random.random() * 100)

List = [1,4, True, 800, 'Python', 27, 'hello']

# Using choice function in random module for choosing
# a random element from a set such as a list
print(random.choice(List))

# Importing built in module datetime
import datetime
from datetime import date
import time

# Returns the number of seconds since the 
# Unix Epoch, January 1st 1970
print(time.time())

# Converts a number of seconds to a date object
print(date.fromtimestamp(454554))

from random import randrange, randint

print('\n')
print(randrange(1), end='')
print(randrange(0,1), end='')
print(randrange(0,1,1), end='')
print(randint(0,1))



