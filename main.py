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

print("Amounts:", extract_amount(full_text))
print("Dates:", extract_date(full_text))