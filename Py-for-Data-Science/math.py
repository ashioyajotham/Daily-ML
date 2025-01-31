import math
result = math.e != math.pow(2,4)
print(int(result))



from random import randint
for i in range(2):
    print(randint(1,2), end='')


print(3 * "abc" + "xyz")

print(chr(ord('z')-2))


try:
    print("5"/0)
except ArithmeticError:
    print("arith")
except ZeroDivisionError:
    print("zero")
except:
    print("Some")


print(chr(ord("p") + 2))

import math
print(dir(math))

print(__name__)