# Part 1
## Task 1
import re
import nltk
from nltk.tokenize import word_tokenize

def clean_text(text):
    # Konverter til små bogstaver
    text = text.lower()

    # Erstat e-mails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL', text)

    # Erstat URLs (http, https, www)
    text = re.sub(r'\b(?:https?://|www\.)\S+\b', 'URL', text)

    # Erstat datoer i forskellige formater (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, osv.)
    text = re.sub(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b', 'DATE', text)

    # Erstat tal (men ikke allerede erstattede datoer)
    text = re.sub(r'\b\d+\b', 'NUM', text)

    # Fjern ekstra mellemrum, tabulatorer og linjeskift
    text = re.sub(r'\s+', ' ', text).strip()

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