# Analiza dejavnikov, povezanih s tržno vrednostjo 500 najvrednejših nogometnih igralcev

## Opis projekta

V projektni nalogi analiziram 500 najvrednejših nogometnih igralcev in raziskujem, kateri dejavniki so povezani z njihovo tržno vrednostjo.

Pri analizi obravnavam predvsem povezavo tržne vrednosti z:
- starostjo igralca,
- igralnim časom,
- močjo tekmovanj, v katerih igralec nastopa,
- napadalno uspešnostjo,
- klubom,
- državljanstvom.

## Struktura projekta

Projekt vsebuje naslednje glavne datoteke:

- `transfermarket.py`  
  Pridobi podatke o 500 najvrednejših igralcih in jih shrani v `podatki/transfermarket/najvrednejsi_igralci.csv`.

- `fbref.py`  
  Pridobi statistične podatke igralcev iz različnih domačih in mednarodnih tekmovanj. Za posameznega igralca združi podatke iz vseh tekmovanj, v katerih je nastopal, in jih shrani v `podatki/fbref/fbref_igralci.csv`.

- `opta_analyst.py`  
  Pridobi podatke o moči lig ter izračuna moč posameznih tekmovanj. Rezultate shrani v `podatki/opta/moc_tekmovanj.csv`.

- `orodja.py`  
  Vsebuje pomožne funkcije za prenos spletnih strani, uporabo SeleniumBase, branje in shranjevanje datotek ter zapisovanje podatkov v CSV.

- `analiza.ipynb`  
  Jupyter Notebook, v katerem združim in očistim pridobljene podatke ter izvedem končno analizo. Rezultati so predstavljeni s tabelami, opisnimi statistikami in grafi.

## Navodila za uporabo in zagon

Za zagon projekta je treba narediti naslednje:

1. Prenesemo oziroma kloniramo repozitorij na računalnik in v terminalu odpremo njegovo korensko mapo.

2. Namestimo potrebne Python knjižnice:
- pandas
- matplotlib
- requests
- seleniumbase
- jupyter
   

3. Če želimo podatke pridobiti s spletnih strani, najprej zaženemo skripto za pridobivanje podatkov o igralcih:
   python transfermarkt.py

4. Nato zaženemo skripto za pridobivanje statistike igralcev:
   python fbref.py

5. Nato zaženemo skripto za pridobivanje in izračun moči tekmovanj:
   python opta_analyst.py

6. Skripte ustvarijo CSV-datoteke, ki jih uporablja končna analiza. Če so te datoteke v mapi `podatki` že prisotne, korakov 3, 4 in 5 ni treba ponovno izvesti.

7. Zaženemo Jupyter Notebook:

8. V Jupyterju odpremo datoteko `analiza.ipynb`.

9. Celice v notebooku izvedemo po vrsti od začetka do konca oziroma uporabimo možnost **Run All**.

Datoteke `orodja.py` ne zaganjamo posebej, saj vsebuje pomožne funkcije, ki jih uporabljajo ostale skripte.
"Copilot: Pomagal pri sestavljanju besedila navodilo za uporabo in zagon"