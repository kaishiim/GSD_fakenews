# Part 1
import re

def clean_text(text):
    #Replaces text to be lowercase.
    text = text.lower()
    #Removing spaces/lines.
    text = re.sub(r'\s+', ' ', text)
    #Replacing numbers with NUM.
    text = re.sub(r'\d+', '<NUM>', text)
    #Replacing dates with DATE.
    text = re.sub(r'\d{4}-\d{2}-\d{2}', '<DATE>', text)
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '<DATE>', text)
    #Replacing emails with EMAIL.
    text = re.sub(r'\S+@\S+\.\S+', '<EMAIL>', text)
    #Replacing urls with URL.
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)
    return text

import pandas as pd

url = "https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv"

dataframe = pd.read_csv(url)

dataframe["content_clean"] = dataframe["content"].dropna().apply(clean_text)

print(dataframe[["content", "content_clean"]].head(10))

dataframe.to_csv("cleaned_dataset.csv", index=False)

#Part 2
#Part 3
#Part 4