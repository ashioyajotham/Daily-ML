my_list = [x * x for x in range (5)]

def fun(lst):
    del lst[lst[2]]
    return lst

print (fun(my_list))




lst = [[x for x in range(3)]for y in range(3)]
for r in range(3):
    for c in range(3):
        if lst[r][c] % 2 != 0:
            print("#")