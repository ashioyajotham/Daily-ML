# Task 1 

# Sum of integers in a list
def sum_list(lst):
    """Returns the sum of all integers in a list"""
    
    # Initialize variable to store sum
    total = 0 
    
    # Iterate through list
    for num in lst:
      
        # Add current number to total
        total += num
        
    # Return final sum    
    return total

# Return larger of two numbers
def larger_num(num1, num2):
    """Returns the larger of two numbers"""
   
    # Compare num1 and num2
    if num1 > num2:
      
        # If num1 is larger, return it
        return num1
    
    else: 
       
        # Otherwise, num2 must be larger (or equal)
        return num2

# Count vowels in a string
def count_vowels(string):
    """Returns the number of vowels in a string"""
  
    # String containing all vowels
    vowels = "aeiouAEIOU" 
  
    # Initialize vowel count variable
    count = 0
  
    # Iterate through string 
    for char in string:
      
        # Check if character is a vowel
        if char in vowels:
          
          # Increment count if vowel  
          count += 1
            
    # Return final vowel count    
    return count

# Filter strings longer than 5 characters
def filter_long_strings(lst):
    """Returns list of strings longer than 5 characters"""
    
    # Initialize empty list to hold long strings
    long_strings = []
    
    # Iterate through list
    for string in lst:
      
        # Check if string length is over 5
        if len(string) > 5:
        
          # Add long string to list  
          long_strings.append(string)
            
    # Return list of long strings
    return long_strings

# Sort list of integers in descending order
def sort_desc(lst):
    """Sorts a list of integers in descending order"""
    
    # Call sort method on list
    # Set reverse=True to sort in descending order
    lst.sort(reverse=True)
    
    # Return sorted list
    return lst