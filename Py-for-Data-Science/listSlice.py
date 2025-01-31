#list slicing 
lst =["p", "y", "t", "h", "o", "n"]

#Since slicing returns a list, slice assignment requires a list(or other iterable)
#Whatever portion of the list is returned by slice indexing, 
# that's the same portion that is changed by slice assignment
lst[2:4] = ["t", "r"] 
print(lst)

lst[2:4] = ["T", "H"]
print(lst)
#The assigned list (iterable) doesn't have to have the same length; the indexed
 #is simply sliced out and replaced en masse by whateverv is beng assigned

lst[2:4] = ["s", "p", "a", "m"]
print(lst)

# Syntax
# [start : end]
# inclusive  exclusive


areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]
downstairs = areas[:6]
upstairs = areas[6:]
print("\n")
print(downstairs)
print(upstairs)




