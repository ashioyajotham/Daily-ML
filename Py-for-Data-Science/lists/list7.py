lst = [1, 2, 3, 4, 5]
lst_2 = []
add = 0

for number in lst:
    add += number #Perform an addition(inside the loop body) between the current 
    # value of iteration variable, number and the current value stored in lst(defined outside 
    #  the body)
    lst_2.append(add)

print(lst_2)