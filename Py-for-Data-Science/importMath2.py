from math import log10, log2, pi, radians, degrees, sin, cos, tan, asin

ad = 90
ar = radians(ad)
ad = degrees(ar)

print(ad == 90.)
print(ar == pi/2.)
print(sin(ar) / cos(ar) == tan(ar))
print(asin(sin(ar)) == ar)


from math import e, exp, log

# math.e constant returns the Euler's number: 2.7182818246
print('\n')
print(pow(e, 1) == exp(log(e)))
print(pow(2,2) == exp(2*log(2)))
print(log(e,e) == exp(0))



import math
result = (pow(32,6,5)) == (32**6)%5 
print(result)



from math import fabs, log

print("\n")
number = 2e-7 #fabs used to calculate absolute value 
print("Log of the absolute value of 2e-7 is ", log(fabs(number)))



import math
print("\n")
result = math.e == math.exp(1) # used to calculate the power of e ie e^y
print(result)



from math import ceil, floor, trunc

x = 1.4
y = 2.6

# Ceil method returns the greater than or equal value to x 
# floor method returns the less than or equal value to x

print('\n')
print(floor(x), floor(y))
print(floor(-x), floor(-y))
print(ceil(x), ceil(y))
print(ceil(-x), ceil(-y))
print(trunc(x), trunc(y))
print(trunc(-x), trunc(-y))
