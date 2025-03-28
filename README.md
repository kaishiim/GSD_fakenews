# READ ME FOR KØRSEL AF KODE:
Her indsætter vi instruktions på ting til kørsel af koden:

I part 1 opretter vi en clean_text funktion og cleaner filen med 995.000 rows. Denne fil kan ikke gemmes under vores github repository, men kan køres og fås igennem koden ved linje "85-105 (med sin egen sti til 995.000 rows filepath)". Vi har brugt "Modern CSV" til at kigge på dataen, fordi det var for stort til almindelige programmer, som excel. Når du har fået denne fil, så skal den indsættes længere nede i linje "119" ved df995k for at kunne indlæse dataen, som bliver opereret på længere nede til at lave statestik på, hvor ofte forskellige ord forekommer.

Part 2?

Part 3
Sørg for at have installet filen "processed_995K_FakeNewsCorpus.csv" (kan hentes fra part1) i sammer folder som 'fake_news_svm.py'. Dernæst vælg parameter 'nr', 'N' og 'word_min_len'. 
- 'N' står for 'Numbers of most commonwords' og styrer størelsen af puljen for de mest hyppige ord i datasættet.
- 'word_min_len' styrer minimumslængden af ord, som sorterer fejlagtige elementer tilstede i 'processed_text' kolonnen, som fx ",".
- 'nr' står for 'number of rows' og styrer hvor mange rækker indlæses fra datasættet. Juster denne parameter efter behov hvis du oplever memory problemer

Jeg anbefaler at kører med N = 1000 til 10.000 og word_min_len = 3. Derefter kør python filen fra en termnial. Hvis du oplever at koden crasher, skyldes det mest sandsynligt fordi at din maskine mangler tilstrækkelig RAM; fittingen af SVM modellen kræver nemlig 9.88 GiB (bemærk at justering på 'nr' ikke kan løse dette memory problem af en eller anden mystisk årsag)

