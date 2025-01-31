#Platform lets you dive into the underlying layers of the OS and hardware allowing you 
# to knnow more about the environment in which your code is executed.

from platform import platform

print('\n')
#Displaying platform information
print(platform())
print(platform(1))
print(platform(0,1))



import platform
print("\n")
print("Platform processor:", platform.processor()) #Displays platform processor


from platform import system
print("\n")
# Displaying the OS name
print(platform.system())



import platform
print("\n")
#Display platform architecture - returns a tuple that stores information
# about the bit architecture(number of bits in the platform architecture)
# and linkage format(defines how names can or cannot refer to the same entity 
# throughout the whole program or whole translation unit)
print("Platform architecture:", platform.architecture())


from platform import version
print("\n")
print(platform.python_version())



import platform
print("\n")
#Display the machine type ie info that tells the width or size of 
# registers available in the core
print(platform.machine())



import platform
print('\n')
# Displays node ie the systems's network name
print("System's network name:", platform.node())


from platform import python_implementation, python_version_tuple
print("\n")
print(python_implementation())

for atr in python_version_tuple():
    print(atr)



import platform
print('\n')
# Display python build date and number
print("Python build date and number:", platform.python_build())



import platform
print('\n')
# Displays python's compiler
print("Python compiler is ", platform.python_compiler())



import platform
print('\n')
# Displays branch or Source Code Manager(SCM) used to track revisions
print("Python SCM:", platform.python_compiler())



import platform
# Display additional info about Windows OS
# release, version, csd, ptype
print(platform.win32_ver())







