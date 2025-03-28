import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack

# Label mapping til processed_text og til Liar data-sættet
label_mapping = {
    "true": 1,
    "mostly-true": 0,
    "half-true": 0,
    "barely-true": 0,
    "false": 0,
    "pants-fire": 0,
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

# Test kun model 1 på LIAR 
print("\n=== Test: Model 1 på LIAR ===")
df_test_liar = pd.read_csv("liar_dataset/Clean_test.tsv", sep="\t")
df_test_liar = df_test_liar[["cleaned_text", "label"]].dropna()
df_test_liar["label"] = df_test_liar["label"].map(label_mapping)
df_test_liar.dropna(subset=["label"], inplace=True)
df_test_liar["label"] = df_test_liar["label"].astype(int)

test_text_liar = df_test_liar["cleaned_text"]
test_labels_liar = df_test_liar["label"]

#Loader model 1 fra mappen Part2-Model
model_1 = joblib.load("part2-Model/model_1_text_only.pkl")
vectorizer_1 = joblib.load("part2-Model/vectorizer_1.pkl")
X_test_liar = vectorizer_1.transform(test_text_liar)

pred_liar = model_1.predict(X_test_liar)
f1_liar = f1_score(test_labels_liar, pred_liar)
acc_liar = accuracy_score(test_labels_liar, pred_liar)
cm_liar = confusion_matrix(test_labels_liar, pred_liar)

print(f"F1-score: {f1_liar:.4f}")
print(f"Accuracy: {acc_liar:.4f}")
plt.figure(figsize=(4, 3))
sns.heatmap(cm_liar, annot=True, fmt="d", cmap="Blues")
plt.title("Model 1 - LIAR")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# Test alle modeller på 995K_val.csv 
print("\n=== Test: Alle modeller på 995K_val.csv ===")
df_val = pd.read_csv("Split_Data/995K_val.csv")
df_val = df_val[["processed_text", "type", "Domain"]].dropna()
df_val["label"] = df_val["type"].map(label_mapping)
df_val.dropna(subset=["label"], inplace=True)
df_val["label"] = df_val["label"].astype(int)

val_text = df_val["processed_text"]
val_labels = df_val["label"]

#Funktion til at teste på de 3 modeller
def evaluate_model_on_995k(name, model_path, vectorizer_path, domain_encoder_path=None, domain_series=None):
    print(f"\nEvaluating {name} on 995K_val.csv")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    X_text = vectorizer.transform(val_text)

    if domain_encoder_path and domain_series is not None:
        encoder = joblib.load(domain_encoder_path)
        domain_data = domain_series.fillna("unknown").astype(str).values.reshape(-1, 1)
        X_domain = encoder.transform(domain_data)
        X = hstack([X_text, X_domain])
    else:
        X = X_text

    preds = model.predict(X)
    f1 = f1_score(val_labels, preds)
    acc = accuracy_score(val_labels, preds)
    cm = confusion_matrix(val_labels, preds)

    print(f"F1-score: {f1:.4f}")
    print(f"Accuracy: {acc:.4f}")
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
    plt.title(f"{name} - 995K_val.csv")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

#Køre på alle modeller 
evaluate_model_on_995k(
    name="Model 1: Text only",
    model_path="part2-Model/model_1_text_only.pkl",
    vectorizer_path="part2-Model/vectorizer_1.pkl"
)

evaluate_model_on_995k(
    name="Model 2: Text + Domain",
    model_path="part2-Model/model_2_text_domain.pkl",
    vectorizer_path="part2-Model/vectorizer_2.pkl",
    domain_encoder_path="part2-Model/domain_encoder_2.pkl",
    domain_series=df_val["Domain"]
)

evaluate_model_on_995k(
    name="Model 3: Text + Extra data",
    model_path="part2-Model/model_3_text_extra_data.pkl",
    vectorizer_path="part2-Model/vectorizer_3.pkl"
)
