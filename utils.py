import re
from datetime import datetime

def extract_amount(text):
    amounts = re.findall(r'\d+[\.,]\d+', text)
    return amounts

def extract_date(text):
    dates = re.findall(r'\d{2}[\/\-]\d{2}[\/\-]\d{4}', text)
    return dates

def categorize_expense(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ['chicken', 'food', 'restaurant', 'kebab', 'naan', 'haldiram', 'drink']):
        return 'Food & Beverage'
    elif any(word in text_lower for word in ['grocery', 'supermarket', 'vegetables', 'fruits', 'rice']):
        return 'Grocery'
    elif any(word in text_lower for word in ['medical', 'pharmacy', 'medicine', 'hospital']):
        return 'Medical'
    else:
        return 'Other'