dictionary = {}
my_list = ['a', 'b', 'c', 'd']

for i in range(len(my_list)-1):
    dictionary[my_list[i]] = (my_list[i],)

for i in sorted(dictionary.keys()):
    k = dictionary[i]
    print(k[0])



dictionary = {'one': 'two', 'three':'one', 'two':'three'}
v = dictionary['three']

for k in range(len(dictionary)):
    v = dictionary[v]

print(v)