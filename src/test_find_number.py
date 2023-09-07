import re

def find_last_number(text):
    # The regex pattern to match any number (integer or floating-point)
    pattern = r'\d+(?:\.\d+)?'
    
    # Using findall to get all occurrences of numbers in the string
    all_numbers = re.findall(pattern, text)
    
    # If there are no numbers in the string, return None
    if not all_numbers:
        return None
    
    # Return the last number found in the string
    return all_numbers[-1]

text = "There are 2 apples, 3 oranges, and 5.5 pineapples."
last_number = find_last_number(text)
print(f"The last number in the text is: {last_number}")