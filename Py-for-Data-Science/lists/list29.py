#Using for loops to create lists

#Instantiate an empty loop
squares = []

#Loop over an iterable or range of elements
for i in range(10):
    #Append ech element to the end of the list
    squares.append(i * i)
print(squares)




#Using list comprehension
squares = [i * i for i in range(10)]
print(squares)


h_letters = []

for letter in "human":
    h_letters.append(letter)

print(h_letters)

h_letters = [letter for letter in 'human']
print(h_letters)
