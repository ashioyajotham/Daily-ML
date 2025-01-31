def multiply(a, b):
    return a * b

print(multiply(3, 4))


def multiply():
    return 

print(multiply(3, 4))


#The result of a function can easily be assigned to a variable
def wishes():
    return "Happy Birthday!"

w = wishes()

print(w)


def wishes():
    print("My wishes")
    return "Happy Birthday!"

wishes()


def wishes():
    print("My wishes")
    return "Happy Birthday!"


print(wishes())


#You can use a list as a function's argument
def hi_everybody(my_list):
    for name in my_list:
        print("Hi",name)

hi_everybody(["Adam","John","Lucy"])


#A list can be a function too
def create_list(n):
    my_list = []
    for i in range (n):
        my_list.append(i)
        return my_list

print(create_list(5))

