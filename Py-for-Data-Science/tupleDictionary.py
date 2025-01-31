my_tup = (1, 2, 3)
print(my_tup[2])


tup = 1, 2, 3
a, b, c = tup

print(a * b * c)


my_dictionary = {"A":1, "B":2}
copy_my_dictionary = my_dictionary.copy()
my_dictionary.clear()

print(copy_my_dictionary)



colors = {
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "red": (255, 0, 0),
    "green": (0, 128, 0)
}

for col, rgb in colors.items():
    print(col, ":", rgb)