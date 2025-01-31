pol_eng_dictionary = {
    "kwiat": "flower",
    "woda" : "water",
    "gleba": "soil"
    }

item_1 = pol_eng_dictionary["gleba"]
print(item_1)

item_2 = pol_eng_dictionary.get("woda")
print(item_2)

#If you want to change the value associated with a specific key, 
# you can do so by referring to the item's key 
pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

pol_eng_dictionary["zamek"] = "lock"
item = pol_eng_dictionary["zamek"]
print(item) 




#To add or remove a key (and the associated value)
phonebook = {}

phonebook["Adam"] = 53421674
print(phonebook)

del phonebook['Adam']
print(phonebook)



# You can also insert an item to a dictionary by using the update () method
# and remove the last element using popitem()
pol_eng_dictionary = {
    "kwiat": "flower"
    }

pol_eng_dictionary.update({"gleba": "soil"})
print(pol_eng_dictionary)

pol_eng_dictionary.popitem()
print(pol_eng_dictionary)



# You can use the for loop to loop through a directory 
pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

for item in pol_eng_dictionary:
    print(item)



# If you want to loop through a dictionary's keys and values, 
# you can use the keys and values 
pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

for key, value in pol_eng_dictionary.items():
    print("Pol/Eng ->", key, ":", value)




pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

if "zamek" in pol_eng_dictionary:
    print("Yes")
else:
    print("No")



pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

print(len(pol_eng_dictionary))
del pol_eng_dictionary["zamek"]
print(len(pol_eng_dictionary))

pol_eng_dictionary.clear()
print(len(pol_eng_dictionary))

del pol_eng_dictionary


#To copy use the copy()
pol_eng_dictionary = {
    "zamek": "castle",
    "woda" : "water",
    "gleba": "soil"
    }

copy_dictionary = pol_eng_dictionary.copy()
