# Průvodce použitím

## Rychlý start

### 1. Základní analýza grafu
```bash
python3 main.py test_complete_graph.txt
```
Vypíše:
- Typ grafu (orientovaný/neorientovaný)
- Vlastnosti (prostý, jednoduchý, souvislý, úplný, regulární, bipartitní)
- Detaily každého uzlu (stupně, sousedé, předchůdci, následníci)
- Seznam všech hran

### 2. Analýza matic
```bash
python3 matrix_analyzer.py test_complete_graph.txt
```
Vypíše:
- Matici sousednosti
- Incidenční matici
- Matici stupňů
- Laplaceovu matici
- Matici dosažitelnosti
- Matici vzdáleností
- Poloměr, průměr a centrum grafu

### 3. Pokročilé algoritmy
```bash
python3 advanced_algorithms.py test_graph.txt
```
Vypíše:
- Detekci cyklů
- Topologické řazení (pro DAG)
- Silně souvislé komponenty
- Mosty a artikulační body
- Nejkratší cesty (Dijkstra)
- Minimální kostru (Kruskal)

### 4. Komplexní analýza
```bash
python3 analyze.py test_bipartite_graph.txt --all
```
Provede kompletní analýzu grafu i matic.

## Vlastní grafy

### Vytvoření vlastního grafu

1. Vytvořte textový soubor (např. `muj_graf.txt`)
2. Definujte uzly:
```
u A;
u B;
u C;
```

3. Definujte hrany:
```
# Orientovaná hrana z A do B s váhou 5
h A > B 5 :hrana1;

# Orientovaná hrana z B do A s váhou 3
h B < A 3 :hrana2;

# Neorientovaná hrana mezi B a C
h B - C 2 :hrana3;
```

4. Analyzujte graf:
```bash
python3 main.py muj_graf.txt
```

## Příklady typů grafů

### Úplný graf K₄
```
u A; u B; u C; u D;
h A - B; h A - C; h A - D;
h B - C; h B - D;
h C - D;
```

### Bipartitní graf K₂,₃
```
u A1; u A2;
u B1; u B2; u B3;
h A1 - B1; h A1 - B2; h A1 - B3;
h A2 - B1; h A2 - B2; h A2 - B3;
```

### Orientovaný acyklický graf (DAG)
```
u Start; u A; u B; u C; u End;
h Start > A;
h Start > B;
h A > C;
h B > C;
h C > End;
```

### Graf s cyklem
```
u A; u B; u C;
h A > B;
h B > C;
h C > A;
```

### Multigraf
```
u A; u B;
h A > B :h1;
h A > B :h2;  # Násobná hrana
h A > A :loop;  # Smyčka
```

## Interpretace výstupu

### Vlastnosti grafu

- **✓ Prostý graf** - graf nemá násobné hrany
- **✓ Jednoduchý graf** - graf nemá smyčky ani násobné hrany
- **✓ Souvislý graf** - mezi každými dvěma uzly existuje cesta
- **✓ Úplný graf** - každý uzel je spojen se všemi ostatními
- **✓ Regulární graf stupně k** - všechny uzly mají stejný stupeň k
- **✓ Bipartitní graf** - uzly lze rozdělit do dvou množin bez hran uvnitř množin

### Stupně uzlů

- **Vstupní stupeň** - počet hran vstupujících do uzlu
- **Výstupní stupeň** - počet hran vystupujících z uzlu
- **Celkový stupeň** - součet vstupního a výstupního stupně

### Matice

- **Matice sousednosti** - M[i][j] = počet hran z uzlu i do uzlu j
- **Incidenční matice** - M[i][j] = vztah uzlu i a hrany j
  - 1 = hrana vychází z uzlu
  - -1 = hrana vstupuje do uzlu
  - 2 = smyčka
- **Laplaceova matice** - L = D - A (matice stupňů - matice sousednosti)

### Pokročilé vlastnosti

- **Excentricita uzlu** - největší vzdálenost od uzlu k ostatním uzlům
- **Poloměr grafu** - minimální excentricita
- **Průměr grafu** - maximální excentricita
- **Centrum grafu** - množina uzlů s minimální excentricitou
- **Most** - hrana, jejíž odebrání zvýší počet komponent
- **Artikulační bod** - uzel, jehož odebrání zvýší počet komponent

## Časté dotazy

### Jak vytvořit orientovaný graf?
Použijte `>` nebo `<` v definici hrany:
```
h A > B;  # Z A do B
h B < A;  # Z A do B (stejné jako výše)
```

### Jak vytvořit neorientovaný graf?
Použijte `-` v definici hrany:
```
h A - B;  # Neorientovaná hrana mezi A a B
```

### Jak přidat váhy?
Přidejte číslo za definici hrany:
```
h A > B 5.5;  # Hrana s váhou 5.5
u C 10;  # Uzel s váhou 10
```

### Jak přidat označení hrany?
Použijte `:` následované označením:
```
h A > B 5 :moje_hrana;
```

### Mohu mít smíšený graf?
Ano, můžete kombinovat orientované a neorientované hrany:
```
u A; u B; u C;
h A > B;  # Orientovaná
h B - C;  # Neorientovaná
```

### Jak analyzovat binární strom?
Pro binární strom používejte `*` pro vynechané uzly:
```
u A;
u B;
u C;
u D;
u *;  # Chybějící levý syn uzlu C
u E;
```

## Chybová hlášení

### "Soubor nenalezen"
- Zkontrolujte, zda soubor existuje
- Zkontrolujte název souboru

### "Uzly neexistují"
- Ujistěte se, že uzly jsou definovány před použitím v hranách
```
u A;  # Nejprve definujte uzly
u B;
h A > B;  # Pak použijte hrany
```

### "Neplatný formát"
- Každý řádek musí končit středníkem `;`
- Uzly začínají `u `
- Hrany začínají `h `

## Tipy a triky

### Komentáře
Používejte `#` pro komentáře:
```
# Toto je komentář
u A;  # Komentář za definicí
```

### Prázdné řádky
Prázdné řádky jsou ignorovány a můžete je použít pro přehlednost:
```
u A;
u B;

h A > B;
```

### Velká písmena vs. malá písmena
Identifikátory rozlišují malá a velká písmena:
```
u A;  # Uzel A
u a;  # Jiný uzel (malé a)
```

### Speciální znaky v identifikátorech
Můžete používat čísla a podtržítka:
```
u Node_1;
u Node_2;
h Node_1 > Node_2;
```

