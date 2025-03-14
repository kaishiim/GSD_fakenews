# Part 1
## Task 1
import re
import nltk
from nltk.tokenize import word_tokenize

def clean_text(text):
    #Replaces text to be lowercase.
    text = text.lower()
    #Removing spaces/lines.
    text = re.sub(r'\s+', ' ', text)
    #Replacing numbers with NUM.
    text = re.sub(r'\d+', 'NUM', text)
    #Replacing dates with DATE.
    #text = re.sub(r'\d{4}-\d{2}-\d{2}', 'DATE', text)
    #text = re.sub(r'\d{2}/\d{2}/\d{4}', 'DATE', text)
    # Erstat datoer i forskellige formater (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, osv.)
    text = re.sub(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b', '<DATE>', text)

    #Replacing emails with EMAIL.
    text = re.sub(r'\S+@\S+\.\S+', 'EMAIL', text)
    #Replacing urls with URL.
    text = re.sub(r'https?://\S+|www\.\S+', 'URL', text)

    # Tokenization: Opdeling af teksten i ord
    tokens = word_tokenize(text)
    
    # Returnerer tokens som en string, så de kan gemmes i CSV
    return "[" + ", ".join(f"'{token}'" for token in tokens) + "]"  

import pandas as pd

url = "https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv"

dataframe = pd.read_csv(url)

dataframe_cleaned = dataframe.map(lambda x: clean_text(str(x)))
print(dataframe_cleaned.head(10))

dataframe_cleaned.to_csv("cleaned_dataset.csv", index=False)

#Part 2
#Part 3
#Part 4