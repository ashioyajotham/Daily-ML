def rerturn_42():
    return 42 #An explicit return statement

rerturn_42() #The caller code gets 42



num = rerturn_42()
num

rerturn_42() * 2

rerturn_42() + 5


def get_even(numbers):
    even_nums = [num for num in numbers if not num % 2]
    return even_nums

    get_even([1, 2, 3, 4, 5, 6])


def get_even(numbers):
    return [num for num in numbers if not num % 2]
    
    get_even([1, 2, 3, 4, 5, 6])


def mean(sample):
    return num (sample) / len(sample)

mean([1, 2, 3, 4])

