import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from collections import Counter

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
#file_path = "output.csv"    #small test set
file_path = "processed_995K_FakeNewsCorpus.csv"
df = pd.read_csv(file_path, header=0) 



# Parameters
N = 2000  # number of most common words
word_min_len = 3 # minimum length of words


"""
# Create target vector of labels
art_type = df['type'].values.tolist()
y = []
for ts in art_type:
    if type(ts) is type(''):
        ts2 = ts.strip()[2:-2]
        if ts2 in label_mapping:
            t3 = label_mapping[ts2]
        else:
            t3 = 0
        y.append(t3)
del art_type

# Get words
artcontent = df['content'].values.tolist()
print(len(artcontent))
#print(wordcontent)
wordlist = []
for art in artcontent:
    #if type(art) is not type(''): print(type(art), art)
    if type(art) is type(''):
        wl = art.split(",")
        for wrd in wl:
            wrd2 = wrd.strip()[1:-1]
            if len(wrd2) >= word_min_len:
                wordlist.append(wrd2)
"""

# Get targets and words
art_type = df['type'].values.tolist()
artcontent = df['content'].values.tolist()
nr = len(art_type) // 10 # antal rækker indlæsning
print("nr", nr)
wordlist, y = [], []
for i in range(nr):
    ts = art_type[i]
    art = artcontent[i]
    #if type(ts) is not type(''): print(type(ts), ts)
    if type(ts) is type(''):
        ts2 = ts.strip()[2:-2]
        if ts2 in label_mapping:
            t3 = label_mapping[ts2]
        else:
            t3 = 0
        #if type(art) is not type(''): print(type(art), art)
        if type(art) is type(''):
            wl = art.split(",")
            for wrd in wl:
                wrd2 = wrd.strip()[1:-1]
                if len(wrd2) >= word_min_len:
                    wordlist.append(wrd2)
            # append to y
            y.append(t3)
print("y has size", len(y))

# Collect N most common words from dataframe column 'content'
word_cnt = Counter(wordlist)
common_words = word_cnt.most_common(N)
print(common_words)
print(len(word_cnt))
del wordlist
del word_cnt
del df



# Create mapping from word to vector index
w2i = dict()  # word to index
for i, kc in enumerate(common_words):
    k, c = kc
    print(i, k, c)
    w2i[k] = i
print(w2i)
del common_words

# Create a vector for each article
"""articlevectors = []
for art in artcontent:
    articlevector = [0]*N
    #if type(art) is not type(''): print(type(art), art)
    if type(art) is type(''):
        wl = art.split(",")
        for wrd in wl:
            wrd2 = wrd.strip()[1:-1]
            if wrd2 in w2i: # brug ord fra ww2 som index i w2i
                i = w2i[wrd2]
                articlevector[i] = 1
        articlevectors.append(articlevector)
X = articlevectors
del articlevector
del articlevectors
del w2i"""
articlevectors = []
for i in range(nr):
    ts = art_type[i]
    art = artcontent[i]
    articlevector = [0]*N
    #if type(ts) is not type(''): print(type(ts), ts)
    if type(ts) is type(''):
        #if type(art) is not type(''): print(type(art), art)
        if type(art) is type(''):
            wl = art.split(",")
            for wrd in wl:
                wrd2 = wrd.strip()[1:-1]
                if wrd2 in w2i:  # brug ord fra ww2 som index i w2i
                    i = w2i[wrd2]
                    articlevector[i] = 1
            articlevectors.append(articlevector)
X = articlevectors
del(art_type)
del articlevector
del articlevectors
del w2i

print("X and y")
#print("X SÆT:", X)
#print("Y SÆT:", y)

# Split into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0) # 70% training and 30% test
del X
del y

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)  ## numpy._core._exceptions._ArrayMemoryError: Unable to allocate 9.88 GiB for an array with shape (663049, 2000) and data type float64

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))

"""
#MODEL STATS
Accuracy: 0.92
Precision: 0.9433962264150944
Recall: 0.9433962264150944
"""
