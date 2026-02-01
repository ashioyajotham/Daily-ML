largest_number = -99999999
 
 #Input the first value
number = int(input('Enter a number or type -1 to stop: '))

while number != -1:
     if number > largest_number:
         largest_number = number #Update largest_number
     number = int(input('Enter a number or type -1 to stop: '))


print('The largest number is: ',largest_number)

