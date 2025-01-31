var = 17
var_right = var  >> 1
var_left = var << 2 
print(var, var_left, var_right)

#<< and >> are bitwise shift operators
#<< Returns x with the bits shifted to the left by y places(and new bits 
     # on the right hand side are zeros). This is the same as multiplying x by 2**y
#>> Returns x with the bits shifted to the right by y places. This is the same as //ing
     # x by 2**y