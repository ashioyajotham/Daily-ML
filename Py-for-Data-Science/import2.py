#You can change the name of the imported entity by using the as phrase of the import

import math as m
 
print(m.sin(m.pi/2))


import os
os.mkdir("pictures")
os.chdir("pictures")
os.mkdir("thumbnails")
os.chdir("thumbnails")
os.mkdir("tmp")
os.chdir("../")
print(os.getcwd())


