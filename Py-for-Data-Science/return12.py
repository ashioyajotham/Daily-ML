def bmi(weight, height):
    return weight / height ** 2

print(bmi(52.5, 1.65))


def bmi(weight, height):
    if height < 1.0 or height > 2.5 or \
        weight < 20 or weight > 200:
        return None

    return weight / height ** 2

print(bmi(352.5, 1.65))



def is_a_triangle(a, b, c):
    if a + b <= c:
        return False
    
    if b + c <= a:
        return False

    if c + a <= b:
        return False
    
print(is_a_triangle(1, 1, 1))
print(is_a_triangle(1, 1, 3))



def is_a_triangle(a, b, c):
    return a + b > c and b + c > a and c  + a > b

a = float(input("Enter the first side\'s length: "))
b = float(input("Enter the second side\'s length: "))
c = float(input("Enter the third side\'s length: "))

if is_a_triangle(a, b, c):
    print("Yes, it can be a triangle.")

else:
    print("No, it can\'t be a triangle.") 




def fib(n):
    if n < 1:
        return None
    if n < 3:
        return 1
    
    elem_1 = elem_2 = 1
    the_sum = 0
    for i in range (3, n + 1):
        the_sum = elem_1 + elem_2
        elem_1, elem_2 = elem_2, the_sum
    return the_sum

for n in range (1, 10):
    print(n, "->", fib(n))