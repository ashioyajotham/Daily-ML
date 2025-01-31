# break - eaxample

print ('The break instruction:')
for i in range(1,6):
    if i == 3:
        break
    print('Inside the loop.', i)
print('outside the loop.')

#Break terminates the current loop and resumes execution at the next statement, 
# just like the traditional break statement in C