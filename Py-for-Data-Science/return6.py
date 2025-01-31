def strange_function(n):
    if (n % 2 == 0):
        return True


def list_sum(lst):
    s = 0

    for elem in lst:
        s += elem
    return s



def strange_list_fun(n):
    strange_list = []

    for i in range(0, n):
        strange_list.insert(0, i)

    return strange_list
print(strange_list_fun(5))