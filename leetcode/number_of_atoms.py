"""
Given a string formula representing a chemical formula, return the count of each atom.

The atomic element always starts with an uppercase character, then zero or more lowercase letters, representing the name.

One or more digits representing that element's count may follow if the count is greater than 1. If the count is 1, no digits will follow.

For example, "H2O" and "H2O2" are possible, but "H1O2" is impossible.
Two formulas are concatenated together to produce another formula.

For example, "H2O2He3Mg4" is also a formula.
A formula placed in parentheses, and a count (optionally added) is also a formula.

For example, "(H2O2)" and "(H2O2)3" are formulas.
Return the count of all elements as a string in the following form: the first name (in sorted order), followed by its count (if that count is more than 1), followed by the second name (in sorted order), followed by its count (if that count is more than 1), and so on.

The test cases are generated so that all the values in the output fit in a 32-bit integer.

 

Example 1:

Input: formula = "H2O"
Output: "H2O"
Explanation: The count of elements are {'H': 2, 'O': 1}.
Example 2:

Input: formula = "Mg(OH)2"
Output: "H2MgO2"
Explanation: The count of elements are {'H': 2, 'Mg': 1, 'O': 2}.
Example 3:

Input: formula = "K4(ON(SO3)2)2"
Output: "K4N2O14S4"
Explanation: The count of elements are {'K': 4, 'N': 2, 'O': 14, 'S': 4}.
 

Constraints:

1 <= formula.length <= 1000
formula consists of English letters, digits, '(', and ')'.
formula is always valid.
"""

# Approach
# 1. Parse the chemical formula character by character
# 2. If the character is an uppercase letter, then it is the start of a new element
# 3. If the character is a lowercase letter, then it is the continuation of the element
# 4. If the character is a digit, then it is the count of the element
# 5. If the character is an opening parenthesis, then it is the start of a new formula
# 6. If the character is a closing parenthesis, then it is the end of the formula
# 7. Use a stack to handle the nested formulas
# 8. Use a counter to store atom frequencies
# 9. Sort the atom frequencies by atom name and format the output

from collections import Counter

class Solution:
    def countOfAtoms(self, formula: str) -> str:
        def parse_number(i):
            num = 0
            while i < len(formula) and formula[i].isdigit():
                num = num * 10 + int(formula[i])
                i += 1
            return i, max(1, num)
        
        def parse_atom(i):
            atom = formula[i]
            i += 1
            while i < len(formula) and formula[i].islower():
                atom += formula[i]
                i += 1
            return i, atom
        
        stack = [Counter()]
        i = 0
        
        while i < len(formula):
            if formula[i] == '(':
                stack.append(Counter())
                i += 1
            elif formula[i] == ')':
                i += 1
                i, multiplier = parse_number(i)
                inner = stack.pop()
                for atom, count in inner.items():
                    stack[-1][atom] += count * multiplier
            elif formula[i].isupper():
                i, atom = parse_atom(i)
                i, count = parse_number(i)
                stack[-1][atom] += count
        
        result = []
        for atom in sorted(stack[0].keys()):
            result.append(atom)
            if stack[0][atom] > 1:
                result.append(str(stack[0][atom]))
                
        return ''.join(result)