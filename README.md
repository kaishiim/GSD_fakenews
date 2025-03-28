# READ ME OMKRING KØRSEL AF KODE:
Her indsætter vi instruktions på ting til kørsel af koden:

I part 1 opretter vi en clean_text funktion og cleaner filen med 995.000 rows. Denne fil kan ikke gemmes under vores github repository, men kan køres og fås igennem koden ved linje "...". Vi har brugt "Modern CSV" til at kigge på dataen, fordi det var for stort til almindelige programmer, som excel. Når du har fået denne fil, så skal den indsættes længere nede i linje 102 ved df995k for at kunne indlæse dataen, som bliver opereret på.

Part 2?

Part 3?


# Læs CSV-fil
#file_path = r"C:\Users\yifan\Downloads\995,000_rows (1).csv"
file_path = r"C:\Users\marti\OneDrive\Skrivebord\995000_rows.csv"

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

