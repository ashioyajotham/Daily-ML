print("\nThe continue instruction:")
for i in range(1,6):
    if i == 3:
        continue
    print('Inside the loop.', i)
print('Outside the loop.')

#continue is used to skip the rest of the code inside a loop for the current iteration only
#Loop doesn't terminate but continues with the next iteration