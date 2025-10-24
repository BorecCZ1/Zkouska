# 🚀 ZAČNĚTE TADY!

## Rychlý návod k použití analyzátoru grafů

### ⚡ NEJRYCHLEJŠÍ START (3 kroky):

#### 1. Spusťte hlavní analyzátor:
```bash
python3 main.py
```

#### 2. Stiskněte Enter (použije výchozí testovací graf)

#### 3. Prohlédněte si výsledky! ✨

---

## 📊 CO DOSTANETE

### Analýza grafu obsahuje:

```
================================================================================
ROZHODNĚTE O NÁSLEDUJÍCÍCH VLASTNOSTECH:
================================================================================

a) OHODNOCENÝ: ✓/✗
b) ORIENTOVANÝ: ✓/✗
c) SOUVISLÝ: ✓/✗
d) PROSTÝ: ✓/✗
e) JEDNODUCHÝ: ✓/✗
f) ROVINNÝ: ? (NP-úplný)
g) KONEČNÝ: ✓
h) ÚPLNÝ: ✓/✗
i) REGULÁRNÍ: ✓/✗
j) BIPARTITNÍ: ✓/✗

================================================================================
DŮLEŽITÉ POJMY A CHARAKTERISTIKY:
================================================================================

🔹 Všechny pojmy vysvětleny s příklady
```

---

## 🎯 DALŠÍ MOŽNOSTI

### Analýza matic:
```bash
python3 matrix_analyzer.py
```
→ Dostanete 8+ typů matic + statistiky (kolik jakých čísel v matici)

### Pokročilé algoritmy:
```bash
python3 advanced_algorithms.py
```
→ Detekce cyklů, topologické řazení, nejkratší cesty, atd.

### Vše najednou:
```bash
python3 analyze.py
# Vyberte režim: grafy / matice / vše
```

---

## 📁 TESTOVACÍ GRAFY

### Máte k dispozici 27 grafů:

**Základní (7):**
- `test_graph.txt`, `test_complete_graph.txt`, atd.

**Rozšířené (20) ve složce `graphs/`:**
- Od malých (3 uzly) po velké (64 uzly)
- Různé vlastnosti: bipartitní, úplné, multigraf, atd.
- Ideální pro zkoušky - nelze poznat vlastnosti na první pohled

**Příklad použití:**
```bash
python3 main.py graphs/graph12_grid.txt
```

---

## 📚 DOKUMENTACE

### Pokud potřebujete více informací:

1. **QUICK_START.md** - Rychlý průvodce
2. **MATICE_A_VLASTNOSTI.md** - Vše o maticích (k čemu slouží)
3. **graphs/README.md** - Popis všech 20 grafů
4. **README.md** - Kompletní dokumentace

---

## 💡 TIPY

### Pro zkoušky:
```bash
# Vyberte náhodný graf
python3 main.py graphs/graph08_tree_large.txt

# Dostanete všechny vlastnosti a-j
# + vysvětlení všech pojmů
```

### Pro pochopení matic:
```bash
# Malý graf pro názornost
python3 matrix_analyzer.py test_complete_graph.txt

# Nebo přečtěte:
cat MATICE_A_VLASTNOSTI.md
```

### Vlastní graf:
```bash
# 1. Vytvořte soubor muj_graf.txt:
cat > muj_graf.txt << 'EOF'
u A;
u B;
u C;
h A > B 5;
h B > C 3;
EOF

# 2. Analyzujte:
python3 main.py muj_graf.txt
```

---

## ✅ MÁTE VŠE CO POTŘEBUJETE!

- ✅ Analyzátor vlastností grafů (a-j)
- ✅ Analyzátor matic (8+ typů)
- ✅ Pokročilé algoritmy
- ✅ 27 testovacích grafů
- ✅ Kompletní dokumentaci
- ✅ Interaktivní režim

**Stačí spustit a použít!** 🎉

---

## 🆘 POTŘEBUJETE POMOC?

1. **Základy:** Přečtěte `QUICK_START.md`
2. **Matice:** Přečtěte `MATICE_A_VLASTNOSTI.md`
3. **Grafy:** Přečtěte `graphs/README.md`
4. **Všechno:** Přečtěte `README.md`

**Nebo prostě spusťte:** `python3 main.py` a uvidíte sami! 😊

