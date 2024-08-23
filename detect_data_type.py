import re
from datetime import datetime

# Detect the data type of the csv file column
def detect_data_type(value):
    # Convert the value to string for easy handling
    value = str(value)
    
    # Check if integer
    try:
        int(value)
        return "Integer"
    except ValueError:
        pass
    
    # Check if float
    try:
        float(value)
        return "Float"
    except ValueError:
        pass
    
    # Check if date
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return "Date"
    except ValueError:
        pass

    # Check if email
    if re.match(r'^\S+@\S+\.\S+$', value):
        return "Email"
    
    # Check if IP address
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
        return "IP Address"

    # Check if US SSN 
    if re.match(r'^\d{3}-\d{2}-\d{4}$', value):
        return "us_ssn"

    # Add more data type checks here as needed
    # If none of the above, assume it's a string
    return "String"
