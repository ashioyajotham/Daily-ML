x = '1'

if x==1:
    print('one')
elif x=='1':
    if int(x) > 1:
        print("two")
    elif int(x) < 1:
        print("three")
    else:
        print('four')
if int(x) == 1:
    print('five')
else:
    print('six')