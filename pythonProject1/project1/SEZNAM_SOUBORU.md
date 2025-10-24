# Seznam všech souborů projektu

## 📂 STRUKTURA PROJEKTU

```
pythonProject1/
├── main.py                     ★ HLAVNÍ SKRIPT pro analýzu grafů
├── matrix_analyzer.py          ★ Analyzátor matic
├── advanced_algorithms.py      ★ Pokročilé algoritmy
├── analyze.py                  ★ Kombinovaný analyzátor
├── demo.py                     Demo všech funkcí
│
├── README.md                   Hlavní dokumentace
├── MATICE_A_VLASTNOSTI.md      Kompletní průvodce maticemi
├── USAGE.md                    Průvodce použitím
├── QUICK_START.md              Rychlý start
├── FINAL_SUMMARY.md            Finální souhrn
├── PROJECT_SUMMARY.md          Souhrn projektu
├── CHANGELOG.md                Historie změn
├── SEZNAM_SOUBORU.md           Tento soubor
│
├── test_graph.txt              Testovací grafy (7)
├── test_complete_graph.txt
├── test_bipartite_graph.txt
├── test_dag.txt
├── test_regular_graph.txt
├── test_multigraph.txt
├── test_binary_tree.txt
│
└── graphs/                     Složka s 20 grafy
    ├── README.md               Popis všech grafů
    ├── graph01_large_directed.txt
    ├── graph02_petersen.txt
    ├── ... (celkem 20 grafů)
    └── graph20_complex_cycles.txt
```

---

## ⭐ HLAVNÍ SKRIPTY (4 + 1 demo)

### 1. `main.py` - Analyzátor vlastností grafů
**Velikost:** 19 KB | **Řádků:** ~550

**Co dělá:**
- Parsuje vstupní soubor s grafem
- Rozhoduje o vlastnostech a-j (ohodnocený, orientovaný, ...)
- Vypisuje všechny důležité pojmy
- Přehledný stručný výstup

**Použití:**
```bash
python3 main.py                          # Interaktivně
python3 main.py graphs/graph01_xxx.txt   # S parametrem
```

**Výstup:**
- Rozhodnutí a-j s odůvodněním
- Vysvětlení všech důležitých pojmů
- Statistiky grafu

---

### 2. `matrix_analyzer.py` - Analyzátor matic
**Velikost:** 27 KB | **Řádků:** ~830

**Co dělá:**
- Vytváří 8+ typů matic
- Počítá statistiky matic (kolik jakých čísel)
- Detailní charakteristiky uzlů
- Stručný výstup (jen příklady)

**Implementované matice:**
1. Matice sousednosti
2. Vážená matice sousednosti  
3. Incidenční matice
4. Matice délek/vzdáleností
5. Znaménková matice
6. Matice stupňů
7. Laplaceova matice
8. Matice dosažitelnosti
9. Tabulka incidentních hran
10. Dynamický seznam sousedů

**Použití:**
```bash
python3 matrix_analyzer.py                    # Interaktivně
python3 matrix_analyzer.py graphs/graph12.txt # S parametrem
```

---

### 3. `advanced_algorithms.py` - Pokročilé algoritmy
**Velikost:** 17 KB | **Řádků:** ~490

**Co dělá:**
- Detekce cyklů
- Topologické řazení (Kahn)
- Silně souvislé komponenty (Tarjan)
- Mosty a artikulační body
- Dijkstra, Bellman-Ford
- Kruskal (MST)

**Použití:**
```bash
python3 advanced_algorithms.py graphs/graph04_dag_complex.txt
```

---

### 4. `analyze.py` - Kombinovaný analyzátor
**Velikost:** 2.5 KB | **Řádků:** ~80

**Co dělá:**
- Kombinuje analýzu grafů a matic
- Interaktivní volba režimu
- Umožňuje analyzovat vše najednou

**Použití:**
```bash
python3 analyze.py                    # Interaktivně
python3 analyze.py graph.txt --all    # Vše
```

---

### 5. `demo.py` - Demonstrace
**Velikost:** 7.6 KB | **Řádků:** ~240

**Co dělá:**
- Interaktivní demo všech funkcí
- Ukázky různých grafů
- Krok po kroku demonstrace

---

## 📄 DOKUMENTACE (8 souborů)

### 1. README.md (7 KB)
- Hlavní dokumentace projektu
- Přehled všech funkcí
- Návod k použití

### 2. MATICE_A_VLASTNOSTI.md (10 KB) ⭐
- **KOMPLETNÍ průvodce všemi maticemi**
- K čemu slouží každá matice
- Jak ji číst a interpretovat
- Praktické příklady

### 3. QUICK_START.md (4 KB)
- Rychlý start
- Interaktivní režim
- Příklady použití

### 4. USAGE.md (5 KB)
- Detailní průvodce
- Různé scénáře použití
- FAQ

### 5. FINAL_SUMMARY.md (3 KB)
- Finální souhrn projektu
- Co bylo dokončeno
- Přehled funkcí

### 6. PROJECT_SUMMARY.md (6.5 KB)
- Technický souhrn
- Statistiky kódu
- Implementované pojmy

### 7. CHANGELOG.md (3 KB)
- Historie změn
- Verze projektu

### 8. SEZNAM_SOUBORU.md (tento soubor)
- Přehled všech souborů
- Struktura projektu

### 9. graphs/README.md (7.5 KB)
- Popis všech 20 testovacích grafů
- Vlastnosti každého grafu
- Doporučení pro použití

---

## 🧪 TESTOVACÍ GRAFY

### Původní testy (7 souborů):
- `test_graph.txt` - Ze zadání
- `test_complete_graph.txt` - K₄
- `test_bipartite_graph.txt` - K₃,₃
- `test_dag.txt` - DAG
- `test_regular_graph.txt` - Cyklus
- `test_multigraph.txt` - Multigraf
- `test_binary_tree.txt` - Strom

### Nové grafy ve složce graphs/ (20 souborů):
1. **graph01** - Velký orientovaný (25 uzlů)
2. **graph02** - Petersonův graf (10 uzlů)
3. **graph03** - Velký bipartitní (27 uzlů)
4. **graph04** - Komplexní DAG (34 uzlů)
5. **graph05** - Úplný K₁₂ (12 uzlů, 132 hran)
6. **graph06** - Těžký multigraf (8 uzlů, 60+ hran)
7. **graph07** - Nesouvislý (18 uzlů, 5 komponent)
8. **graph08** - Velký strom (31 uzlů)
9. **graph09** - Hustý neorientovaný (20 uzlů, 120+ hran)
10. **graph10** - Řídký orientovaný (30 uzlů)
11. **graph11** - Kruhová struktura (36 uzlů)
12. **graph12** - Mřížka 8×8 (64 uzlů, 112 hran)
13. **graph13** - Hvězda (26 uzlů)
14. **graph14** - Záporné váhy (20 uzlů)
15. **graph15** - Neuronová síť (28 uzlů, 140+ hran)
16. **graph16** - Turnaj (15 uzlů, 105 hran)
17. **graph17** - Smíšený graf (20 uzlů)
18. **graph18** - Silně propojený (18 uzlů, 110+ hran)
19. **graph19** - Ekonomická síť (20 uzlů, záporné váhy)
20. **graph20** - Mnoho cyklů (35 uzlů, 90+ hran)

---

## 📊 CELKOVÉ STATISTIKY

### Kód:
- **Python soubory:** 5
- **Řádků kódu:** ~1850
- **Tříd:** 4
- **Funkcí:** 60+

### Testy:
- **Testovacích grafů:** 27 (7 základních + 20 rozšířených)
- **Uzlů celkem:** ~600+
- **Hran celkem:** ~1200+

### Dokumentace:
- **Dokumentačních souborů:** 9
- **Řádků dokumentace:** ~1500+
- **KB dokumentace:** ~50 KB

### Celkem:
- **Všech souborů:** 41
- **Celková velikost:** ~120 KB

---

## 🚀 JAK POUŽÍVAT

### Rychlý test:
```bash
# Přehledná analýza grafu
python3 main.py graphs/graph02_petersen.txt

# Matice
python3 matrix_analyzer.py graphs/graph12_grid.txt

# Vše najednou
python3 analyze.py graphs/graph03_large_bipartite.txt --all
```

### Interaktivní režim:
```bash
python3 main.py
# → Zeptá se na soubor
# → Vyberte z nabídky nebo zadejte vlastní cestu
```

---

## 💡 DOPORUČENÍ PRO RŮZNÉ ÚČELY

### Pro zkoušení vlastností grafů:
→ **Použijte:** `main.py`
→ **Grafy:** Jakýkoliv z `graphs/`
→ **Dostanete:** Rozhodnutí a-j + pojmy

### Pro analýzu matic:
→ **Použijte:** `matrix_analyzer.py`  
→ **Grafy:** graph12 (mřížka), graph03 (bipartitní)
→ **Dostanete:** Všechny matice + statistiky

### Pro algoritmy:
→ **Použijte:** `advanced_algorithms.py`
→ **Grafy:** graph04 (DAG), graph20 (cykly)
→ **Dostanete:** Detekce cyklů, SCC, cesty

---

## 📚 NEJDŮLEŽITĚJŠÍ SOUBORY

**Pro rychlý start:**
1. `QUICK_START.md` - Jak začít
2. `main.py` - Hlavní skript

**Pro pochopení:**
1. `MATICE_A_VLASTNOSTI.md` - K čemu slouží matice
2. `graphs/README.md` - Popis všech grafů

**Pro testování:**
1. `graphs/graph01-20` - 20 různých grafů
2. `main.py` - Analýza vlastností

---

## ✅ SOUHRN

Máte k dispozici:
- ✅ **4 hlavní skripty** pro různé analýzy
- ✅ **27 testovacích grafů** s různými vlastnostmi
- ✅ **9 dokumentačních souborů** s kompletními informacemi
- ✅ **Interaktivní režim** pro snadné použití
- ✅ **Přehledný výstup** (stručný, strukturovaný)

**Všechno funguje a je připraveno k použití!** 🎉

