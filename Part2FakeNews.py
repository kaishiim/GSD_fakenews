import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, classification_report
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# Mapping af labels fra 'type'-kolonnen til binary classification
label_mapping = {
    "reliable": 1,
    "fake": 0,
    "conspiracy": 0,
    "political": 0,
    "unreliable": 0,
    "junksci": 0,
    "bias": 0,
    "clickbait": 0,
    "hate": 0,
}

# 1. Indlæs dataset
file_path = "output.csv"
df = pd.read_csv(file_path, header=0)  # Sørger for, at første række er kolonnenavne

# 2. Debugging: Udskriv kolonnenavne for at sikre, at 'type' findes
print("Kolonnenavne i DataFrame:", df.columns)

# Hvis 'type' ikke findes, stop programmet
if "type" not in df.columns:
    print("Fejl: Kolonnen 'type' findes ikke i filen.")
    exit()

# 3. Konverter 'type' til labels
df['label'] = df['type'].map(label_mapping)
df = df.dropna(subset=['label'])  # Fjern rækker hvor label er NaN
df['label'] = df['label'].astype(int)  # Konverter til heltal

# 4. Split dataset i træning, validering, test (80% træning, 10% validering, 10% test)
train_text, test_text, train_labels, test_labels = train_test_split(df['processed_text'], df['label'], test_size=0.2, random_state=42)
val_text, test_text, val_labels, test_labels = train_test_split(test_text, test_labels, test_size=0.5, random_state=42)

print(f"Train: {len(train_text)}, Validation: {len(val_text)}, Test: {len(test_text)}")

# 5. Forbered tekstdata (kun 10.000 mest hyppige ord)
vectorizer = CountVectorizer(max_features=10000, stop_words='english')
X_train = vectorizer.fit_transform(train_text)
X_val = vectorizer.transform(val_text)
X_test = vectorizer.transform(test_text)

# 6. Træn logistisk regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, train_labels)

predictions = model.predict(X_test)
f1 = f1_score(test_labels, predictions)
accuracy = accuracy_score(test_labels, predictions)

print("Classification Report:")
print(classification_report(test_labels, predictions))
print(f"F1-score: {f1:.4f}")
print(f"Accuracy: {accuracy:.4f}")

import joblib
joblib.dump(model, "logistic_regression_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
