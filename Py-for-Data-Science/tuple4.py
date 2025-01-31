tup = (1, 2, 4, 8)
tup = tup[-2:-1]
tup = tup[-1]
print(tup)


my_tup = (0,1,2,3,4,5,6)
foo = list(filter(lambda x: x-0 and x-1, my_tup))
print(foo)

my_list = [1,2,3]
foo = tuple(map(lambda x: x**x, my_list))
print(foo)
