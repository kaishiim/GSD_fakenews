# READ ME TIL KØRSEL AF KODE:
Her indsætter vi instruktions på ting til kørsel af koden:

## Part 1
I part 1 opretter vi en clean_text funktion og cleaner filen med 995.000 rows. Denne fil kan ikke gemmes under vores github repository, men kan køres og fås igennem koden ved linje "85-105 (med sin egen sti til 995.000 rows filepath)". Vi har brugt "Modern CSV" til at kigge på dataen, fordi det var for stort til almindelige programmer, som excel. Når du har fået denne fil, så skal den indsættes længere nede i linje "119" ved df995k for at kunne indlæse dataen, som bliver opereret på længere nede til at lave statestik på, hvor ofte forskellige ord forekommer.

Før man splitter, skal man bruge type og Domain (Bruges til part2 task 3). Filen fra part 1, gemmer ikke de 2 kolonner
Så python file Merge-csvfiler.py, bruges til at få type og Domain kolonnen ind i processed_995K_FakeNewsCorpus.csv

### Task 4
Task 4 bliver lavet inde i mappen Split_Data, og hedder Part1-Task4.py og splitter filen i 80% træning, 10% test og 10% validering

## Part 2

Her indlæses data'en fra part 1 task 4, fra mappen Split_Data.
Og laver de 3 modeller, der så lægges ned i mappen Part2-Model, De forskelige modeller er allerede i Part2-Model mappen.
Der burde ikke være noget man skal ændre for at få det til at virke, måske filepath.

### Task 3 
Tager Data_Scraped_During_exercise.csv fil og adder det til trænings datasættet i koden



## Part 3 - Advanced model (SVM)
Sørg for at have installet filen "processed_995K_FakeNewsCorpus.csv" (kan hentes fra part1) i sammer folder som 'fake_news_svm.py'. Dernæst vælg parameter 'nr', 'N' og 'word_min_len'. 
- 'N' står for 'Numbers of most commonwords' og styrer størelsen af puljen for de mest hyppige ord i datasættet.
- 'word_min_len' styrer minimumslængden af ord, som sorterer fejlagtige elementer tilstede i 'processed_text' kolonnen, som fx ",".
- 'nr' står for 'number of rows' og styrer hvor mange rækker indlæses fra datasættet. Juster denne parameter efter behov hvis du oplever memory problemer

Jeg anbefaler at kører med N = 1000 til 10.000 og word_min_len = 3. Derefter kør python filen fra en termnial. Hvis du oplever at koden crasher, skyldes det mest sandsynligt fordi at din maskine mangler tilstrækkelig RAM; fittingen af SVM modellen kræver nemlig 9.88 GiB (bemærk at justering på 'nr' ikke kan løse dette memory problem af en eller anden mystisk årsag)

Filen 'output.csv' er en lille version af det store datasæt på 250 rækker, brug den udelukkende til at teste om progammet virker.

## Part 4

Part 4 tager de forskellige modeller i Part2-Model mappen, og henter val datasættet i Data_split
Først prøver model 1 på Liar data-sættet, som er i liar_dataset, og er allerede kørt igennem part 1

Derefter prøver De 3 forskelige modeller til val data-sættet fra 995K_val sættet

