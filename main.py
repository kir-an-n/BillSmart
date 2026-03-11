import easyocr
import re

reader = easyocr.Reader(['en'])
result = reader.readtext('receipt.jpeg')

full_text = ' '.join([detection[1] for detection in result])

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
    elif any(word in text_lower for word in ['grocery', 'vegetables', 'fruits', 'rice']):
        return 'Grocery'
    elif any(word in text_lower for word in ['medical', 'pharmacy', 'medicine', 'hospital']):
        return 'Medical'
    else:
        return 'Other'

print("Amounts:", extract_amount(full_text))
print("Dates:", extract_date(full_text))
print("Category:", categorize_expense(full_text))


import pandas as pd
from datetime import datetime

def save_to_csv(amounts,category, dates):
    data={

        'date': [dates[0] if dates else datetime.now().strftime('%d-%m-%Y')],
        'amounts': [', '.join(amounts)],
        'total':[amounts[-1] if amounts else '0'],
        'category': [category]

    }

    df=pd.DataFrame(data)
    df.to_csv('expensses.csv', mode='a', header=not pd.io.common.file_exists('expenses.csv'), index=False)
    print("Saved!")
    
save_to_csv(extract_amount(full_text), categorize_expense(full_text), extract_date(full_text))