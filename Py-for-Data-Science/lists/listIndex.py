#list indexing
n_list = ["Happy", [2, 0, 1, 5]]

#Nested Indexing
print(n_list[0][1])
print(n_list[1][3])


fam = ["liz", 1.73, "emma", 1.68, "mom", 1.71, "dad", 1.89]
fam
['liz', 1.73, 'emma', 1.68, 'mom', 1.71, 'dad', 1.89]
fam[3]
1.68

# Subsetting lists
['liz', 1.73, 'emma', 1.68, 'mom', 1.71, 'dad', 1.89]
fam[6]
'dad'
fam[-1]
1.89
fam[7]
1.89

#Subsetting lists
['liz', 1.73, 'emma', 1.68, 'mom', 1.71, 'dad', 1.89]
fam[
6
]
'dad'
fam[
-1
]
# <-
1.89
fam[
7
]
# <-
1.89



# Subsetting list of lists
x = [["a", "b", "c"],
     ["d", "e", "f"],
     ["g", "h", "i"]]

print("\n")    
print(x[2][0])
print(x[2][:2])
