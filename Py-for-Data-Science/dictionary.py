dictionary = {"cat": "chat", "dog": "chien", "horse": "cheval"}
phone_numbers = {'boss': 5551234567, 'Suzy': 2265854310}
empty_dictionary = {}

print(dictionary)
print(phone_numbers)
print(empty_dictionary)

#In the first example, the dictionary uses keys and values which are both strings.
#In the second one, the keys are strings, but the values are integers. The reverse layout
# (keys - numbers, values - strings) is also possible, as well as number-number combination.

#The lists of pairs is surrounded by curly braces, while the pairs themselves are separated
# by commas and the keys and values by colons.

dictionary = {"cat": "chat", "dog": "chien", "horse": "cheval"}

for key in dictionary.keys():
    print (key, "->", dictionary[key])

dictionary = {"cat": "chat", "dog": "chien", "horse": "cheval"}

for english, french in dictionary.items():
    print (english, "->", french)


dictionary = {"cat": "chat", "dog": "chien", "horse": "cheval"}

dictionary['cat'] = 'minou'
print (dictionary)
