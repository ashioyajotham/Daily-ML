# You can pass info to functions using parameters

# A one-name parameter
def hi(name):
    print("Hi", name)

#You can use the keyword argument passing technique 
# to pre-define a value for a given argument

hi("Greg")


# A two-parameter function
def hi_all (name_1, name_2):
    print("Hi", name_1)
    print("Hi", name_2)

hi_all("Victor", "Ashioya")


# A three-parameter function
def address (street, city, postal_code):
    print("Your address is ", street, "St...", city, postal_code)

s = input("Street: ")
p_c = input("Postal code: ")
c = input("City: ")

address(s, p_c, c)
