#Initialize list
List = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#Show original list
print("\nOriginal List: \n", List)

print("\nSliced Lists: ")

#Creating new list 
newList = List[:3] + List[7:]

#Display sliced list
print(newList)

#Changing existing list
List = List[::2] + List[1::2]

#Display sliced list
print(List)

