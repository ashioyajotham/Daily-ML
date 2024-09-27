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
class Solution:
    def isNumber(self, s: str) -> bool:
        # {state: {char_type: state}}
        transitions = {
            'Start': {'digit': 'Integer', 'sign': 'Sign', 'dot': 'Dot'},
            'Sign': {'digit': 'Integer', 'dot': 'Dot'},
            'Integer': {'digit': 'Integer', 'dot': 'Fraction', 'e': 'Exponent'},
            'Dot': {'digit': 'Fraction'},
            'Fraction': {'digit': 'Fraction', 'e': 'Exponent'},
            'Exponent': {'digit': 'Exp_number', 'sign': 'Exp_sign'},
            'Exp_sign': {'digit': 'Exp_number'},
            'Exp_number': {'digit': 'Exp_number'}
        }
        
        valid_end_states = {'Integer', 'Fraction', 'Exp_number'}

        def get_char_type(char):
            if char.isdigit():
                return 'digit'
            if char in '+-':
                return 'sign'
            if char in 'eE':
                return 'e'
            if char == '.':
                return 'dot'
            return None

        current_state = 'Start'

        for char in s:
            char_type = get_char_type(char)
            if not char_type or char_type not in transitions[current_state]:
                return False
            current_state = transitions[current_state][char_type]

        return current_state in valid_end_states
    
# From the above code, we can deduce the action plan:
# 1. Create a dictionary to keep track of the transitions.
# 2. Create a set to keep track of the valid end states.
# 3. Create a function to get the character type.
# 4. Initialize the current state to 'Start'.
# 5. Traverse through the string and get the character type.
# 6. If the character type is not valid or not in the transitions, return False.
# 7. Update the current state.
# 8. Return True if the current state is in the valid end states.