# Testovací grafy - Sbírka 20 různých grafů

Tato složka obsahuje 20 různorodých testovacích grafů s různými vlastnostmi, velikostmi a strukturami.

## 📊 Přehled grafů

### Graf 01 - Velký orientovaný graf (graph01_large_directed.txt)
- **Uzly:** 25
- **Hrany:** 55+
- **Typ:** Orientovaný
- **Vlastnosti:** Obsahuje cykly, silně propojený, váhy a označení
- **Popis:** Simuluje síť distribuovaných služeb
- **Vhodné pro:** Testování SCC, detekce cyklů, Dijkstra

### Graf 02 - Petersonův graf (graph02_petersen.txt)
- **Uzly:** 10
- **Hrany:** 15
- **Typ:** Neorientovaný
- **Vlastnosti:** Kubický (stupeň 3), není bipartitní, není planární
- **Popis:** Slavný matematický graf
- **Vhodné pro:** Testování bipartitnosti, regularity

### Graf 03 - Velký bipartitní graf (graph03_large_bipartite.txt)
- **Uzly:** 27 (15 zaměstnanců + 12 projektů)
- **Hrany:** 45+
- **Typ:** Neorientovaný bipartitní
- **Vlastnosti:** Bipartitní, vážený
- **Popis:** Přiřazení zaměstnanců k projektům
- **Vhodné pro:** Testování bipartitnosti, matching

### Graf 04 - Komplexní DAG (graph04_dag_complex.txt)
- **Uzly:** 34
- **Hrany:** 60+
- **Typ:** Orientovaný acyklický (DAG)
- **Vlastnosti:** Bez cyklů, mnoho úrovní závislostí
- **Popis:** Kompilační závislosti velkého projektu
- **Vhodné pro:** Topologické řazení, kritická cesta

### Graf 05 - Úplný orientovaný graf (graph05_complete_directed.txt)
- **Uzly:** 12
- **Hrany:** 132 (12×11)
- **Typ:** Orientovaný úplný
- **Vlastnosti:** Každý uzel má hranu do každého jiného
- **Popis:** Úplný turnajový graf
- **Vhodné pro:** Testování úplnosti, husté grafy

### Graf 06 - Těžký multigraf (graph06_multigraph_heavy.txt)
- **Uzly:** 8
- **Hrany:** 60+
- **Typ:** Smíšený multigraf
- **Vlastnosti:** Násobné hrany, smyčky, směs orientovaných/neorientovaných
- **Popis:** Dopravní síť s různými typy spojení
- **Vhodné pro:** Testování multigrafu, smyček

### Graf 07 - Nesouvislý graf (graph07_disconnected.txt)
- **Uzly:** 18
- **Hrany:** 25
- **Typ:** Neorientovaný nesouvislý
- **Vlastnosti:** 5 komponent, 1 izolovaný uzel
- **Popis:** Izolované sociální skupiny
- **Vhodné pro:** Testování souvislosti, komponenty

### Graf 08 - Velký strom (graph08_tree_large.txt)
- **Uzly:** 31
- **Hrany:** 30
- **Typ:** Orientovaný strom
- **Vlastnosti:** Hierarchická struktura, bez cyklů
- **Popis:** Organizační hierarchie firmy
- **Vhodné pro:** Testování stromů, BFS/DFS

### Graf 09 - Hustý neorientovaný graf (graph09_dense_undirected.txt)
- **Uzly:** 20
- **Hrany:** 120+
- **Typ:** Neorientovaný hustý
- **Vlastnosti:** Vysoký stupeň propojení, téměř úplný
- **Popis:** Společenská síť
- **Vhodné pro:** Testování hustých grafů, kliky

### Graf 10 - Řídký orientovaný graf (graph10_sparse_directed.txt)
- **Uzly:** 30
- **Hrany:** 35
- **Typ:** Orientovaný řídký
- **Vlastnosti:** Dlouhá cesta s odbočkami, DAG
- **Popis:** Sekvenční proces s alternativami
- **Vhodné pro:** Testování řídkých grafů, cest

### Graf 11 - Kruhová struktura (graph11_circular.txt)
- **Uzly:** 36
- **Hrany:** 48
- **Typ:** Neorientovaný
- **Vlastnosti:** 3 koncentrické kruhy s paprsky
- **Popis:** Vícevrstevná kruhová síť
- **Vhodné pro:** Testování cyklů, radiální struktury

### Graf 12 - Mřížka (graph12_grid.txt)
- **Uzly:** 64 (8×8)
- **Hrany:** 112
- **Typ:** Neorientovaný grid
- **Vlastnosti:** Pravidelná mřížka, planární
- **Popis:** Šachovnice nebo mapová síť
- **Vhodné pro:** Testování planárních grafů, nejkratší cesty

### Graf 13 - Hvězda (graph13_star.txt)
- **Uzly:** 26
- **Hrany:** 25
- **Typ:** Neorientovaný hvězdicový
- **Vlastnosti:** Jeden centrální uzel, stupeň 25
- **Popis:** Hub-and-spoke topologie
- **Vhodné pro:** Testování excentricity, centrality

### Graf 14 - Náhodný vážený (graph14_random_weighted.txt)
- **Uzly:** 20
- **Hrany:** 35
- **Typ:** Orientovaný vážený
- **Vlastnosti:** Záporné i kladné váhy
- **Popis:** Graf s různými váhami
- **Vhodné pro:** Bellman-Ford, záporné váhy

### Graf 15 - Vrstvený graf (graph15_layered.txt)
- **Uzly:** 28
- **Hrany:** 140+
- **Typ:** Orientovaný feed-forward
- **Vlastnosti:** 4 vrstvy, plně propojené mezi vrstvami
- **Popis:** Neuronová síť
- **Vhodné pro:** Testování vrstvených struktur

### Graf 16 - Turnajový graf (graph16_tournament.txt)
- **Uzly:** 15
- **Hrany:** 105 (15×14/2)
- **Typ:** Orientovaný tournament
- **Vlastnosti:** Mezi každými 2 uzly právě 1 orientovaná hrana
- **Popis:** Sportovní turnaj
- **Vhodné pro:** Testování turnajových grafů, ranking

### Graf 17 - Smíšený graf (graph17_mixed.txt)
- **Uzly:** 20
- **Hrany:** 55+
- **Typ:** Smíšený (orientované + neorientované)
- **Vlastnosti:** Kombinace obou typů hran
- **Popis:** IT síťová infrastruktura
- **Vhodné pro:** Testování smíšených grafů

### Graf 18 - Silně propojený (graph18_highly_connected.txt)
- **Uzly:** 18
- **Hrany:** 110+
- **Typ:** Neorientovaný hustý
- **Vlastnosti:** Vysoký průměrný stupeň (12+)
- **Popis:** Mesh síť
- **Vhodné pro:** Testování hustě propojených sítí

### Graf 19 - Záporné váhy (graph19_negative_weights.txt)
- **Uzly:** 20
- **Hrany:** 45+
- **Typ:** Orientovaný se zápornými váhami
- **Vlastnosti:** Smyčky, záporné váhy, ekonomická síť
- **Popis:** Cash flow síť
- **Vhodné pro:** Bellman-Ford, záporné cykly

### Graf 20 - Komplexní cykly (graph20_complex_cycles.txt)
- **Uzly:** 35
- **Hrany:** 90+
- **Typ:** Orientovaný s mnoha cykly
- **Vlastnosti:** Mnohonásobné cykly různých délek, smyčky
- **Popis:** Komplexní cyklická struktura
- **Vhodné pro:** Detekce cyklů, SCC, složité algoritmy

## 📈 Statistiky

### Podle velikosti:
- **Malé** (< 15 uzlů): Grafy 02, 06, 13
- **Střední** (15-30 uzlů): Grafy 01, 03, 07, 08, 10, 11, 14, 15, 16, 17, 19
- **Velké** (> 30 uzlů): Grafy 04, 05, 09, 12, 18, 20

### Podle typu:
- **Orientované:** 01, 04, 05, 10, 14, 15, 16, 19, 20
- **Neorientované:** 02, 03, 07, 08, 09, 11, 12, 13, 18
- **Smíšené:** 06, 17

### Podle vlastností:
- **S cykly:** 01, 02, 05, 06, 07, 09, 11, 12, 13, 14, 16, 17, 18, 19, 20
- **Acyklické (DAG):** 04, 08, 10, 15
- **Bipartitní:** 03
- **Úplné:** 05
- **Multigraf:** 06
- **Nesouvislé:** 07
- **Se smyčkami:** 06, 19, 20
- **Se zápornými váhami:** 14, 19

## 🎯 Doporučené použití

### Pro zkoušky:
- Vyberte náhodně 3-5 grafů různých typů
- Grafy jsou dostatečně velké, aby nebylo vidět vlastnosti na první pohled
- Každý graf má jiné vlastnosti pro komplexní testování

### Pro testování algoritmů:
- **Dijkstra:** 01, 05, 09, 12, 17
- **Bellman-Ford:** 14, 19
- **Detekce cyklů:** 01, 06, 20
- **Topologické řazení:** 04, 08, 10, 15
- **SCC (Tarjan):** 01, 05, 16, 20
- **Bipartitnost:** 02, 03, 07
- **MST (Kruskal):** 09, 11, 12, 18
- **Souvislost:** 07, 13

## 📝 Použití

```bash
# Analyzovat libovolný graf
python3 main.py graphs/graph01_large_directed.txt

# Matice
python3 matrix_analyzer.py graphs/graph12_grid.txt

# Pokročilé algoritmy
python3 advanced_algorithms.py graphs/graph04_dag_complex.txt

# Komplexní analýza
python3 analyze.py graphs/graph20_complex_cycles.txt --all
```

## 💡 Tipy

1. **Náhodný výběr:** Použijte různé grafy pro každou zkoušku
2. **Kombinace vlastností:** Každý graf testuje jiné vlastnosti
3. **Velikost:** Větší grafy jsou složitější na analýzu pouhým pohledem
4. **Diverzita:** Pokrývají všechny důležité typy a vlastnosti grafů

