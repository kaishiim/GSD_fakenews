import pandas as pd
from sklearn.model_selection import train_test_split


#Indlæs data fra part 1/ task4
file_path = "../processed_995K_FakeNewsCorpus.csv"
df = pd.read_csv(file_path, header=0)


# Split data 
train_df, test_df = train_test_split(df, test_size=0.2, random_state=0)
val_df, test_df = train_test_split(test_df, test_size=0.5, random_state=0)

cols_to_save = ['processed_text', 'type', 'Domain']

# Gemerm til filer 
train_df.to_csv("995K_train.csv", index=False)
val_df.to_csv("995K_val.csv", index=False)
test_df.to_csv("995K_test.csv", index=False)

print(f"Data gemt!\nTrain: {len(train_df)}, Validation: {len(val_df)}, Test: {len(test_df)}")
