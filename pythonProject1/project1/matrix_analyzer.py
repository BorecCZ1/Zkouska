#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rozšířený analyzátor matic grafu
Implementuje všechny typy matic a detailní statistiky
"""

import sys
from typing import List, Dict, Tuple, Set
from collections import Counter
import main as graph_module


class MatrixAnalyzer:
    """Třída pro komplexní analýzu matic grafu a vlastností uzlů"""
    
    def __init__(self, graph: graph_module.Graph):
        self.graph = graph
        self.nodes_list = sorted(graph.nodes.keys())
        self.node_to_index = {node: i for i, node in enumerate(self.nodes_list)}
    
    # ==================== MATICE SOUSEDNOSTI ====================
    
    def get_adjacency_matrix(self) -> List[List[int]]:
        """
        MATICE SOUSEDNOSTI (Adjacency Matrix)
        
        Popis: Čtvercová matice reprezentující spojení mezi uzly.
        
        Použití:
        - Základní reprezentace grafu
        - Rychlé zjištění, zda existuje hrana mezi dvěma uzly
        - Výpočet počtu cest délky k (A^k)
        
        Formát:
        - M[i][j] = počet hran z uzlu i do uzlu j
        - Pro neorientovaný graf: M[i][j] = M[j][i]
        - Diagonála obsahuje počet smyček
        
        Vlastnosti:
        - Symetrická pro neorientované grafy
        - Nesymetrická pro orientované grafy
        - Stopa matice = počet smyček
        """
        n = len(self.nodes_list)
        matrix = [[0] * n for _ in range(n)]
        
        for edge in self.graph.edges:
            i = self.node_to_index[edge.from_node]
            j = self.node_to_index[edge.to_node]
            
            if edge.directed:
                matrix[i][j] += 1
            else:
                matrix[i][j] += 1
                matrix[j][i] += 1
        
        return matrix
    
    def get_weighted_adjacency_matrix(self) -> List[List[float]]:
        """
        VÁŽENÁ MATICE SOUSEDNOSTI (Weighted Adjacency Matrix)
        
        Popis: Matice sousednosti s váhami hran místo počtu hran.
        
        Použití:
        - Algoritmy nejkratší cesty (Dijkstra, Floyd-Warshall)
        - Minimální kostra (MST)
        - Síťové toky
        
        Formát:
        - M[i][j] = váha hrany z i do j (0 pokud hrana neexistuje)
        - Pro násobné hrany se váhy sčítají
        
        Výhody:
        - Umožňuje práci s ohodnocenými grafy
        - Přímé použití v algoritmech optimalizace
        """
        n = len(self.nodes_list)
        matrix = [[0.0] * n for _ in range(n)]
        
        for edge in self.graph.edges:
            i = self.node_to_index[edge.from_node]
            j = self.node_to_index[edge.to_node]
            weight = edge.weight if edge.weight is not None else 1.0
            
            if edge.directed:
                matrix[i][j] += weight
            else:
                matrix[i][j] += weight
                matrix[j][i] += weight
        
        return matrix
    
    # ==================== MATICE INCIDENCE ====================
    
    def get_incidence_matrix(self) -> List[List[int]]:
        """
        INCIDENČNÍ MATICE (Incidence Matrix)
        
        Popis: Matice znázorňující vztah mezi uzly a hranami.
        
        Použití:
        - Reprezentace grafu pro některé algoritmy
        - Analýza toků v síti
        - Kirchhoffovy zákony v elektrických obvodech
        
        Formát:
        - Rozměr: n × m (uzly × hrany)
        - Pro orientované grafy:
          * M[i][j] = 1 pokud z uzlu i vychází hrana j
          * M[i][j] = -1 pokud do uzlu i vstupuje hrana j
          * M[i][j] = 2 pro smyčku
        - Pro neorientované grafy:
          * M[i][j] = 1 pokud uzel i inciduje s hranou j
        
        Vlastnosti:
        - Každý sloupec má právě dva nenulové prvky (kromě smyček)
        - Součet sloupce = 0 pro orientované grafy (kromě smyček)
        """
        n = len(self.nodes_list)
        m = len(self.graph.edges)
        matrix = [[0] * m for _ in range(n)]
        
        for j, edge in enumerate(self.graph.edges):
            i_from = self.node_to_index[edge.from_node]
            i_to = self.node_to_index[edge.to_node]
            
            if edge.from_node == edge.to_node:
                # Smyčka
                matrix[i_from][j] = 2
            elif edge.directed:
                matrix[i_from][j] = 1   # Z uzlu vychází
                matrix[i_to][j] = -1    # Do uzlu vstupuje
            else:
                matrix[i_from][j] = 1
                matrix[i_to][j] = 1
        
        return matrix
    
    # ==================== TABULKA INCIDENTNÍCH HRAN ====================
    
    def get_edge_list_table(self) -> List[Dict]:
        """
        TABULKA INCIDENTNÍCH HRAN (Edge List Table)
        
        Popis: Seznam všech hran s jejich vlastnostmi.
        
        Použití:
        - Kompaktní reprezentace řídkých grafů
        - Export/import grafů
        - Lidsky čitelná reprezentace
        
        Formát: Seznam slovníků, každý obsahuje:
        - from_node: počáteční uzel
        - to_node: koncový uzel
        - weight: váha hrany
        - label: označení hrany
        - directed: typ hrany (orientovaná/neorientovaná)
        
        Výhody:
        - Úsporná paměť pro řídké grafy
        - Snadné přidávání/odebírání hran
        """
        edge_list = []
        for i, edge in enumerate(self.graph.edges):
            edge_list.append({
                'id': i + 1,
                'from': edge.from_node,
                'to': edge.to_node,
                'weight': edge.weight,
                'label': edge.label,
                'type': '→' if edge.directed else '—',
                'directed': edge.directed
            })
        return edge_list
    
    # ==================== DYNAMICKÉ SEZNAMY ====================
    
    def get_adjacency_list(self) -> Dict[str, List[str]]:
        """
        DYNAMICKÝ SEZNAM SOUSEDŮ (Adjacency List)
        
        Popis: Pro každý uzel seznam jeho sousedů.
        
        Použití:
        - Efektivní reprezentace pro řídké grafy
        - DFS a BFS algoritmy
        - Rychlý průchod grafu
        
        Formát:
        - Slovník: {uzel: [seznam_sousedů]}
        - Pro orientované: pouze následníci
        - Pro neorientované: všichni sousedé
        
        Výhody:
        - O(1) přístup k sousedům uzlu
        - Paměťově efektivní pro řídké grafy
        - Rychlé iterace přes sousedy
        """
        adj_list = {node: [] for node in self.nodes_list}
        
        for edge in self.graph.edges:
            if edge.directed:
                adj_list[edge.from_node].append(edge.to_node)
            else:
                adj_list[edge.from_node].append(edge.to_node)
                if edge.from_node != edge.to_node:  # Ne smyčka
                    adj_list[edge.to_node].append(edge.from_node)
        
        return adj_list
    
    def get_node_edge_lists(self) -> Dict[str, Dict]:
        """
        DYNAMICKÝ SEZNAM UZLŮ A HRAN
        
        Popis: Kompletní informace o uzlech a jejich hranách.
        
        Formát pro každý uzel:
        - out_edges: hrany vystupující z uzlu
        - in_edges: hrany vstupující do uzlu
        - all_edges: všechny incidentní hrany
        """
        node_edges = {node: {'out': [], 'in': [], 'all': []} for node in self.nodes_list}
        
        for edge in self.graph.edges:
            edge_info = {
                'to': edge.to_node,
                'from': edge.from_node,
                'weight': edge.weight,
                'label': edge.label
            }
            
            if edge.directed:
                node_edges[edge.from_node]['out'].append(edge_info)
                node_edges[edge.to_node]['in'].append(edge_info)
                node_edges[edge.from_node]['all'].append(edge_info)
                if edge.from_node != edge.to_node:
                    node_edges[edge.to_node]['all'].append(edge_info)
            else:
                node_edges[edge.from_node]['all'].append(edge_info)
                if edge.from_node != edge.to_node:
                    node_edges[edge.to_node]['all'].append(edge_info)
        
        return node_edges
    
    # ==================== MATICE DÉLEK ====================
    
    def get_distance_matrix(self) -> List[List[float]]:
        """
        MATICE DÉLEK / VZDÁLENOSTÍ (Distance Matrix)
        
        Popis: Matice nejkratších vzdáleností mezi všemi páry uzlů.
        
        Použití:
        - Analýza dostupnosti v grafu
        - Výpočet průměru a poloměru grafu
        - Centrum grafu
        - Metrické vlastnosti grafu
        
        Algoritmus: Floyd-Warshall (O(n³))
        
        Formát:
        - M[i][j] = délka nejkratší cesty z i do j
        - M[i][i] = 0 (vzdálenost k sobě samému)
        - M[i][j] = ∞ pokud neexistuje cesta
        
        Vlastnosti:
        - Symetrická pro neorientované grafy
        - Obsahuje všechny nejkratší cesty
        """
        n = len(self.nodes_list)
        INF = float('inf')
        
        # Inicializace
        dist = [[INF] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
        
        # Nastavit vzdálenosti podle hran
        for edge in self.graph.edges:
            i = self.node_to_index[edge.from_node]
            j = self.node_to_index[edge.to_node]
            weight = edge.weight if edge.weight is not None else 1.0
            
            if edge.directed:
                dist[i][j] = min(dist[i][j], weight)
            else:
                dist[i][j] = min(dist[i][j], weight)
                dist[j][i] = min(dist[j][i], weight)
        
        # Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return dist
    
    # ==================== ZNAMÉNKOVÁ MATICE ====================
    
    def get_signed_matrix(self) -> List[List[int]]:
        """
        ZNAMÉNKOVÁ MATICE (Signed Matrix)
        
        Popis: Matice zobrazující směr hran pomocí znaménka.
        
        Použití:
        - Analýza orientace hran
        - Detekce bilančních uzlů (součet řádku = 0)
        - Toky v sítích
        
        Formát:
        - M[i][j] = +1 pokud existuje hrana z i do j
        - M[i][j] = -1 pokud existuje hrana z j do i
        - M[i][j] = 0 pokud neexistuje přímá hrana
        - M[i][i] = 0 (bez smyček na diagonále)
        
        Vlastnosti:
        - Antisymetrická: M[i][j] = -M[j][i]
        - Součet řádku = out-degree - in-degree
        """
        n = len(self.nodes_list)
        matrix = [[0] * n for _ in range(n)]
        
        for edge in self.graph.edges:
            i = self.node_to_index[edge.from_node]
            j = self.node_to_index[edge.to_node]
            
            if i != j:  # Ignorovat smyčky
                if edge.directed:
                    matrix[i][j] = 1
                    matrix[j][i] = -1
                # Pro neorientované hrany necháme 0
        
        return matrix
    
    # ==================== DALŠÍ SPECIALIZOVANÉ MATICE ====================
    
    def get_degree_matrix(self) -> List[List[int]]:
        """
        MATICE STUPŇŮ (Degree Matrix)
        
        Popis: Diagonální matice se stupni uzlů.
        
        Použití:
        - Výpočet Laplaceovy matice (L = D - A)
        - Spektrální analýza grafu
        - Náhodné procházky grafem
        
        Formát:
        - M[i][i] = stupeň uzlu i
        - M[i][j] = 0 pro i ≠ j
        """
        n = len(self.nodes_list)
        matrix = [[0] * n for _ in range(n)]
        
        for i, node in enumerate(self.nodes_list):
            matrix[i][i] = self.graph.get_degree(node)
        
        return matrix
    
    def get_laplacian_matrix(self) -> List[List[int]]:
        """
        LAPLACEOVA MATICE (Laplacian Matrix)
        
        Popis: L = D - A (matice stupňů mínus matice sousednosti)
        
        Použití:
        - Spektrální analýza grafu
        - Detekce komunit
        - Počet koster grafu (Kirchhoffova věta)
        - Náhodné procházky
        
        Vlastnosti:
        - Symetrická pro neorientované grafy
        - Součet řádku = 0
        - Nejmenší vlastní číslo = 0
        - Algebraická souvislost grafu
        """
        n = len(self.nodes_list)
        adj_matrix = self.get_adjacency_matrix()
        laplacian = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    laplacian[i][j] = sum(adj_matrix[i])
                else:
                    laplacian[i][j] = -adj_matrix[i][j]
        
        return laplacian
    
    def get_reachability_matrix(self) -> List[List[int]]:
        """
        MATICE DOSAŽITELNOSTI (Reachability Matrix)
        
        Popis: Matice udávající, které uzly jsou dosažitelné z kterých.
        
        Algoritmus: Warshallův algoritmus (O(n³))
        
        Použití:
        - Testování souvislosti
        - Tranziivní uzávěr relace
        - Analýza dosažitelnosti
        
        Formát:
        - M[i][j] = 1 pokud existuje cesta z i do j
        - M[i][j] = 0 pokud neexistuje cesta
        """
        n = len(self.nodes_list)
        reach = [[0] * n for _ in range(n)]
        
        for i in range(n):
            reach[i][i] = 1
        
        for edge in self.graph.edges:
            i = self.node_to_index[edge.from_node]
            j = self.node_to_index[edge.to_node]
            
            if edge.directed:
                reach[i][j] = 1
            else:
                reach[i][j] = 1
                reach[j][i] = 1
        
        # Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
        
        return reach
    
    # ==================== STATISTIKY MATIC ====================
    
    def get_matrix_statistics(self, matrix: List[List], name: str) -> Dict:
        """
        STATISTIKY MATICE
        
        Vrací kompletní statistické informace o matici:
        - Počty jednotlivých hodnot
        - Minimální a maximální hodnota
        - Součty řádků a sloupců
        - Stopa (součet diagonály)
        """
        if not matrix or not matrix[0]:
            return {}
        
        n = len(matrix)
        m = len(matrix[0])
        
        # Sběr všech hodnot
        all_values = []
        for row in matrix:
            for val in row:
                if val != float('inf'):
                    all_values.append(val)
        
        # Počítání hodnot
        value_counts = Counter(all_values)
        
        # Součty
        row_sums = [sum(row) if all(v != float('inf') for v in row) else None for row in matrix]
        col_sums = []
        for j in range(m):
            col_sum = sum(matrix[i][j] for i in range(n) if matrix[i][j] != float('inf'))
            col_sums.append(col_sum)
        
        # Stopa (pro čtvercové matice)
        trace = sum(matrix[i][i] for i in range(min(n, m)) if matrix[i][i] != float('inf')) if n == m else None
        
        # Nenulové prvky
        non_zero = sum(1 for v in all_values if v != 0)
        zero_count = sum(1 for v in all_values if v == 0)
        
        stats = {
            'name': name,
            'dimensions': (n, m),
            'total_elements': n * m,
            'value_counts': dict(value_counts),
            'non_zero_count': non_zero,
            'zero_count': zero_count,
            'min_value': min(all_values) if all_values else None,
            'max_value': max(all_values) if all_values else None,
            'trace': trace,
            'row_sums': row_sums,
            'col_sums': col_sums
        }
        
        return stats
    
    def find_value_in_matrix(self, matrix: List[List], search_value, name: str = "matice"):
        """
        Vyhledá všechny výskyty hodnoty v matici a vrátí jejich indexy
        """
        results = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                val = matrix[i][j]
                # Porovnání s tolerancí pro float
                if isinstance(val, float) and isinstance(search_value, (int, float)):
                    if abs(val - float(search_value)) < 1e-10:
                        results.append((i, j, val))
                elif val == search_value:
                    results.append((i, j, val))
        
        return results
    
    def print_matrix_statistics(self, stats: Dict, matrix: List[List] = None):
        """Vytiskne statistiky matice s interaktivním výběrem hodnot"""
        print(f"\n📊 STATISTIKY: {stats['name']}")
        print("─" * 80)
        print(f"  Rozměr: {stats['dimensions'][0]} × {stats['dimensions'][1]}")
        print(f"  Celkem prvků: {stats['total_elements']}")
        
        print(f"\n  Nenulové prvky: {stats['non_zero_count']}")
        print(f"  Nulové prvky: {stats['zero_count']}")
        
        if stats['min_value'] is not None:
            print(f"  Minimální hodnota: {stats['min_value']}")
        if stats['max_value'] is not None:
            print(f"  Maximální hodnota: {stats['max_value']}")
        
        if stats['trace'] is not None:
            print(f"  Stopa matice (součet diagonály): {stats['trace']}")
        
        # Interaktivní výběr pro výpis hodnot
        print(f"\n  📋 Počty hodnot v matici:")
        print(f"     Celkem různých hodnot: {len(stats['value_counts'])}")
        
        if len(stats['value_counts']) <= 10:
            # Pokud je málo hodnot, vypíšeme všechny automaticky
            for value, count in sorted(stats['value_counts'].items()):
                if value == 0:
                    print(f"       Nuly (0): {count} prvků")
                elif value == 1:
                    print(f"       Jedničky (1): {count} prvků")
                elif value == -1:
                    print(f"       Mínus jedničky (-1): {count} prvků")
                else:
                    print(f"       Hodnota {value}: {count} prvků")
        else:
            # Pokud je moc hodnot, nabídneme výběr
            print(f"\n     ℹ️  Matice má příliš mnoho různých hodnot ({len(stats['value_counts'])})")
            print(f"     Volby:")
            print(f"       [v]šechny  - Vypsat všechny hodnoty")
            print(f"       [s]pecif   - Zadat konkrétní hodnotu k vyhledání")
            print(f"       [p]řeskoč  - Přeskočit výpis hodnot")
            
            try:
                choice = input("\n     Vaše volba (v/s/p): ").strip().lower()
                
                if choice == 'v':
                    print(f"\n     Výpis všech hodnot:")
                    for value, count in sorted(stats['value_counts'].items()):
                        if value == 0:
                            print(f"       Nuly (0): {count} prvků")
                        elif value == 1:
                            print(f"       Jedničky (1): {count} prvků")
                        elif value == -1:
                            print(f"       Mínus jedničky (-1): {count} prvků")
                        else:
                            print(f"       Hodnota {value}: {count} prvků")
                
                elif choice == 's':
                    value_str = input(f"     Zadejte hodnotu k vyhledání: ").strip()
                    try:
                        # Zkusit převést na číslo
                        search_value = float(value_str) if '.' in value_str else int(value_str)
                        
                        if matrix is not None:
                            results = self.find_value_in_matrix(matrix, search_value, stats['name'])
                            
                            print(f"\n     🔍 Výsledky hledání pro hodnotu {search_value}:")
                            print(f"        Nalezeno: {len(results)} výskytů\n")
                            
                            if len(results) <= 50:
                                # Vypíšeme všechny výskyty
                                for i, (row_idx, col_idx, val) in enumerate(results, 1):
                                    row_node = self.nodes_list[row_idx] if row_idx < len(self.nodes_list) else f"[{row_idx}]"
                                    col_node = self.nodes_list[col_idx] if col_idx < len(self.nodes_list) else f"[{col_idx}]"
                                    print(f"        {i}. matrix[{row_idx}][{col_idx}] ({row_node} → {col_node}) = {val}")
                            else:
                                # Příliš mnoho, ukážeme jen prvních 50
                                for i, (row_idx, col_idx, val) in enumerate(results[:50], 1):
                                    row_node = self.nodes_list[row_idx] if row_idx < len(self.nodes_list) else f"[{row_idx}]"
                                    col_node = self.nodes_list[col_idx] if col_idx < len(self.nodes_list) else f"[{col_idx}]"
                                    print(f"        {i}. matrix[{row_idx}][{col_idx}] ({row_node} → {col_node}) = {val}")
                                print(f"        ... a dalších {len(results) - 50} výskytů")
                        else:
                            if search_value in stats['value_counts']:
                                print(f"\n     Hodnota {search_value}: {stats['value_counts'][search_value]} prvků")
                            else:
                                print(f"\n     Hodnota {search_value} se v matici nevyskytuje")
                    
                    except ValueError:
                        print(f"     ❌ Chyba: '{value_str}' není platné číslo")
                
                # 'p' nebo cokoliv jiného = přeskočit
            
            except EOFError:
                # Pokud není vstup (batch mode), přeskočit
                pass
    
    # ==================== DETAILNÍ CHARAKTERISTIKY UZLŮ ====================
    
    def get_node_characteristics(self, node: str) -> Dict:
        """
        KOMPLETNÍ CHARAKTERISTIKY UZLU
        
        Vrací všechny možné charakteristiky daného uzlu:
        - Stupně (vstupní, výstupní, celkový)
        - Sousedé, předchůdci, následníci
        - Excentricita
        - Incidentní hrany
        - Pozice v matici
        """
        node_idx = self.node_to_index[node]
        
        # Základní informace
        node_obj = self.graph.nodes[node]
        
        # Stupně
        in_degree = self.graph.get_in_degree(node)
        out_degree = self.graph.get_out_degree(node)
        total_degree = self.graph.get_degree(node)
        
        # Sousedé
        predecessors = self.graph.get_predecessors(node)
        successors = self.graph.get_successors(node)
        all_neighbors = self.graph.get_all_neighbors(node)
        
        # Excentricita (maximální vzdálenost)
        dist_matrix = self.get_distance_matrix()
        eccentricity = 0
        for j, other_node in enumerate(self.nodes_list):
            if node != other_node and dist_matrix[node_idx][j] != float('inf'):
                eccentricity = max(eccentricity, dist_matrix[node_idx][j])
        
        # Incidentní hrany
        incident_edges = []
        for edge in self.graph.edges:
            if edge.from_node == node or edge.to_node == node:
                incident_edges.append({
                    'from': edge.from_node,
                    'to': edge.to_node,
                    'type': '→' if edge.directed else '—',
                    'weight': edge.weight,
                    'label': edge.label
                })
        
        characteristics = {
            'node_name': node,
            'node_weight': node_obj.weight,
            'index_in_matrix': node_idx,
            
            # Stupně
            'in_degree': in_degree,
            'out_degree': out_degree,
            'total_degree': total_degree,
            
            # Sousedé
            'predecessors': sorted(predecessors),
            'successors': sorted(successors),
            'all_neighbors': sorted(all_neighbors),
            'neighbor_count': len(all_neighbors),
            
            # Excentricita a vzdálenosti
            'eccentricity': eccentricity if eccentricity > 0 else float('inf'),
            
            # Hrany
            'incident_edges_count': len(incident_edges),
            'incident_edges': incident_edges,
            
            # Speciální vlastnosti
            'is_isolated': total_degree == 0,
            'has_self_loop': any(e.from_node == node and e.to_node == node for e in self.graph.edges),
            'is_source': in_degree == 0 and out_degree > 0,
            'is_sink': in_degree > 0 and out_degree == 0,
        }
        
        return characteristics
    
    # ==================== TISK VÝSLEDKŮ ====================
    
    def print_matrix(self, matrix: List[List], title: str, is_float: bool = False):
        """Vytiskne matici v čitelném formátu (jen pokud je max 20x20)"""
        print(f"\n{title}:")
        print("─" * 80)
        
        if not matrix:
            print("  (Matice je prázdná)")
            return
        
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        
        # Pokud je matice příliš velká, vypíšeme jen info
        if rows > 20 or cols > 20:
            print(f"  ℹ️  Matice je příliš velká na vypsání ({rows}×{cols})")
            print(f"     (Zobrazují se pouze matice o velikosti max 20×20)")
            return
        
        # Hlavička sloupců
        header = "      " + "  ".join(f"{node:>6}" for node in self.nodes_list)
        print(header)
        print("─" * 80)
        
        # Řádky matice
        for i, node in enumerate(self.nodes_list):
            if is_float:
                row_str = "  ".join(
                    f"{val:>6.1f}" if val != float('inf') else "   ∞  " 
                    for val in matrix[i]
                )
            else:
                row_str = "  ".join(f"{val:>6}" for val in matrix[i])
            print(f"{node:>5} {row_str}")
        print()
    
    def print_incidence_matrix(self, matrix: List[List]):
        """Vytiskne incidenční matici (jen pokud je max 20x20)"""
        print("\n📋 INCIDENČNÍ MATICE (Incidence Matrix):")
        print("─" * 100)
        
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        
        # Pokud je matice příliš velká, vypíšeme jen info
        if rows > 20 or cols > 20:
            print(f"  ℹ️  Incidenční matice je příliš velká na vypsání ({rows}×{cols})")
            print(f"     (Zobrazují se pouze matice o velikosti max 20×20)")
            print(f"\n  Matice incidenční:")
            print(f"    - Řádky: {rows} uzlů")
            print(f"    - Sloupce: {cols} hran")
            return
        
        # Hlavička sloupců (názvy hran)
        edge_labels = []
        for i, edge in enumerate(self.graph.edges):
            if edge.label:
                edge_labels.append(edge.label[:6])
            else:
                direction = "→" if edge.directed else "—"
                label = f"{edge.from_node[:3]}{direction}{edge.to_node[:3]}"
                edge_labels.append(label[:6])
        
        header = "      " + "  ".join(f"{label:>6}" for label in edge_labels)
        print(header)
        print("─" * 100)
        
        # Řádky matice
        for i, node in enumerate(self.nodes_list):
            row_str = "  ".join(f"{val:>6}" for val in matrix[i])
            print(f"{node:>5} {row_str}")
        print()
    
    def print_node_characteristics(self, node: str):
        """Vytiskne všechny charakteristiky uzlu"""
        char = self.get_node_characteristics(node)
        
        print(f"\n{'='*80}")
        print(f"KOMPLETNÍ CHARAKTERISTIKY UZLU: {node}")
        print(f"{'='*80}")
        
        print(f"\n📌 ZÁKLADNÍ INFORMACE:")
        print(f"  Název uzlu: {char['node_name']}")
        if char['node_weight'] is not None:
            print(f"  Ohodnocení uzlu: {char['node_weight']}")
        print(f"  Index v matici: {char['index_in_matrix']}")
        
        print(f"\n📊 STUPNĚ:")
        print(f"  Vstupní stupeň (in-degree): {char['in_degree']}")
        print(f"    → Počet hran vstupujících DO tohoto uzlu")
        print(f"  Výstupní stupeň (out-degree): {char['out_degree']}")
        print(f"    → Počet hran vystupujících Z tohoto uzlu")
        print(f"  Celkový stupeň: {char['total_degree']}")
        print(f"    → Součet vstupního a výstupního stupně")
        
        print(f"\n👥 SOUSEDÉ A RELACE:")
        print(f"  Předchůdci (predecessors): {char['predecessors'] if char['predecessors'] else '(žádní)'}")
        print(f"    → Uzly, ze kterých vede hrana DO tohoto uzlu")
        print(f"  Následníci (successors): {char['successors'] if char['successors'] else '(žádní)'}")
        print(f"    → Uzly, do kterých vede hrana Z tohoto uzlu")
        print(f"  Všichni sousedé: {char['all_neighbors'] if char['all_neighbors'] else '(žádní)'}")
        print(f"    → Všechny sousední uzly (bez ohledu na směr)")
        print(f"  Počet sousedů: {char['neighbor_count']}")
        
        print(f"\n📏 VZDÁLENOSTI:")
        ecc = char['eccentricity']
        if ecc != float('inf'):
            print(f"  Excentricita: {ecc}")
            print(f"    → Největší vzdálenost k ostatním uzlům")
        else:
            print(f"  Excentricita: ∞ (uzel je nedosažitelný nebo izolovaný)")
        
        print(f"\n🔗 INCIDENTNÍ HRANY:")
        print(f"  Počet incidentních hran: {char['incident_edges_count']}")
        if char['incident_edges']:
            for i, edge in enumerate(char['incident_edges'], 1):
                weight_str = f", váha={edge['weight']}" if edge['weight'] else ""
                label_str = f", '{edge['label']}'" if edge['label'] else ""
                print(f"    {i}. {edge['from']} {edge['type']} {edge['to']}{weight_str}{label_str}")
        
        print(f"\n✨ SPECIÁLNÍ VLASTNOSTI:")
        print(f"  Je izolovaný: {'✓ Ano' if char['is_isolated'] else '✗ Ne'}")
        print(f"    → Uzel bez jakýchkoliv hran")
        print(f"  Má smyčku: {'✓ Ano' if char['has_self_loop'] else '✗ Ne'}")
        print(f"    → Hrana z uzlu do sebe sama")
        print(f"  Je zdroj (source): {'✓ Ano' if char['is_source'] else '✗ Ne'}")
        print(f"    → Pouze výstupní hrany, žádné vstupní")
        print(f"  Je stok (sink): {'✓ Ano' if char['is_sink'] else '✗ Ne'}")
        print(f"    → Pouze vstupní hrany, žádné výstupní")
        
        print(f"\n{'='*80}")
    
    def print_edge_list_table(self):
        """Vytiskne tabulku incidentních hran"""
        edge_list = self.get_edge_list_table()
        
        print("\n📋 TABULKA INCIDENTNÍCH HRAN:")
        print("─" * 100)
        print(f"  Celkem hran: {len(edge_list)}")
        print(f"  Formát: ID | Z uzlu | Typ | Do uzlu | Váha | Označení")
        print("─" * 100)
        
        # Ukázat jen prvních 15 hran
        edges_to_show = edge_list[:15]
        
        print(f"{'ID':>4} {'Z uzlu':>15} {'Typ':>4} {'Do uzlu':>15} {'Váha':>10} {'Označení':>20}")
        print("─" * 100)
        
        for edge in edges_to_show:
            weight_str = str(edge['weight']) if edge['weight'] is not None else '-'
            label_str = edge['label'] if edge['label'] else '-'
            print(f"{edge['id']:>4} {edge['from']:>15} {edge['type']:>4} {edge['to']:>15} {weight_str:>10} {label_str:>20}")
        
        if len(edge_list) > 15:
            print(f"  ... a dalších {len(edge_list) - 15} hran")
        print()
    
    # ==================== HLAVNÍ ANALÝZA ====================
    
    def analyze_all(self):
        """Provede kompletní analýzu všech matic a charakteristik"""
        print("\n" + "=" * 80)
        print("KOMPLETNÍ ANALÝZA MATIC GRAFU")
        print("=" * 80)
        
        print(f"\n📊 ZÁKLADNÍ INFORMACE:")
        print(f"  Počet uzlů: {len(self.nodes_list)}")
        print(f"  Počet hran: {len(self.graph.edges)}")
        print(f"  Uzly: {self.nodes_list}")
        
        # ========== MATICE SOUSEDNOSTI ==========
        adj_matrix = self.get_adjacency_matrix()
        self.print_matrix(adj_matrix, "📐 MATICE SOUSEDNOSTI (Adjacency Matrix)")
        stats_adj = self.get_matrix_statistics(adj_matrix, "Matice sousednosti")
        self.print_matrix_statistics(stats_adj, adj_matrix)
        
        # ========== VÁŽENÁ MATICE SOUSEDNOSTI ==========
        has_weights = any(edge.weight is not None for edge in self.graph.edges)
        if has_weights:
            weighted_adj = self.get_weighted_adjacency_matrix()
            self.print_matrix(weighted_adj, "⚖️  VÁŽENÁ MATICE SOUSEDNOSTI (Weighted Adjacency)", is_float=True)
            stats_wadj = self.get_matrix_statistics(weighted_adj, "Vážená matice sousednosti")
            self.print_matrix_statistics(stats_wadj, weighted_adj)
        
        # ========== INCIDENČNÍ MATICE ==========
        inc_matrix = self.get_incidence_matrix()
        self.print_incidence_matrix(inc_matrix)
        stats_inc = self.get_matrix_statistics(inc_matrix, "Incidenční matice")
        self.print_matrix_statistics(stats_inc, inc_matrix)
        
        # ========== ZNAMÉNKOVÁ MATICE ==========
        if self.graph.is_oriented():
            signed_matrix = self.get_signed_matrix()
            self.print_matrix(signed_matrix, "➕➖ ZNAMÉNKOVÁ MATICE (Signed Matrix)")
            stats_signed = self.get_matrix_statistics(signed_matrix, "Znaménková matice")
            self.print_matrix_statistics(stats_signed, signed_matrix)
        
        # ========== MATICE STUPŇŮ ==========
        deg_matrix = self.get_degree_matrix()
        self.print_matrix(deg_matrix, "📊 MATICE STUPŇŮ (Degree Matrix)")
        stats_deg = self.get_matrix_statistics(deg_matrix, "Matice stupňů")
        self.print_matrix_statistics(stats_deg, deg_matrix)
        
        # ========== LAPLACEOVA MATICE ==========
        if self.graph.is_unoriented():
            lap_matrix = self.get_laplacian_matrix()
            self.print_matrix(lap_matrix, "🔷 LAPLACEOVA MATICE (Laplacian Matrix L = D - A)")
            stats_lap = self.get_matrix_statistics(lap_matrix, "Laplaceova matice")
            self.print_matrix_statistics(stats_lap, lap_matrix)
        
        # ========== MATICE DOSAŽITELNOSTI ==========
        reach_matrix = self.get_reachability_matrix()
        self.print_matrix(reach_matrix, "🎯 MATICE DOSAŽITELNOSTI (Reachability Matrix - Warshall)")
        stats_reach = self.get_matrix_statistics(reach_matrix, "Matice dosažitelnosti")
        self.print_matrix_statistics(stats_reach, reach_matrix)
        
        # ========== MATICE VZDÁLENOSTÍ ==========
        dist_matrix = self.get_distance_matrix()
        self.print_matrix(dist_matrix, "📏 MATICE DÉLEK/VZDÁLENOSTÍ (Distance Matrix - Floyd-Warshall)", is_float=True)
        # Vzdálenostní matice má ∞, takže statistiky speciálně
        
        # ========== TABULKA INCIDENTNÍCH HRAN ==========
        self.print_edge_list_table()
        
        # ========== DYNAMICKÝ SEZNAM SOUSEDŮ ==========
        print("\n📝 DYNAMICKÝ SEZNAM SOUSEDŮ (Adjacency List):")
        print("─" * 80)
        print("  Pro každý uzel seznam jeho sousedů - paměťově efektivní reprezentace")
        adj_list = self.get_adjacency_list()
        
        # Ukázat jen prvních 10 uzlů, aby to nebylo moc dlouhé
        nodes_to_show = self.nodes_list[:10]
        for node in nodes_to_show:
            neighbors = adj_list[node]
            print(f"  {node}: {neighbors if neighbors else '(žádní sousedé)'}")
        
        if len(self.nodes_list) > 10:
            print(f"  ... a dalších {len(self.nodes_list) - 10} uzlů")
        
        # ========== PŘÍKLAD DETAILNÍCH CHARAKTERISTIK ==========
        print("\n" + "=" * 80)
        print("PŘÍKLAD DETAILNÍCH CHARAKTERISTIK UZLU")
        print("=" * 80)
        print("\nPro zobrazení detailů konkrétního uzlu použijte:")
        print("  viz dokumentace v MATICE_A_VLASTNOSTI.md")
        
        # Ukázat charakteristiky prvního uzlu jako příklad
        if self.nodes_list:
            example_node = self.nodes_list[0]
            print(f"\nPŘÍKLAD pro uzel '{example_node}':")
            self.print_node_characteristics(example_node)
        
        print("\n" + "=" * 80)
        print("KONEC ANALÝZY")
        print("=" * 80)


def main():
    """Hlavní funkce pro analýzu matic"""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║              ROZŠÍŘENÝ ANALYZÁTOR MATIC GRAFU                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    if len(sys.argv) < 2:
        # Interaktivní vstup
        print("\nDostupné testovací soubory:")
        print("  1. test_graph.txt - Orientovaný graf ze zadání")
        print("  2. test_complete_graph.txt - Úplný graf K₄")
        print("  3. test_bipartite_graph.txt - Bipartitní graf K₃,₃")
        print("  4. graphs/graph01_large_directed.txt - Velký orientovaný graf")
        print("  5. graphs/graph03_large_bipartite.txt - Velký bipartitní graf")
        print("  6. graphs/graph12_grid.txt - Mřížka 8×8")
        print()
        
        filename = input("📂 Zadejte cestu k souboru s grafem (nebo stiskněte Enter pro test_complete_graph.txt): ").strip()
        
        if not filename:
            filename = "../graphs/test_complete_graph.txt"
            print(f"   → Použiji výchozí soubor: {filename}")
    else:
        filename = sys.argv[1]
    
    print(f"\n📂 Načítám soubor: {filename}")
    
    # Načíst graf
    graph = graph_module.parse_graph_file(filename)
    print(f"✓ Graf úspěšně načten!\n")
    
    # Analyzovat matice
    analyzer = MatrixAnalyzer(graph)
    analyzer.analyze_all()


if __name__ == '__main__':
    main()
