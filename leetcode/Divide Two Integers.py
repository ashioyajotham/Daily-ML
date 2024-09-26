"""
Given two integers dividend and divisor, divide two integers without using multiplication, division, and mod operator.

The integer division should truncate toward zero, which means losing its fractional part. For example, 8.345 would be truncated to 8, and -2.7335 would be truncated to -2.

Return the quotient after dividing dividend by divisor.

Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: [−231, 231 − 1]. For this problem, if the quotient is strictly greater than 231 - 1, then return 231 - 1, and if the quotient is strictly less than -231, then return -231.

 

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = 3.33333.. which is truncated to 3.
Example 2:

Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = -2.33333.. which is truncated to -2.
 

Constraints:

-231 <= dividend, divisor <= 231 - 1
divisor != 0
"""
# Action Plan
# 1. Check if the dividend is 0, return 0.
# 2. Check if the divisor is 1, return the dividend.
# 3. Check if the divisor is -1, return the negative of the dividend.
# 4. Check if the dividend and divisor have the same sign.
# 5. If they have the same sign, return the result.
# 6. If they have different signs, return the negative of the result.
# 7. Time complexity is O(log n) where n is the dividend.
# 8. Space complexity is O(1).

class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        if dividend == 0:
            return 0
        if divisor == 1:
            return dividend
        if divisor == -1:
            return -dividend
        sign = (dividend < 0) == (divisor < 0)
        dividend = abs(dividend)
        divisor = abs(divisor)
        result = 0
        while dividend >= divisor:
            temp, i = divisor, 1
            while dividend >= temp:
                dividend -= temp
                result += i
                i <<= 1
                temp <<= 1
        if not sign:
            result = -result
        return min(max(-2**31, result), 2**31 - 1)