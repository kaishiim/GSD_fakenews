# fil2.py

import pandas as pd
import numpy as np
import nltk
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack

# NLTK resourcer
nltk.download('punkt')
nltk.download('stopwords')

# === Mapping til binær klassificering ===
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

# === 1. Indlæs data fra Fil1's output ===
train_df = pd.read_csv("Split_Data/995K_train.csv")
val_df = pd.read_csv("Split_Data/995K_val.csv")
test_df = pd.read_csv("Split_Data/995K_test.csv")

# === 2. Tilføj binære labels ===
for df in [train_df, val_df, test_df]:
    df['label'] = df['type'].map(label_mapping)
    df.dropna(subset=['label', 'processed_text'], inplace=True)
    df['label'] = df['label'].astype(int)

# === 3. Model 1: Kun tekst ===
vectorizer = CountVectorizer(max_features=10000, stop_words='english')

X_train = vectorizer.fit_transform(train_df['processed_text'])
X_val = vectorizer.transform(val_df['processed_text'])
X_test = vectorizer.transform(test_df['processed_text'])

model_1 = LogisticRegression(max_iter=1000, class_weight="balanced")
model_1.fit(X_train, train_df['label'])

preds_1 = model_1.predict(X_test)
print("\n--- Model 1: Kun tekst ---")
print(classification_report(test_df['label'], preds_1))
print(f"F1-score: {f1_score(test_df['label'], preds_1):.4f}")
print(f"Accuracy: {accuracy_score(test_df['label'], preds_1):.4f}")

joblib.dump(model_1, "Part2-Model/model_1_text_only.pkl")
joblib.dump(vectorizer, "Part2-Model/vectorizer_1.pkl")

# === 4. Model 2: Tekst + Domain ===
if "Domain" not in train_df.columns:
    print("Fejl: 'Domain'-kolonnen mangler.")
    exit()

domain_encoder = OneHotEncoder(handle_unknown='ignore')

X_train_domain = domain_encoder.fit_transform(train_df['Domain'].fillna("unknown").astype(str).values.reshape(-1, 1))
X_val_domain = domain_encoder.transform(val_df['Domain'].fillna("unknown").astype(str).values.reshape(-1, 1))
X_test_domain = domain_encoder.transform(test_df['Domain'].fillna("unknown").astype(str).values.reshape(-1, 1))

X_train_comb = hstack([X_train, X_train_domain])
X_val_comb = hstack([X_val, X_val_domain])
X_test_comb = hstack([X_test, X_test_domain])

model_2 = LogisticRegression(max_iter=1000)
model_2.fit(X_train_comb, train_df['label'])

preds_2 = model_2.predict(X_test_comb)
print("\n--- Model 2: Tekst + Domain ---")
print(classification_report(test_df['label'], preds_2))
print(f"F1-score: {f1_score(test_df['label'], preds_2):.4f}")
print(f"Accuracy: {accuracy_score(test_df['label'], preds_2):.4f}")

joblib.dump(model_2, "Part2-Model/model_2_text_domain.pkl")
joblib.dump(domain_encoder, "Part2-Model/domain_encoder_2.pkl")
joblib.dump(vectorizer, "Part2-Model/vectorizer_2.pkl")  # samme som model 1


# === 5. Model 3: Træn med ekstra data + originalt træningsdata ===
extra_file = r"C:\Users\rasmu\Documents\GitHub\GSD_fakenews\Data_Scraped_During_Exercise2.csv"
df_extra = pd.read_csv(extra_file)

if "type" not in df_extra.columns or "processed_text" not in df_extra.columns:
    print("Fejl: Det ekstra datasæt mangler 'type' eller 'processed_text'")
    exit()

df_extra['label'] = df_extra['type'].map(label_mapping)
df_extra.dropna(subset=['label', 'processed_text'], inplace=True)
df_extra['label'] = df_extra['label'].astype(int)

# === Kombiner ekstra data med det originale træningssæt ===
combined_train_text = pd.concat([train_df['processed_text'], df_extra['processed_text']], ignore_index=True)
combined_train_labels = pd.concat([train_df['label'], df_extra['label']], ignore_index=True)

# Brug val_df og test_df fra tidligere
vectorizer_3 = CountVectorizer(max_features=10000, stop_words='english')
X_train_3 = vectorizer_3.fit_transform(combined_train_text)
X_val_3 = vectorizer_3.transform(val_df['processed_text'])
X_test_3 = vectorizer_3.transform(test_df['processed_text'])

model_3 = LogisticRegression(max_iter=1000)
model_3.fit(X_train_3, combined_train_labels)

preds_3 = model_3.predict(X_test_3)
print("\n--- Model 3: Træning med ekstra data ---")
print(classification_report(test_df['label'], preds_3))
print(f"F1-score: {f1_score(test_df['label'], preds_3):.4f}")
print(f"Accuracy: {accuracy_score(test_df['label'], preds_3):.4f}")

joblib.dump(model_3, "Part2-Model/model_3_text_extra_data.pkl")
joblib.dump(vectorizer_3, "Part2-Model/vectorizer_3.pkl")
