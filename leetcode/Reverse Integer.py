"""
Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

 

Example 1:

Input: x = 123
Output: 321
Example 2:

Input: x = -123
Output: -321
Example 3:

Input: x = 120
Output: 21
 

Constraints:

-231 <= x <= 231 - 1
"""

# Approach:
# 1. Convert the integer to string
# 2. Check if the integer is negative or positive
# 3. If negative, remove the negative sign and reverse the string
# 4. If positive, reverse the string
# 5. Convert the string to integer
# 6. Check if the integer is within the range of 32-bit signed integer
# 7. Return the integer

class Solution:
    def reverse(self, x: int) -> int:
        if x < 0:
            x = int(str(x)[1:][::-1]) * -1
        else:
            x = int(str(x)[::-1])
        
        if x < -2**31 or x > 2**31 - 1:
            return 0
        
        return x