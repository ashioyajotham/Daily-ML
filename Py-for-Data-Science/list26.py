
lst = [1, 2, 3]
for v in range(len(lst)):
    lst.insert(1, lst[v])
print(lst)

my_list = [1,2]

for v in range(2):
    my_list.insert(-1, my_list[v])

print(my_list)