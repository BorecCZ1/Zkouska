# Rychlý start - Interaktivní použití

## 🚀 Spuštění bez parametrů

Všechny skripty nyní podporují **interaktivní režim**. Stačí je spustit bez parametrů a budou se vás ptát na vstup.

### 1. Základní analýza grafů

```bash
python3 main.py
```

**Co se stane:**
1. Zobrazí se seznam dostupných testovacích souborů
2. Zadejte cestu k souboru nebo stiskněte Enter pro výchozí
3. Program automaticky načte a analyzuje graf

**Příklad:**
```
╔════════════════════════════════════════════════════════════════════╗
║          ANALYZÁTOR VLASTNOSTÍ GRAFŮ A MATIC                       ║
╚════════════════════════════════════════════════════════════════════╝

Dostupné testovací soubory:
  1. test_graph.txt - Orientovaný graf ze zadání
  2. test_complete_graph.txt - Úplný graf K₄
  3. test_bipartite_graph.txt - Bipartitní graf K₃,₃
  4. test_regular_graph.txt - Regulární graf (cyklus)
  5. test_multigraph.txt - Multigraf se smyčkami
  6. test_dag.txt - Acyklický orientovaný graf
  7. test_binary_tree.txt - Binární strom

📂 Zadejte cestu k souboru s grafem (nebo stiskněte Enter pro test_graph.txt): 
```

**Můžete:**
- Stisknout **Enter** → použije se výchozí soubor
- Zadat **číslo** (např. `2`) → použije se test_complete_graph.txt
- Zadat **vlastní cestu** (např. `muj_graf.txt`)

---

### 2. Analýza matic

```bash
python3 matrix_analyzer.py
```

**Stejný princip** - ptá se na soubor, výchozí je `test_complete_graph.txt`

---

### 3. Pokročilé algoritmy

```bash
python3 advanced_algorithms.py
```

**Výchozí soubor:** `test_dag.txt` (doporučený pro ukázku topologického řazení)

---

### 4. Komplexní analýza

```bash
python3 analyze.py
```

**Ptá se na:**
1. **Soubor s grafem** (výchozí: `test_graph.txt`)
2. **Režim analýzy:**
   - `1` nebo Enter → pouze grafy
   - `2` → pouze matice
   - `3` → kompletní analýza (grafy + matice)

**Příklad interakce:**
```
📂 Zadejte cestu k souboru s grafem (nebo stiskněte Enter pro test_graph.txt): test_bipartite_graph.txt
   → Použiji výchozí soubor: test_bipartite_graph.txt

Režim analýzy:
  1. --graph  - pouze analýza vlastností grafu
  2. --matrix - pouze analýza matic
  3. --all    - komplexní analýza (grafy + matice)

Vyberte režim (1/2/3 nebo stiskněte Enter pro --graph): 3
   → Režim: --all
```

---

## 📝 Alternativní použití (s parametry)

Pokud chcete, můžete stále používat parametry příkazové řádky:

```bash
# Základní analýza
python3 main.py test_complete_graph.txt

# Analýza matic
python3 matrix_analyzer.py test_bipartite_graph.txt

# Pokročilé algoritmy
python3 advanced_algorithms.py test_dag.txt

# Komplexní analýza
python3 analyze.py test_graph.txt --all
```

---

## 💡 Tipy

### Rychlý test (stále Enter)
```bash
python3 main.py
# Stiskněte Enter → použije test_graph.txt
```

### Vlastní soubor
```bash
python3 main.py
# Zadejte: muj_vlastni_graf.txt
```

### Číslo místo názvu
Můžete zadat jen číslo z nabídky:
```bash
python3 matrix_analyzer.py
# Zadejte: 3 → použije test_bipartite_graph.txt
```

---

## 🎯 Doporučené scénáře

### Pro začátečníky
```bash
python3 analyze.py
# Enter, Enter → rychlá analýza test_graph.txt
```

### Pro testování
```bash
python3 analyze.py
# test_complete_graph.txt
# 3 (kompletní analýza)
```

### Pro vlastní grafy
```bash
python3 main.py
# muj_graf.txt
```

---

## ✅ Shrnutí

**Interaktivní režim:**
- ✅ Bez nutnosti pamatovat si parametry
- ✅ Přehledný výběr souborů
- ✅ Výchozí hodnoty pro rychlé testování
- ✅ Možnost zadat vlastní cestu

**Parametrický režim:**
- ✅ Stále funguje
- ✅ Rychlejší pro opakované použití
- ✅ Vhodný pro skripty

---

Vyberte si, co vám vyhovuje! 🚀

