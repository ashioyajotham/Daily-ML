#Positional argument passing in which the order of arguments passed matters

def subtra(a, b):
    print(a - b)
    print("\n")

subtra(5, 2)
subtra(2, 5)


#Keyword (named) argument passing in which the order of arguments passed doesn't matters

def subtra(a, b):
    print(a - b)

subtra(a = 5, b = 2)
subtra(b = 2, a = 5)


#A mix of posional and keyword argument passing

def subtra(a, b):
    print(a - b)
    print("\n")

subtra(5, b = 2)
subtra(2, 5)




