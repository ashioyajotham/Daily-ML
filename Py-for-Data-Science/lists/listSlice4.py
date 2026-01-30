#Iniatilize list
List = [-999, 'G4G', 1706256, '^_^', 3.1496]

#Show original list
print('\nOriginal List: \n', List)

print('\nSliced Lists:　')

#Display sliced list
print(List[1:1:1])

#Display sliced list
print(List[-1:-1:-1])

#Display sliced list
print(List[:0:])

#If some slicing expressions are made that do not make sense or 
# are incomputable then empty lists are generated