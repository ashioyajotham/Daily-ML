t = [[3 - i for i in range(3)]for j in range (3)]
s = 0
for i in range (3):
    s += t[i][i]
print(s)