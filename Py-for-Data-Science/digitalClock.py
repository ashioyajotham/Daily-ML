import time

while True:
    localtime = time.localtime()
    result = time.strftime('%I:%M:%S %p', localtime)
    print(result)
    time.sleep(1) #delays the condition for a second
    #ctrl +c to break the loop
    