def intro(a = "James Bond", b = "Bond"):
    print("My name is ", b + ".", a + ".")

intro(b = "Sean Connery")


def intro(a, b = "Bond"):
    print("My name is ", b + ".", a + ".")

intro("Susan")


def add_numbers(a, c, b = 2):
    print(a + b + c)

add_numbers(a = 1, c = 3)


