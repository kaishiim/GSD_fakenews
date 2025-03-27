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

def clean_text(text, remove_stopwords=True, apply_stemming=True):
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
    
    # Fjern stopwords, hvis det er aktiveret
    if remove_stopwords:
        tokens = [word for word in tokens if word not in stop_words]

    # Stem ordene, hvis det er aktiveret
    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]

    # Returnerer tokens som en string, så de kan gemmes i CSV
    return "[" + ", ".join(f"'{token}'" for token in tokens) + "]"  

# Burde være 100% korrekt indtil her:
import pandas as pd

url = "https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv"

dataframe = pd.read_csv(url)

dataframe_cleaned = dataframe.map(lambda x: clean_text(str(x)))
print(dataframe_cleaned.head(10))

dataframe_cleaned.to_csv("cleaned_dataset.csv", index=False)


# Konverter alle tekstkolonner til én samlet tekststreng
full_text = " ".join(dataframe.astype(str).sum())

# Oprindelig ordforrådsstørrelse
original_tokens = set(word_tokenize(full_text.lower()))
original_vocab_size = len(original_tokens)

# Efter fjernelse af stopord
tokens_no_stopwords = set(clean_text(full_text, remove_stopwords=True, apply_stemming=False))
vocab_size_no_stopwords = len(tokens_no_stopwords)

# Efter stemming
tokens_stemmed = set(clean_text(full_text, remove_stopwords=True, apply_stemming=True))
vocab_size_stemmed = len(tokens_stemmed)

# Beregning af reduktionshastigheder
stopword_reduction = (original_vocab_size - vocab_size_no_stopwords) / original_vocab_size * 100
stemming_reduction = (vocab_size_no_stopwords - vocab_size_stemmed) / vocab_size_no_stopwords * 100

# Udskriv resultater
print(f"Oprindelig ordforrådsstørrelse: {original_vocab_size}")
print(f"Ordforrådsstørrelse efter fjernelse af stopord: {vocab_size_no_stopwords}")
print(f"Reduktionshastighed efter stopord: {stopword_reduction:.2f}%")
print(f"Ordforrådsstørrelse efter stemming: {vocab_size_stemmed}")
print(f"Reduktionshastighed efter stemming: {stemming_reduction:.2f}%")

#print("Stopwords liste:", stopwords)
#print("Antal stopord i listen:", len(stop_words))

#print("Før stopword fjernes:", word_tokenize(full_text.lower())[:50])
#print("Efter stopword fjernes:", clean_text(full_text, remove_stopwords=True, apply_stemming=False).split()[:50])

# Læs CSV-fil
#file_path = r"C:\Users\yifan\Downloads\995,000_rows (1).csv"
file_path = r"C:\Users\marti\OneDrive\Skrivebord\995000_rows.csv"

#df = pd.read_csv(file_path, low_memory=False)

#df_cleaned = df.map(lambda x: clean_text(str(x)))

#print(df_cleaned.head(10))
print("Trying to start to read chunks:")
#Ny måde, hvor vi prøver, at indlæse dokumentet lidt af gangen.
chunk_size = 10000  # Læs 10.000 rækker ad gangen

# Gem forbehandlede data
output_file = "processed_995K_FakeNewsCorpus.csv"
first_chunk = True
Times = 0

for chunk in pd.read_csv(file_path, chunksize=chunk_size, usecols=["content"], low_memory=False):
    chunk["processed_text"] = chunk["content"].astype(str).apply(clean_text)

    mode = "w" if first_chunk else "a"

    chunk.to_csv(output_file, mode=mode, header=first_chunk, index=False)

    first_chunk = False
    Times += len(chunk)
    print(f"{Times}")

print(f"Færdig")

# task 3

df995k = pd.read_csv("processed_995K_FakeNewsCorpus.csv")
print(df995k.head())

email_count = df['processed_text'].str.count("EMAIL").sum()
url_count = df['processed_text'].str.count("URL").sum()
date_count = df['processed_text'].str.count("DATE").sum()
num_count = df['processed_text'].str.count("NUM").sum()

print("EMAIL:", email_count)
print("URL:", url_count)
print("DATE:", date_count)
print("NUM:", num_count)

import ast  # til at konvertere streng -> liste
from collections import Counter

all_tokens = []

for text in df['processed_text']:
    try:
        tokens = ast.literal_eval(text)
        all_tokens.extend(tokens)
    except:
        continue

freq = Counter(all_tokens)
most_common = freq.most_common(100)

for word, count in most_common:
    print(f"{word}: {count}")

import matplotlib.pyplot as plt

most_common_10k = freq.most_common(10000)
counts = [c for _, c in most_common_10k]

plt.figure(figsize=(12,6))
plt.plot(counts)
plt.title("Frekvens af top 10.000 ord")
plt.xlabel("Ord-rang")
plt.ylabel("Frekvens")
plt.grid()
plt.show()

