#Read the numbers
number1 = int(input('Enter the first number: '))
number2 = int(input('Enter the second number: '))
number3 = int(input('Enter the third number:'))

#Check which of the numbers the largest
#and pass it to the largest_number variable

largest_number = max(number1, number2, number3)

#print the results
print("The largest number is: ",largest_number)

#By the same fashion you can use the min() function