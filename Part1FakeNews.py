# Part 1
## Task 1
import re
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')

#Her initialiserer vi stopwords til, at fjerne 
stop_words = set(stopwords.words('english'))
#Her initialiserer vi stemmer til, at reducerer ordenes længde.
stemmer = PorterStemmer()

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
    # Her fjerner vi stopwords fra vores csv fil.
    tokens = [word for word in tokens if word not in stop_words]
    # Her tilføjer vi stemmer, som reducerer længden af ordene.
    tokens = [stemmer.stem(word) for word in tokens]

    # Returnerer tokens som en string, så de kan gemmes i CSV
    return "[" + ", ".join(f"'{token}'" for token in tokens) + "]"  

import pandas as pd

url = "https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv"

dataframe = pd.read_csv(url)

dataframe_cleaned = dataframe.map(lambda x: clean_text(str(x)))
print(dataframe_cleaned.head(10))

dataframe_cleaned.to_csv("cleaned_dataset.csv", index=False)

# Læs CSV-fil
file_path = r"C:\Users\yifan\Downloads\995,000_rows (1).csv"
df = pd.read_csv(file_path, low_memory=False)

df_cleaned = df.map(lambda x: clean_text(str(x)))

print(df_cleaned.head(10))

# Gem forbehandlede data
df_cleaned.to_csv("processed_995K_FakeNewsCorpus.csv", index=False)

#df['processed_text'] = df['content'].astype(str).apply(clean_text)

#Part 2
#Part 3
#Part 4