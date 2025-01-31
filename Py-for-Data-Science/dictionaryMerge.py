dict1 = {"Alexandra": 27,
         "Shwlina Gomez": 22,
         "James": 29,
         "Peterson": 27
            }

dict2 ={"Jasmine": 19,
        "Maria": 26,
        "Helena": 30

}

print("Before merging the two dictionaries")
print("Dictionary 1 is ", dict1)
print("Dictionary 2 is ", dict2)

dict3 = dict1.copy()

for key, value in dict2.items():
    dict3[key] = value

print("After merging the two dictionary")
print(dict3)





# Using copy() and for loop
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

d3 = d1.copy()

for key, value in d2.items():
    d3[key] = value

print(d3)


# Using the update() method
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d1.update(d2)
print(d1)

# Using the function
def merge_twoDict(d1, d2):
    return(d1.update(d2))
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}

merge_twoDict(d1,d2)
print(d1)


# Using both copy and update
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

d3 = d1.copy()

d3.update(d2)

print(d3)

# Using the unpacking operator(**)
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

d3 = {
    **d1, **d2
}

print(d3)

# Using the dict() constructor and **kwargs
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

d3 = dict(dict1, **dict2)
print(d3)

# Using the collections - chainMap function
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

from collections import ChainMap
d3 = dict(ChainMap(d1, d2))

print(d3)

# Using the itertools - chain() method
d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = {}

from itertools import chain
d3 =  dict(chain(d1.items(), d2.items()))

print(d3)

# Using the merge (|)operator
def merge (d1, d2):
    result = d1 | d2
    return

d1 = {'Adam Smith': 'A', 'Judy Paxton': "B+"}
d2 = {'Mary Louis': 'A', 'Patrick Wilson': "C"}
d3 = merge(d1, d2)

print(d3)












