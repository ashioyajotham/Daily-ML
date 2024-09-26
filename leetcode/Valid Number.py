"""
Given a string s, return whether s is a valid number.

For example, all the following are valid numbers: "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789", while the following are not valid numbers: "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53".

Formally, a valid number is defined using one of the following definitions:

An integer number followed by an optional exponent.
A decimal number followed by an optional exponent.
An integer number is defined with an optional sign '-' or '+' followed by digits.

A decimal number is defined with an optional sign '-' or '+' followed by one of the following definitions:

Digits followed by a dot '.'.
Digits followed by a dot '.' followed by digits.
A dot '.' followed by digits.
An exponent is defined with an exponent notation 'e' or 'E' followed by an integer number.

The digits are defined as one or more digits.

 

Example 1:

Input: s = "0"

Output: true

Example 2:

Input: s = "e"

Output: false

Example 3:

Input: s = "."

Output: false

 

Constraints:

1 <= s.length <= 20
s consists of only English letters (both uppercase and lowercase), digits (0-9), plus '+', minus '-', or dot '.'.

"""
# Action Plan
# 1. Remove the leading and trailing whitespaces.
# 2. Create a function to check if the string is a number.
# 3. Create a function to check if the string is an integer.
# 4. Create a function to check if the string is a decimal.
# 5. Create a function to check if the string is an exponent.
# 6. Check if the string is a number.
# 7. Time complexity is O(n) where n is the length of the string.

class Solution:
    def isNumber(self, s: str) -> bool:
        s = s.strip()
        def is_number(s):
            return is_integer(s) or is_decimal(s) or is_exponent(s)
        def is_integer(s):
            if not s:
                return False
            if s[0] in ['+', '-']:
                s = s[1:]
            return s.isdigit()
        def is_decimal(s):
            if not s:
                return False
            if s[0] in ['+', '-']:
                s = s[1:]
            if '.' not in s:
                return False
            left, right = s.split('.')
            return (left.isdigit() or not left) and right.isdigit()
        def is_exponent(s):
            if not s:
                return False
            if 'e' not in s and 'E' not in s:
                return False
            left, right = s.split('e') if 'e' in s else s.split('E')
            return is_number(left) and is_integer(right)
        return is_number(s)