# return without an expression

def happy_new_year(wishes = True):
    print("Three...")
    print("Two...")
    print("One...")
    if not wishes:
        return

    print("Happy New Year")


# Return with an expression
def boring_function():
    return 123

x = boring_function

print("The boring_function has returned its result. It's ", x)


def boring_function():
    print("'Boredom Mode' ON.")
    return 123

print("This lesson is interesting!")
boring_function()
print('This lesson is boring...')






