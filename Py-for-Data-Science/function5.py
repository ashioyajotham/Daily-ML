def adding (a, b, c):
    print(a, "+", b, "+", c, "=", a + b + c)

a = int(input("Enter your value: "))
b = int(input("Enter your value: "))
c = int(input("Enter your value: "))

adding(a, b, c)


import re

addressToVerify ='info@scottbrady91.com'
match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

if match == None:
	print('Bad Syntax')
	raise ValueError('Bad Syntax')
