my_list = [17, 3, 11, 5, 1, 9, 7, 15, 13]
largest = my_list[0]

for i in range (1, len(my_list)):
    if my_list[i] > largest:
        largest = my_list[i]

print(largest)
