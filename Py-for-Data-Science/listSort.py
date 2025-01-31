lst = [5, 3, 1, 2, 4]
print(lst)

lst.sort()
print(lst)


first = [11.25, 18.0, 20.0]
second = [10.75, 9.50]

# Sorted takes three arguments: iterable, key and reverse
# Key=None means that if you don't specify the key argument, it will be none
# Reverse=false means that if you don't specify the reverse argument it will be false

full = first + second # Merge the two lists

# Sort full in descending order
full_sorted = sorted(full, reverse = True)
print("\n")
print(full_sorted)