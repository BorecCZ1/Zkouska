# Kompletní průvodce maticemi a vlastnostmi grafů

## 📊 MATICE

### 1. Matice sousednosti (Adjacency Matrix)

**K čemu slouží:**
- Základní reprezentace grafu v paměti počítače
- Rychlé zjištění, zda mezi dvěma uzly existuje hrana (O(1))
- Výpočet počtu cest délky k mezi uzly (umocněním matice A^k)

**Jak vypadá:**
```
     A   B   C   D
A    0   1   1   0
B    1   0   1   1
C    1   1   0   1
D    0   1   1   0
```

**Interpretace:**
- `M[i][j] = 1` znamená, že z uzlu i vede hrana do uzlu j
- `M[i][j] = 0` znamená, že mezi i a j není přímá hrana
- Diagonála: M[i][i] = počet smyček na uzlu i

**Vlastnosti:**
- Pro neorientovaný graf: symetrická (M[i][j] = M[j][i])
- Pro orientovaný graf: obecně nesymetrická
- Stopa matice = počet smyček v grafu

---

### 2. Vážená matice sousednosti (Weighted Adjacency Matrix)

**K čemu slouží:**
- Reprezentace ohodnocených grafů
- Algoritmy nejkratší cesty (Dijkstra, Floyd-Warshall)
- Minimální kostra (Prim, Kruskal)
- Optimalizační úlohy

**Jak vypadá:**
```
     A     B     C     D
A   0.0   5.2   3.1   ∞
B   5.2   0.0   2.4   7.8
C   3.1   2.4   0.0   4.5
D   ∞     7.8   4.5   0.0
```

**Interpretace:**
- `M[i][j] = w` znamená, že hrana z i do j má váhu w
- `M[i][j] = 0` nebo `∞` znamená, že hrana neexistuje
- Váhy mohou být vzdálenosti, ceny, časy, atd.

---

### 3. Incidenční matice (Incidence Matrix)

**K čemu slouží:**
- Reprezentace vztahu mezi uzly a hranami
- Kirchhoffovy zákony v elektrických obvodech
- Toky v sítích
- Některé speciální algoritmy

**Jak vypadá (orientovaný graf):**
```
      e1  e2  e3  e4
A      1  -1   0   0
B     -1   0   1   0
C      0   1  -1   1
D      0   0   0  -1
```

**Interpretace:**
- Řádky = uzly, sloupce = hrany
- `M[i][j] = 1` → z uzlu i vychází hrana j
- `M[i][j] = -1` → do uzlu i vstupuje hrana j
- `M[i][j] = 0` → uzel i a hrana j nemají vztah
- `M[i][j] = 2` → smyčka (hrana z uzlu i do sebe sama)

**Pro neorientovaný graf:**
- `M[i][j] = 1` → uzel i inciduje s hranou j

**Vlastnosti:**
- Každý sloupec má právě 2 nenulové prvky (kromě smyček)
- Součet sloupce = 0 pro orientované grafy

---

### 4. Matice délek/vzdáleností (Distance Matrix)

**K čemu slouží:**
- Nalezení nejkratší cesty mezi VŠEMI páry uzlů
- Výpočet průměru grafu (největší vzdálenost)
- Výpočet poloměru grafu (nejmenší excentricita)
- Nalezení centra grafu

**Algoritmus:** Floyd-Warshall (O(n³))

**Jak vypadá:**
```
     A    B    C    D
A   0.0  1.0  2.0  3.0
B   1.0  0.0  1.0  2.0
C   2.0  1.0  0.0  1.0
D   3.0  2.0  1.0  0.0
```

**Interpretace:**
- `M[i][j]` = délka nejkratší cesty z i do j
- `M[i][i] = 0` (vzdálenost k sobě)
- `M[i][j] = ∞` pokud neexistuje cesta

---

### 5. Znaménková matice (Signed Matrix)

**K čemu slouží:**
- Analýza směru hran
- Detekce bilančních uzlů (kde součet řádku = 0)
- Analýza toků
- Studium orientace grafu

**Jak vypadá:**
```
     A    B    C    D
A    0   +1   -1    0
B   -1    0   +1   +1
C   +1   -1    0   -1
D    0   -1   +1    0
```

**Interpretace:**
- `M[i][j] = +1` → existuje hrana z i do j
- `M[i][j] = -1` → existuje hrana z j do i
- `M[i][j] = 0` → neexistuje přímá hrana
- Antisymetrická: M[i][j] = -M[j][i]

---

### 6. Matice stupňů (Degree Matrix)

**K čemu slouží:**
- Výpočet Laplaceovy matice
- Spektrální analýza grafu
- Normalizace grafu

**Jak vypadá:**
```
     A   B   C   D
A    3   0   0   0
B    0   4   0   0
C    0   0   2   0
D    0   0   0   5
```

**Interpretace:**
- Diagonální matice
- `M[i][i]` = stupeň uzlu i (počet incidentních hran)
- Všechny mimo-diagonální prvky = 0

---

### 7. Laplaceova matice (Laplacian Matrix)

**K čemu slouží:**
- Spektrální analýza grafu
- Detekce komunit v grafu
- Výpočet počtu koster (Kirchhoffova věta)
- Náhodné procházky grafem
- Embedding grafů

**Vzorec:** L = D - A (Matice stupňů - Matice sousednosti)

**Jak vypadá:**
```
     A    B    C    D
A    3   -1   -1   -1
B   -1    4   -1   -1
C   -1   -1    2   -1
D   -1   -1   -1    5
```

**Vlastnosti:**
- Symetrická (pro neorientované grafy)
- Součet každého řádku = 0
- Nejmenší vlastní číslo = 0
- Druhé nejmenší vlastní číslo = algebraická souvislost

---

### 8. Matice dosažitelnosti (Reachability Matrix)

**K čemu slouží:**
- Zjištění, které uzly jsou dosažitelné z kterých
- Testování souvislosti grafu
- Tranzitivní uzávěr relace
- Analýza závislostí

**Algoritmus:** Warshallův algoritmus (O(n³))

**Jak vypadá:**
```
     A   B   C   D
A    1   1   1   1
B    0   1   1   1
C    0   0   1   1
D    0   0   0   1
```

**Interpretace:**
- `M[i][j] = 1` → existuje cesta z i do j
- `M[i][j] = 0` → neexistuje cesta z i do j
- `M[i][i] = 1` (každý uzel je dosažitelný sám ze sebe)

---

## 📋 TABULKA INCIDENTNÍCH HRAN (Edge List)

**K čemu slouží:**
- Kompaktní reprezentace řídkých grafů
- Export/import grafů do různých formátů
- Lidsky čitelná reprezentace

**Formát:**
```
ID  Z uzlu    Typ   Do uzlu   Váha   Označení
1   A         →     B         5.0    hrana1
2   B         →     C         3.0    hrana2
3   A         —     C         2.0    hrana3
```

**Výhody:**
- Úsporná paměť pro řídké grafy (O(E) místo O(V²))
- Snadné přidávání/mazání hran
- Přehledná pro člověka

---

## 📝 DYNAMICKÉ SEZNAMY

### Dynamický seznam sousedů (Adjacency List)

**K čemu slouží:**
- Paměťově efektivní reprezentace řídkých grafů
- Rychlý průchod grafu (DFS, BFS)
- Většina moderních algoritmů grafů

**Formát:**
```
A: [B, C, D]
B: [A, C]
C: [A, B, D]
D: [A, C]
```

**Výhody:**
- O(1) přístup k sousedům uzlu
- Paměť: O(V + E) místo O(V²)
- Rychlá iterace přes sousedy

---

## 🎯 CHARAKTERISTIKY UZLŮ

### 1. Stupně uzlu

**Vstupní stupeň (in-degree):**
- Počet hran vstupujících DO uzlu
- Počet předchůdců
- V orientovaném grafu: kolik uzlů "ukazuje" na tento uzel

**Výstupní stupeň (out-degree):**
- Počet hran vystupujících Z uzlu
- Počet následníků
- V orientovaném grafu: kolik uzlů je dosažitelných přímo z tohoto uzlu

**Celkový stupeň (total degree):**
- Součet vstupního a výstupního stupně
- Pro neorientovaný graf: počet sousedů

**Příklad:**
```
    A → B → C
    ↓       ↑
    D ------+

Uzel B: in-degree = 1 (z A)
        out-degree = 1 (do C)
        total degree = 2
```

---

### 2. Relace uzlů

**Předchůdci (Predecessors):**
- Uzly, ze kterých vede hrana DO tohoto uzlu
- "Kdo mě může přímo ovlivnit"

**Následníci (Successors):**
- Uzly, do kterých vede hrana Z tohoto uzlu
- "Koho mohu přímo ovlivnit"

**Sousedé (Neighbors):**
- Všechny uzly spojené hranou (bez ohledu na směr)
- Pro neorientovaný graf: následníci = předchůdci = sousedé

---

### 3. Excentricita (Eccentricity)

**Co to je:**
- Největší vzdálenost od daného uzlu k ostatním uzlům
- "Jak daleko je nejzazší uzel"

**K čemu slouží:**
- Výpočet poloměru a průměru grafu
- Nalezení centra grafu

**Výpočet:**
- excentricita(v) = max{d(v,u) : u ∈ V}

**Příklad:**
```
A---B---C---D

excentricita(A) = 3 (vzdálenost k D)
excentricita(B) = 2 (vzdálenost k D)
excentricita(C) = 2 (vzdálenost k A)
```

---

### 4. Speciální vlastnosti uzlů

**Izolovaný uzel:**
- Uzel bez jakýchkoliv hran
- stupeň = 0

**Uzel se smyčkou:**
- Má hranu do sebe sama
- V matici sousednosti: M[i][i] > 0

**Zdroj (Source):**
- Pouze výstupní hrany, žádné vstupní
- in-degree = 0, out-degree > 0
- "Začátek toku"

**Stok (Sink):**
- Pouze vstupní hrany, žádné výstupní
- in-degree > 0, out-degree = 0
- "Konec toku"

---

## 📈 GLOBÁLNÍ VLASTNOSTI GRAFU

### Poloměr grafu (Radius)
- Minimální excentricita
- radius(G) = min{ecc(v) : v ∈ V}

### Průměr grafu (Diameter)
- Maximální excentricita
- diameter(G) = max{ecc(v) : v ∈ V}

### Centrum grafu (Center)
- Množina uzlů s minimální excentricitou
- Uzly "uprostřed" grafu

---

## 💡 PRAKTICKÉ POUŽITÍ

### Kdy použít kterou reprezentaci?

**Matice sousednosti:**
- ✅ Hustý graf (hodně hran)
- ✅ Potřebujete rychle zjistit existenci hrany
- ✅ Maticové operace (násobení, mocniny)
- ❌ Řídký graf (plýtvání pamětí)

**Adjacency List:**
- ✅ Řídký graf (málo hran)
- ✅ DFS, BFS průchod
- ✅ Většina moderních algoritmů
- ❌ Pomalé zjištění existence hrany

**Incidenční matice:**
- ✅ Analýza toků
- ✅ Kirchhoffovy zákony
- ✅ Grafy s důležitými hranami
- ❌ Velká paměťová náročnost

**Edge List:**
- ✅ Velmi řídký graf
- ✅ Export/import
- ✅ Jednoduché úpravy
- ❌ Pomalé prohledávání

---

## 🔍 STATISTIKY MATIC

Analyzátor automaticky počítá:

1. **Počty hodnot:**
   - Kolik jedniček, nul, atd.
   - "Matice obsahuje 45 jedniček a 19 nul"

2. **Min/Max hodnoty:**
   - Rozsah hodnot v matici

3. **Stopa matice:**
   - Součet diagonály
   - Pro matici sousednosti = počet smyček

4. **Součty řádků/sloupců:**
   - Součet řádku i = out-degree uzlu i
   - Součet sloupce j = in-degree uzlu j

---

## 📖 PŘÍKLAD KOMPLETNÍ ANALÝZY

Pro graf:
```
A → B
↓   ↓
C → D
```

**Matice sousednosti:**
```
  A B C D
A 0 1 1 0
B 0 0 0 1
C 0 0 0 1
D 0 0 0 0
```
- 3 jedničky, 13 nul
- Nesymetrická → orientovaný
- Stopa = 0 → žádné smyčky

**Charakteristiky uzlů:**
- A: out=2, in=0 → **zdroj**
- B: out=1, in=1
- C: out=1, in=1
- D: out=0, in=2 → **stok**

**Matice délek:**
```
  A B C D
A 0 1 1 2
B ∞ 0 ∞ 1
C ∞ ∞ 0 1
D ∞ ∞ ∞ 0
```
- Z D není cesta nikam → stok

---

## 🎓 ZÁVĚR

Každá matice a charakteristika má své místo:
- **Matice sousednosti** - základ všeho
- **Matice délek** - analýza vzdáleností
- **Laplaceova** - spektrální analýza
- **Stupně uzlů** - lokální vlastnosti
- **Excentricita** - centrality a důležitost

Kombinace všech těchto pohledů dává kompletní obraz o struktuře grafu!

