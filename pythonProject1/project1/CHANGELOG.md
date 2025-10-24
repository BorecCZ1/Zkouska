# Changelog - Historie změn

## Verze 2.0 - Interaktivní režim (22.10.2025)

### ✨ Nové funkce

#### 🎯 Hlavní změna: Interaktivní vstup
Všechny hlavní skripty nyní podporují **interaktivní režim**:

- **main.py** - ptá se na soubor s grafem
- **matrix_analyzer.py** - ptá se na soubor s grafem
- **advanced_algorithms.py** - ptá se na soubor s grafem
- **analyze.py** - ptá se na soubor i režim analýzy

#### 📋 Výhody interaktivního režimu:
- ✅ Není nutné pamatovat si parametry
- ✅ Přehledný výběr z testovacích souborů
- ✅ Výchozí hodnoty pro rychlé testování
- ✅ Možnost zadat vlastní cestu k souboru
- ✅ Stále funguje i parametrický režim

### 📚 Nová dokumentace

- **QUICK_START.md** - Rychlý průvodce pro interaktivní použití
- **CHANGELOG.md** - Historie změn (tento soubor)
- **demo_interactive.sh** - Demo skript pro ukázku

### 🔄 Aktualizace

- Aktualizován **README.md** s informacemi o interaktivním režimu
- Všechny hlavní skripty zachovávají zpětnou kompatibilitu

---

## Verze 1.0 - Původní release (22.10.2025)

### ✨ Implementované funkce

#### Hlavní skripty
- **main.py** - Základní analýza grafů
- **matrix_analyzer.py** - Analýza matic
- **advanced_algorithms.py** - Pokročilé algoritmy
- **analyze.py** - Kombinovaná analýza
- **demo.py** - Interaktivní demonstrace

#### Analyzované vlastnosti (15+)
- Orientovaný/neorientovaný/smíšený graf
- Prostý/jednoduchý/multigraf
- Souvislý/úplný/bipartitní/regulární/diskrétní graf
- Smyčky, násobné hrany, izolované uzly
- Stupně uzlů (vstupní, výstupní, celkový)
- Sousedé, předchůdci, následníci

#### Matice (7 typů)
- Matice sousednosti (základní + vážená)
- Incidenční matice
- Matice stupňů
- Laplaceova matice
- Matice dosažitelnosti (Warshall)
- Matice vzdáleností (Floyd-Warshall)

#### Pokročilé algoritmy (10+)
- Detekce cyklů (orientované i neorientované)
- Topologické řazení (Kahn)
- Silně souvislé komponenty (Tarjan)
- Mosty a artikulační body
- Dijkstrův algoritmus
- Bellman-Fordův algoritmus
- Kruskalův algoritmus (MST)
- Floyd-Warshall
- Warshall

#### Testovací soubory (7)
- test_graph.txt
- test_complete_graph.txt
- test_bipartite_graph.txt
- test_dag.txt
- test_regular_graph.txt
- test_multigraph.txt
- test_binary_tree.txt

#### Dokumentace
- README.md - Kompletní dokumentace
- USAGE.md - Průvodce použitím
- PROJECT_SUMMARY.md - Souhrn projektu

---

## Plány do budoucna

### Možná rozšíření (v 3.0)
- [ ] Vizualizace grafů pomocí matplotlib
- [ ] Export do formátů GraphML, DOT
- [ ] Webové rozhraní
- [ ] Detekce rovinnosti grafu
- [ ] Hamiltonovské cesty/cykly
- [ ] Více testovacích grafů
- [ ] Unit testy

---

## Poznámky k verzím

**Verze 2.0** přidává uživatelsky přívětivý interaktivní režim, který usnadňuje práci se skripty.

**Verze 1.0** obsahuje kompletní implementaci všech požadavků ze zadání včetně pokročilých algoritmů a rozsáhlé dokumentace.

