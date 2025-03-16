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

    # Her fjerner vi stopwords fra vores csv fil.
    #tokens = [word for word in tokens if word not in stop_words]
    # Her tilføjer vi stemmer, som reducerer længden af ordene.
    #tokens = [stemmer.stem(word) for word in tokens]
    # Tokenization: Opdeling af teksten i ord
    #tokens = word_tokenize(text)

    # Fjern stopwords, hvis det er aktiveret
    if remove_stopwords:
        tokens = [word for word in tokens if word not in stop_words]

    # Stem ordene, hvis det er aktiveret
    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]

    # Returnerer tokens som en string, så de kan gemmes i CSV
    return "[" + ", ".join(f"'{token}'" for token in tokens) + "]"  

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













