# Python module search path
import sys
sys.path
['',
'C:\\Python33\\Lib\\idlelib',
'C:\\Windows\\system32\\python33.zip',
'C:\\Python33\\DLLs',
'C:\\Python33\\lib',
'C:\\Python33',
'C:\\Python33\\lib\\site-packages'
]



import sys
#p in sys.path:
#print(p)


# Access function from a module at the top of package
from sys import path
path.append("...\\packages")
#import extra.iota
#print(extra.iota.funI())



# Relative imports 
#from .some_module import some_class
#from..some_package import some_function
#from . import some_class



# Consider
            #Project
               #package1
                   #module1.py
                   #module2.py
               #package2
                   #__init_.py
                   #module3.py
                   #module4.py
                   #subpackage1
                       #module5.py

#package1/module2.py contains a function, function1
#package2/_init_.py contains a class, class1
#package2/subpackage1/module5.py contains a function, function, function2

#You can import function1 into the package1/module1.py file this way
 #from .module2 import function1
 
#You can import class1 and function2 into the package2/module3.py this way
 #from . import class1
 #from .subpackage1.module5 import function2

# Importing a package esentially imports the package's _init_.py file as a module
# Subpackage1 is in the same directory as the current module, which is module3.py
