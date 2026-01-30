my_list = [] #creating an empty list

for i in range(5):
    my_list.append(i + 1)

print(my_list)


numbers = [i*i for i in range(5)]
foo = list(map(lambda x: x//2, numbers))
print(foo)


numbers = [0,2,7,9,10]
foo = map(lambda num: num**2,numbers)
print(list(foo))