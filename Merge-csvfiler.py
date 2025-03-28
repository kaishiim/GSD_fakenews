import pandas as pd


# Justere filepath til den sti fra Part 1, og den sti fra 995000 dataset
file1 = r"C:\Users\rasmu\Documents\GitHub\GSD_fakenews\output_cleaned.csv"
file2 = r"C:\Users\rasmu\Documents\995,000_rows.csv"
output_file = "processed_995K_FakeNewsCorpus.csv"

# Chunksize
chunk_size = 10000

# Merger først typer og dereffer Domain
with pd.read_csv(file1, chunksize=chunk_size) as df1_chunks, pd.read_csv(file2, chunksize=chunk_size) as df2_chunks:
    for df1_chunk, df2_chunk in zip(df1_chunks, df2_chunks):
        # Kontroller at df2 har mindst 3 kolonner
        if df2_chunk.shape[1] >= 3:
            # Udtræk kolonne 3 fra df2
            col_to_insert = df2_chunk.iloc[:, 2]

            # Indsæt som ny kolonne 4 (indeks 3) i df1
            df1_chunk.insert(3, 'Domain', col_to_insert)  
        else:
            raise ValueError("Fejl")

        # Gem i outputfilen
        df1_chunk.to_csv(output_file, mode='a', header=not bool(df1_chunk.index[0]), index=False)