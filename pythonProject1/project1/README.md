# Analyzátor vlastností grafů a matic

## Popis
Kompletní sada Python skriptů pro analýzu vlastností grafů a matic podle zadání. Implementuje všechny požadované vlastnosti a pokročilé algoritmy.

## Dostupné skripty

### 🚀 INTERAKTIVNÍ REŽIM (NOVÉ!)
Všechny skripty lze nyní spustit **bez parametrů** - budou se vás ptát na vstup!

```bash
python3 main.py              # Zeptá se na soubor
python3 matrix_analyzer.py   # Zeptá se na soubor
python3 advanced_algorithms.py  # Zeptá se na soubor
python3 analyze.py           # Zeptá se na soubor i režim
```

Podrobnosti: viz [QUICK_START.md](QUICK_START.md)

---

### 1. `main.py` - Základní analýza grafů
Analyzuje základní vlastnosti grafů.

```bash
# Interaktivně (doporučeno)
python3 main.py

# Nebo s parametrem
python3 main.py <soubor_s_grafem>
```

### 2. `matrix_analyzer.py` - Analýza matic
Vytváří a analyzuje různé typy matic (sousednosti, incidenční, Laplaceova, atd.)

```bash
# Interaktivně (doporučeno)
python3 matrix_analyzer.py

# Nebo s parametrem
python3 matrix_analyzer.py <soubor_s_grafem>
```

### 3. `advanced_algorithms.py` - Pokročilé algoritmy
Implementuje pokročilé algoritmy (detekce cyklů, topologické řazení, nejkratší cesty, atd.)

```bash
# Interaktivně (doporučeno)
python3 advanced_algorithms.py

# Nebo s parametrem
python3 advanced_algorithms.py <soubor_s_grafem>
```

### 4. `analyze.py` - Kombinovaná analýza
Umožňuje komplexní analýzu grafu i matic v jednom běhu.

```bash
# Interaktivně (doporučeno) - ptá se na soubor i režim
python3 analyze.py

# Nebo s parametry
python3 analyze.py <soubor_s_grafem> [--graph|--matrix|--all]
```

Parametry:
- `--graph` - pouze analýza vlastností grafu (výchozí)
- `--matrix` - pouze analýza matic
- `--all` - komplexní analýza (grafy + matice)

## Formát vstupního souboru

### Uzly
```
u identifikátor [ohodnocení];
```

### Hrany
```
h uzel1 (< | - | >) uzel2 [ohodnocení][:označení];
```

**Směry hran:**
- `>` - orientovaná hrana z uzel1 do uzel2
- `<` - orientovaná hrana z uzel2 do uzel1  
- `-` - neorientovaná hrana

**Příklad:**
```
u A;
u B;
h A > B 1 :h1;
u C;
h B > C 1 :h2;
h A - C 2 :h3;
```

## Analyzované vlastnosti

### Základní charakteristiky
- Počet uzlů
- Počet hran
- Typ grafu (orientovaný/neorientovaný/smíšený)

### Vlastnosti grafu
- **Prostý graf** - bez násobných hran
- **Jednoduchý graf** - bez smyček a násobných hran
- **Multigraf** - obsahuje násobné hrany
- **Souvislý graf** - existuje cesta mezi každými dvěma uzly
- **Úplný graf** - každý uzel je spojen se všemi ostatními
- **Bipartitní graf** - uzly lze rozdělit do dvou množin
- **Regulární graf** - všechny uzly mají stejný stupeň
- **Diskrétní graf** - graf bez hran

### Pro každý uzel
- Vstupní stupeň (počet hran vstupujících do uzlu)
- Výstupní stupeň (počet hran vystupujících z uzlu)
- Celkový stupeň
- Sousedé (všechny sousední uzly)
- Předchůdci (uzly s hranou do tohoto uzlu)
- Následníci (uzly s hranou z tohoto uzlu)

### Další vlastnosti
- Smyčky (hrany z uzlu do sebe sama)
- Izolované uzly (uzly bez hran)
- Násobné hrany

## Matice

### Podporované typy matic
- **Matice sousednosti** - základní a vážená varianta
- **Incidenční matice** - vztah uzlů a hran
- **Matice stupňů** - diagonální matice stupňů uzlů
- **Laplaceova matice** - L = D - A (pro neorientované grafy)
- **Matice dosažitelnosti** - pomocí Warshallova algoritmu
- **Matice vzdáleností** - pomocí Floyd-Warshallova algoritmu

### Analýza matic
- Symetrie matice
- Stopa matice (součet diagonály)
- Poloměr grafu (minimální excentricita)
- Průměr grafu (maximální excentricita)
- Centrum grafu (uzly s minimální excentricitou)
- Excentricita jednotlivých uzlů

## Pokročilé algoritmy

### Detekce struktury
- **Detekce cyklů** - pro orientované i neorientované grafy
- **Topologické řazení** - pro acyklické orientované grafy (DAG)
- **Silně souvislé komponenty** - Tarjanův algoritmus
- **Mosty** - kritické hrany
- **Artikulační body** - kritické uzly

### Nejkratší cesty
- **Dijkstrův algoritmus** - pro grafy s nezápornými váhami
- **Bellman-Fordův algoritmus** - podporuje záporné váhy, detekuje záporné cykly

### Minimální kostra
- **Kruskalův algoritmus** - pro neorientované grafy

## Testovací soubory

### test_graph.txt
Orientovaný graf z příkladu zadání (8 uzlů, 14 hran)
- Obsahuje cykly
- Silně souvislý
- S váhami a označeními hran

### test_complete_graph.txt
Úplný neorientovaný graf K₄
- Regulární graf stupně 3
- Není bipartitní
- Souvislý

### test_bipartite_graph.txt
Bipartitní graf K₃,₃
- Regulární graf stupně 3
- Souvislý
- Rozdělitelný na dvě množiny {A1, A2, A3} a {B1, B2, B3}

### test_binary_tree.txt
Binární strom s hvězdičkami (vynechanými uzly)
- Demonstruje formát pro binární stromy
- Hvězdičky značí chybějící uzly

### test_regular_graph.txt
Regulární graf (cyklus C₅)
- Všechny uzly mají stupeň 2
- Obsahuje cyklus
- Souvislý

### test_multigraph.txt
Multigraf s násobnými hranami a smyčkami
- Obsahuje smyčky
- Obsahuje násobné hrany
- Smíšený graf (orientované i neorientované hrany)

### test_dag.txt
Acyklický orientovaný graf (DAG)
- Příklad závislostí úkolů
- Umožňuje topologické řazení
- Bez cyklů

## Příklady spuštění

### Základní analýza grafů
```bash
# Analýza orientovaného grafu
python3 main.py test_graph.txt

# Analýza úplného grafu
python3 main.py test_complete_graph.txt

# Analýza bipartitního grafu
python3 main.py test_bipartite_graph.txt

# Analýza multigrafu
python3 main.py test_multigraph.txt
```

### Analýza matic
```bash
# Matice úplného grafu
python3 matrix_analyzer.py test_complete_graph.txt

# Matice bipartitního grafu
python3 matrix_analyzer.py test_bipartite_graph.txt

# Matice orientovaného grafu
python3 matrix_analyzer.py test_graph.txt
```

### Pokročilé algoritmy
```bash
# Detekce cyklů a topologické řazení
python3 advanced_algorithms.py test_dag.txt

# Silně souvislé komponenty
python3 advanced_algorithms.py test_graph.txt

# Mosty a artikulační body
python3 advanced_algorithms.py test_regular_graph.txt
```

### Komplexní analýza
```bash
# Pouze grafy
python3 analyze.py test_bipartite_graph.txt --graph

# Pouze matice
python3 analyze.py test_complete_graph.txt --matrix

# Kompletní analýza
python3 analyze.py test_bipartite_graph.txt --all
```

## Implementované pojmy

- Graf, uzel, hrana
- Incidenční zobrazení
- Počáteční uzel, koncový uzel
- Sousední uzly
- Smyčka
- Ohodnocený graf
- Prostý graf
- Orientovaný/neorientovaný graf
- Symetrizace grafu
- Násobná hrana
- Jednoduchý graf, multigraf
- Souvislý graf
- Následník uzlu, předchůdce uzlu
- Soused uzlu
- Výstupní okolí uzlu, vstupní okolí uzlu
- Výstupní stupeň uzlu, vstupní stupeň uzlu
- Izolovaný uzel
- Diskrétní graf
- Úplný graf
- Bipartitní graf
- Regulární graf

## Požadavky
- Python 3.6+
- Žádné externí knihovny (používá pouze standardní knihovnu)

