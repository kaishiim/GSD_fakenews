
Før man splitter, skal man bruge type og Domain (Bruges til part2 task 3). Filen fra part 1, gemmer ikke de 2 kolonner
Så python file Merge-csvfiler.py, bruges til at få type og Domain kolonnen ind i processed_995K_FakeNewsCorpus.csv

Task 4

Task 4 bliver lavet inde i mappen Split_Data, og hedder Part1-Task4.py og splitter filen i 80% træning, 10% test og 10% validering

Part 2

Her indlæses data'en fra part 1 task 4, fra mappen Split_Data
Og laver de 3 modeller, der så lægges ned i mappen Part2-Model, De forskelige modeller er allerede i Part2-Model mappen



Der burde ikke være noget man skal ændre for at få det til at virke, måske filepath

Task 3 
Tager Data_Scraped_During_exercise.csv fil og adder det til trænings datasættet i koden

Part 4

Part 4 tager de forskellige modeller i Part2-Model mappen, og henter val datasættet i Data_split
Først prøver model 1 på Liar data-sættet, som er i liar_dataset, og er allerede kørt igennem part 1

Derefter prøver De 3 forskelige modeller til val data-sættet fra 995K_val sættet



