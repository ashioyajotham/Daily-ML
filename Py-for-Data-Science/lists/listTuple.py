# Method 1: Using tuple(list_name)
my_list = ["car", "Ford", "flower", "Tulip"]
def convert(my_list):
    return tuple(my_list)

print(convert(my_list))



# Method 2: Use a loop inside tuple
def convert(my_list):
    return tuple(i for i in my_list)

#Driver function
my_list = ["car", "Ford", "flower", "Tulip"]
print(convert(my_list))



# Method 3: Using (*list,)
def convert(my_list):
    return(*my_list,)

# Driver function
my_list = ["car", "Ford", "flower", "Tulip"]
print(convert(my_list))
