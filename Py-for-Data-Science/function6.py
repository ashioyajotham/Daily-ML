

def introduction (first_name, last_name = "Smith"): 
    print("Hello, my name is ", first_name, last_name)

first_name = input("Enter your first name please:　")

introduction(first_name, last_name="Smith")



#You can use the keyword argument passing technique 
# to pre-define a value for a given argument

def name(first_name, last_name = "Smith"):
    print(first_name, last_name)

name("Andy")
name("Betty", "Johnson")
