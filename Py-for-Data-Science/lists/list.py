numbers = [10, 5, 7, 2, 1] #a list containing five numbers
#Elements are numbered from 0 so the last number above is four(Indexing)
print("Original list content: ", numbers)

numbers[0] = 111
print("\nPrevious list content: ", numbers) #Printing previous list

numbers[1] = numbers[4] #Copying value of the fifth element to the second element
print("Previous list content: ", numbers)
# To preventing copying a list, use list() or [:] (explicit copy)
print("\nList length: ", len(numbers)) #printing the list length



areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Explicit copy
areas_copy = list(areas)
areas_copy = areas[:]
areas_copy[0] = 5.0
print("\n")
print(areas)



areas = [11.25, 18.0, 20.0, 10.75, 9.50]
# Explicit copy
areas_copy[0] = 5.0
print("\n")
print(areas)

del numbers[1] #Removing the second element from the list
print("New list's length: ", len(numbers)) #printing new list
#len returns the number of items in an object. When the object is asrting, 
# it returns the number of characters in the string

hall=11.25
kit=18.25
liv=20.0
bed=10.75
bath=9.50
areas = [hall,kit,liv,bed,bath]
print(areas)

# Adapt list 
areas = ["hallway", hall, "kitchen", kit, liv, "bedroom", bed, bath]
print(areas)


# Lists of lists
house = [["hallway", hall], \
         ["kitchen", kit],\
         ["living room", liv],\
         ["bedroom", bed], \
         ["bathroom", bath]]
print(house)
print(type(house))




