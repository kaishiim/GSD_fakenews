import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Sørg for at disse ressourcer er hentet
nltk.download('punkt')
nltk.download('stopwords')

# Initialiser stemmer og stopord
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text, remove_stopwords=True, apply_stemming=True):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL', text)
    text = re.sub(r'\b(?:https?://|www\.)\S+\b', 'URL', text)
    text = re.sub(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b', 'DATE', text)
    text = re.sub(r'\b\d+\b', 'NUM', text)
    text = re.sub(r'\s+', ' ', text).strip()

    tokens = word_tokenize(text)
    
    if remove_stopwords:
        tokens = [word for word in tokens if word not in stop_words]

    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]

    return "[" + ", ".join(f"'{token}'" for token in tokens) + "]"

# Indlæs TSV-fil
df = pd.read_csv("valid.tsv", sep='\t')

# Antag at kolonnen med tekst hedder 'text'
df['cleaned_text'] = df['statement'].apply(clean_text)

# Gem den rensede data til en ny fil
df.to_csv("Clean_valid.tsv", sep='\t', index=False)
