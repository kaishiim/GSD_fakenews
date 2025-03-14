<<<<<<< HEAD
print("Hello")
print("hej")
=======
import re

def clean_text(text):
    #Replaces text to lowercase
    text = text.lower()
    #Replcaing spaces/lines:
    text = re.sub(r'\s+', ' ', text)
    #Replacing numbers:
    text = re.sub(r'\d+', '<NUM>', text)
    #Replacing dates:
    text = re.sub(r'\d{4}-\d{2}-\d{2}', '<DATE>', text)
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '<DATE>', text)
    #Replacing emails:
    text = re.sub(r'\S+@\S+\.\S+', '<EMAIL>', text)
    #Replacing urls:
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)
    return text
>>>>>>> 99003223ca8499c96c17303733efd0e92dabadff
