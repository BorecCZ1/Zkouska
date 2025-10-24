#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skript pro analýzu vlastností grafů
Podporuje všechny operace podle zadání
"""

import sys
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Optional


class Node:
    """Reprezentace uzlu grafu"""
    def __init__(self, identifier: str, weight: Optional[float] = None):
        self.identifier = identifier
        self.weight = weight
    
    def __repr__(self):
        if self.weight is not None:
            return f"Node({self.identifier}, {self.weight})"
        return f"Node({self.identifier})"


class Edge:
    """Reprezentace hrany grafu"""
    def __init__(self, from_node: str, to_node: str, weight: Optional[float] = None, 
                 label: Optional[str] = None, directed: bool = True):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.label = label
        self.directed = directed
    
    def __repr__(self):
        direction = ">" if self.directed else "-"
        return f"Edge({self.from_node} {direction} {self.to_node}, w={self.weight}, l={self.label})"


class Graph:
    """Reprezentace grafu s metodami pro analýzu vlastností"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)  # pro orientované hrany
        self.reverse_adjacency_list: Dict[str, List[str]] = defaultdict(list)  # zpětné hrany
        self.undirected_adjacency: Dict[str, List[str]] = defaultdict(list)  # neorientované hrany
    
    def add_node(self, identifier: str, weight: Optional[float] = None):
        """Přidá uzel do grafu"""
        if identifier not in self.nodes:
            self.nodes[identifier] = Node(identifier, weight)
    
    def add_edge(self, from_node: str, to_node: str, weight: Optional[float] = None,
                 label: Optional[str] = None, directed: bool = True):
        """Přidá hranu do grafu"""
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError(f"Uzly {from_node} nebo {to_node} neexistují!")
        
        edge = Edge(from_node, to_node, weight, label, directed)
        self.edges.append(edge)
        
        if directed:
            self.adjacency_list[from_node].append(to_node)
            self.reverse_adjacency_list[to_node].append(from_node)
        else:
            self.undirected_adjacency[from_node].append(to_node)
            self.undirected_adjacency[to_node].append(from_node)
    
    def get_all_neighbors(self, node: str) -> Set[str]:
        """Vrátí všechny sousedy uzlu (orientované i neorientované)"""
        neighbors = set()
        neighbors.update(self.adjacency_list.get(node, []))
        neighbors.update(self.reverse_adjacency_list.get(node, []))
        neighbors.update(self.undirected_adjacency.get(node, []))
        return neighbors
    
    def get_successors(self, node: str) -> List[str]:
        """Vrátí následníky uzlu (výstupní okolí)"""
        return self.adjacency_list.get(node, [])
    
    def get_predecessors(self, node: str) -> List[str]:
        """Vrátí předchůdce uzlu (vstupní okolí)"""
        return self.reverse_adjacency_list.get(node, [])
    
    def get_out_degree(self, node: str) -> int:
        """Výstupní stupeň uzlu"""
        return len(self.adjacency_list.get(node, []))
    
    def get_in_degree(self, node: str) -> int:
        """Vstupní stupeň uzlu"""
        return len(self.reverse_adjacency_list.get(node, []))
    
    def get_degree(self, node: str) -> int:
        """Celkový stupeň uzlu"""
        directed_degree = self.get_out_degree(node) + self.get_in_degree(node)
        undirected_degree = len(self.undirected_adjacency.get(node, []))
        return directed_degree + undirected_degree
    
    def is_oriented(self) -> bool:
        """Zjistí, zda je graf orientovaný"""
        return any(edge.directed for edge in self.edges)
    
    def is_unoriented(self) -> bool:
        """Zjistí, zda je graf neorientovaný"""
        return all(not edge.directed for edge in self.edges)
    
    def has_loops(self) -> bool:
        """Zjistí, zda graf obsahuje smyčky"""
        return any(edge.from_node == edge.to_node for edge in self.edges)
    
    def get_loops(self) -> List[Edge]:
        """Vrátí seznam všech smyček"""
        return [edge for edge in self.edges if edge.from_node == edge.to_node]
    
    def has_multiple_edges(self) -> bool:
        """Zjistí, zda graf obsahuje násobné hrany"""
        edge_set = set()
        for edge in self.edges:
            if edge.directed:
                edge_tuple = (edge.from_node, edge.to_node)
            else:
                # Pro neorientované hrany normalizujeme pořadí
                edge_tuple = tuple(sorted([edge.from_node, edge.to_node]))
            
            if edge_tuple in edge_set:
                return True
            edge_set.add(edge_tuple)
        return False
    
    def is_simple(self) -> bool:
        """Zjistí, zda je graf jednoduchý (bez smyček a násobných hran)"""
        return not self.has_loops() and not self.has_multiple_edges()
    
    def is_multigraph(self) -> bool:
        """Zjistí, zda je graf multigraf"""
        return self.has_multiple_edges()
    
    def is_discrete(self) -> bool:
        """Zjistí, zda je graf diskrétní (bez hran)"""
        return len(self.edges) == 0
    
    def get_isolated_nodes(self) -> List[str]:
        """Vrátí izolované uzly (bez hran)"""
        isolated = []
        for node_id in self.nodes:
            if self.get_degree(node_id) == 0:
                isolated.append(node_id)
        return isolated
    
    def is_connected(self) -> bool:
        """Zjistí, zda je graf souvislý (pro neorientovaný nebo symetrizovaný orientovaný)"""
        if len(self.nodes) == 0:
            return True
        
        # BFS z prvního uzlu
        start_node = next(iter(self.nodes.keys()))
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        
        while queue:
            current = queue.popleft()
            neighbors = self.get_all_neighbors(current)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.nodes)
    
    def is_complete(self) -> bool:
        """Zjistí, zda je graf úplný"""
        n = len(self.nodes)
        if n <= 1:
            return True
        
        # Pro neorientovaný graf: každý uzel musí být spojen se všemi ostatními
        if self.is_unoriented():
            for node in self.nodes:
                neighbors = set(self.undirected_adjacency.get(node, []))
                expected_neighbors = set(self.nodes.keys()) - {node}
                if neighbors != expected_neighbors:
                    return False
            return True
        
        # Pro orientovaný graf: mezi každými dvěma uzly musí být obě hrany
        if self.is_oriented():
            for node1 in self.nodes:
                for node2 in self.nodes:
                    if node1 != node2:
                        if node2 not in self.adjacency_list.get(node1, []):
                            return False
            return True
        
        return False
    
    def is_regular(self) -> Optional[int]:
        """Zjistí, zda je graf regulární. Vrací stupeň nebo None."""
        if len(self.nodes) == 0:
            return 0
        
        degrees = [self.get_degree(node) for node in self.nodes]
        first_degree = degrees[0]
        
        if all(d == first_degree for d in degrees):
            return first_degree
        return None
    
    def is_bipartite(self) -> Tuple[bool, Optional[Tuple[Set[str], Set[str]]]]:
        """
        Zjistí, zda je graf bipartitní pomocí 2-obarvení.
        Vrací (is_bipartite, (set1, set2)) nebo (False, None)
        """
        if len(self.nodes) == 0:
            return True, (set(), set())
        
        color = {}
        set1, set2 = set(), set()
        
        # Procházíme všechny komponenty souvislosti
        for start_node in self.nodes:
            if start_node in color:
                continue
            
            # BFS s obarvováním
            queue = deque([start_node])
            color[start_node] = 0
            set1.add(start_node)
            
            while queue:
                current = queue.popleft()
                current_color = color[current]
                next_color = 1 - current_color
                
                neighbors = self.get_all_neighbors(current)
                
                for neighbor in neighbors:
                    if neighbor not in color:
                        color[neighbor] = next_color
                        if next_color == 0:
                            set1.add(neighbor)
                        else:
                            set2.add(neighbor)
                        queue.append(neighbor)
                    elif color[neighbor] == current_color:
                        # Soused má stejnou barvu - není bipartitní
                        return False, None
        
        return True, (set1, set2)
    
    def get_symmetrized_graph(self):
        """Vytvoří symetrizovaný graf (z orientovaného udělá neorientovaný)"""
        sym_graph = Graph()
        
        # Přidej všechny uzly
        for node_id, node in self.nodes.items():
            sym_graph.add_node(node_id, node.weight)
        
        # Přidej hrany jako neorientované
        edge_set = set()
        for edge in self.edges:
            edge_tuple = tuple(sorted([edge.from_node, edge.to_node]))
            if edge_tuple not in edge_set:
                sym_graph.add_edge(edge.from_node, edge.to_node, edge.weight, 
                                 edge.label, directed=False)
                edge_set.add(edge_tuple)
        
        return sym_graph
    
    def print_statistics(self):
        """Vypíše kompletní statistiky grafu"""
        print("=" * 80)
        print("ANALÝZA GRAFU")
        print("=" * 80)
        
        print(f"\n📊 ZÁKLADNÍ INFORMACE:")
        print(f"  Počet uzlů (|V|): {len(self.nodes)}")
        print(f"  Počet hran (|E|): {len(self.edges)}")
        print(f"  Seznam uzlů: {sorted(self.nodes.keys())}")
        
        # Ohodnocení
        has_node_weights = any(node.weight is not None for node in self.nodes.values())
        has_edge_weights = any(edge.weight is not None for edge in self.edges)
        
        print(f"\n" + "="*80)
        print("ROZHODNĚTE O NÁSLEDUJÍCÍCH VLASTNOSTECH:")
        print("="*80)
        
        # a) Ohodnocený
        print(f"\na) OHODNOCENÝ:")
        if has_node_weights or has_edge_weights:
            print(f"   ✓ ANO - Graf je ohodnocený")
            if has_node_weights:
                print(f"     → Uzly mají ohodnocení")
            if has_edge_weights:
                print(f"     → Hrany mají váhy")
        else:
            print(f"   ✗ NE - Graf není ohodnocený (žádné váhy)")
        
        # b) Orientovaný
        print(f"\nb) ORIENTOVANÝ:")
        if self.is_unoriented():
            print(f"   ✗ NE - Neorientovaný graf (všechny hrany bez směru)")
        elif self.is_oriented():
            print(f"   ✓ ANO - Orientovaný graf (všechny hrany mají směr)")
        else:
            print(f"   ⚠ ČÁSTEČNĚ - Smíšený graf (obsahuje orientované i neorientované hrany)")
        
        # c) Souvislý
        print(f"\nc) SOUVISLÝ:")
        if self.is_connected():
            print(f"   ✓ ANO - Graf je souvislý")
            print(f"     → Existuje cesta mezi každými dvěma uzly")
        else:
            print(f"   ✗ NE - Graf není souvislý")
            isolated = self.get_isolated_nodes()
            if isolated:
                print(f"     → Izolované uzly: {isolated}")
        
        # d) Prostý
        print(f"\nd) PROSTÝ:")
        if not self.has_multiple_edges():
            print(f"   ✓ ANO - Prostý graf (bez násobných hran)")
            print(f"     → Mezi každými dvěma uzly max. 1 hrana")
        else:
            print(f"   ✗ NE - Multigraf (obsahuje násobné hrany)")
        
        # e) Jednoduchý
        print(f"\ne) JEDNODUCHÝ:")
        loops = self.get_loops()
        if self.is_simple():
            print(f"   ✓ ANO - Jednoduchý graf")
            print(f"     → Bez smyček a násobných hran")
        else:
            print(f"   ✗ NE - Není jednoduchý graf")
            if loops:
                print(f"     → Obsahuje {len(loops)} smyček")
            if self.has_multiple_edges():
                print(f"     → Obsahuje násobné hrany")
        
        # f) Rovinný
        print(f"\nf) ROVINNÝ:")
        print(f"   ? NELZE AUTOMATICKY URČIT")
        print(f"     → Rovinnost je NP-úplný problém")
        print(f"     → Pro malé grafy: zkuste nakreslit bez křížení hran")
        if len(self.nodes) <= 4:
            print(f"     → Graf s max 4 uzly je vždy rovinný")
        
        # g) Konečný
        print(f"\ng) KONEČNÝ:")
        print(f"   ✓ ANO - Graf je konečný")
        print(f"     → Má konečný počet uzlů ({len(self.nodes)}) a hran ({len(self.edges)})")
        
        # h) Úplný
        print(f"\nh) ÚPLNÝ:")
        if self.is_complete():
            print(f"   ✓ ANO - Úplný graf")
            print(f"     → Každý uzel je spojen se všemi ostatními")
            if self.is_unoriented():
                expected = len(self.nodes) * (len(self.nodes) - 1) // 2
                print(f"     → Pro {len(self.nodes)} uzlů: {expected} hran (K_{len(self.nodes)})")
        else:
            print(f"   ✗ NE - Není úplný graf")
        
        # i) Regulární
        print(f"\ni) REGULÁRNÍ:")
        regularity = self.is_regular()
        if regularity is not None:
            print(f"   ✓ ANO - Regulární graf stupně {regularity}")
            print(f"     → Všechny uzly mají stupeň {regularity}")
        else:
            print(f"   ✗ NE - Není regulární graf")
            degrees = [self.get_degree(node) for node in self.nodes]
            print(f"     → Stupně uzlů: min={min(degrees)}, max={max(degrees)}")
        
        # j) Bipartitní
        print(f"\nj) BIPARTITNÍ:")
        is_bip, partition = self.is_bipartite()
        if is_bip:
            print(f"   ✓ ANO - Bipartitní graf")
            if partition:
                set1, set2 = partition
                print(f"     → Partice 1 ({len(set1)} uzlů): {sorted(set1)}")
                print(f"     → Partice 2 ({len(set2)} uzlů): {sorted(set2)}")
        else:
            print(f"   ✗ NE - Není bipartitní graf")
            print(f"     → Nelze rozdělit do dvou množin bez hran uvnitř")
        
        print(f"\n" + "="*80)
        print("DŮLEŽITÉ POJMY A CHARAKTERISTIKY:")
        print("="*80)
        
        print(f"\n🔹 TYPY UZLŮ A HRAN:")
        print(f"  • Graf: Dvojice G = (V, E) kde V jsou uzly a E hrany")
        print(f"  • Uzel (vrchol): Základní prvek grafu | V tomto grafu: {len(self.nodes)} uzlů")
        print(f"  • Hrana: Spojení dvou uzlů | V tomto grafu: {len(self.edges)} hran")
        
        # Incidenční zobrazení
        print(f"\n🔹 INCIDENCE:")
        print(f"  • Incidenční zobrazení: Zobrazení ε: E → V×V přiřazující hraně dvojici uzlů")
        if len(self.edges) > 0:
            edge = self.edges[0]
            print(f"    Příklad: ε({edge.label or 'hrana'}) = ({edge.from_node}, {edge.to_node})")
        
        # Orientované pojmy
        if self.is_oriented() or not self.is_unoriented():
            print(f"\n🔹 ORIENTOVANÝ GRAF - SPECIFICKÉ POJMY:")
            print(f"  • Počáteční uzel: Uzel, ze kterého hrana vychází")
            print(f"  • Koncový uzel: Uzel, do kterého hrana vstupuje")
            print(f"  • Následník: Koncový uzel hrany vycházející z daného uzlu")
            print(f"  • Předchůdce: Počáteční uzel hrany vstupující do daného uzlu")
            print(f"  • Výstupní okolí: Množina všech následníků uzlu")
            print(f"  • Vstupní okolí: Množina všech předchůdců uzlu")
            print(f"  • Výstupní stupeň: Počet hran vycházejících z uzlu")
            print(f"  • Vstupní stupeň: Počet hran vstupujících do uzlu")
        
        print(f"\n🔹 STUPNĚ UZLŮ:")
        degrees = [self.get_degree(node) for node in self.nodes]
        if degrees:
            print(f"  • Minimální stupeň: {min(degrees)}")
            print(f"  • Maximální stupeň: {max(degrees)}")
            print(f"  • Průměrný stupeň: {sum(degrees)/len(degrees):.2f}")
        
        # Speciální uzly
        isolated = self.get_isolated_nodes()
        if isolated:
            print(f"  • Izolované uzly (stupeň 0): {isolated}")
        
        print(f"\n🔹 SPECIÁLNÍ VLASTNOSTI:")
        loops = self.get_loops()
        if loops:
            print(f"  • Smyčky: {len(loops)} (hrana z uzlu do sebe sama)")
        if self.has_multiple_edges():
            print(f"  • Násobné hrany: ANO (multigraf)")
        if self.is_discrete():
            print(f"  • Diskrétní graf: ANO (bez hran)")
        
        print(f"\n🔹 SOUSEDNOST:")
        print(f"  • Sousední uzly: Uzly spojené hranou")
        print(f"  • Soused uzlu: Jakýkoliv uzel spojený hranou (bez ohledu na směr)")
        
        if not self.is_unoriented():
            print(f"\n🔹 SYMETRIZACE:")
            print(f"  • Symetrizace grafu: Převod orientovaného grafu na neorientovaný")
            print(f"    → Z každé orientované hrany se stane neorientovaná")
        
        print(f"\n" + "="*80)


def parse_graph_file(filename: str) -> Graph:
    """Parsuje soubor s grafem podle zadané struktury"""
    graph = Graph()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Soubor '{filename}' nenalezen!")
        sys.exit(1)
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Přeskočit prázdné řádky a komentáře
        if not line or line.startswith('#'):
            continue
        
        # Odstranit středník na konci
        if line.endswith(';'):
            line = line[:-1].strip()
        
        try:
            if line.startswith('u '):
                # Parsování uzlu: u identifikátor [ohodnocení]
                parts = line[2:].strip().split()
                identifier = parts[0]
                weight = None
                
                if len(parts) > 1:
                    try:
                        weight = float(parts[1])
                    except ValueError:
                        print(f"Varování: Neplatné ohodnocení uzlu na řádku {line_num}")
                
                graph.add_node(identifier, weight)
            
            elif line.startswith('h '):
                # Parsování hrany: h uzel1 (<|-|>) uzel2 [ohodnocení][:označení]
                rest = line[2:].strip()
                
                # Najít směr hrany
                direction = None
                if ' > ' in rest:
                    direction = '>'
                    parts = rest.split(' > ', 1)
                elif ' < ' in rest:
                    direction = '<'
                    parts = rest.split(' < ', 1)
                elif ' - ' in rest:
                    direction = '-'
                    parts = rest.split(' - ', 1)
                else:
                    print(f"Chyba: Neplatný formát hrany na řádku {line_num}")
                    continue
                
                node1 = parts[0].strip()
                rest_parts = parts[1].strip().split()
                node2 = rest_parts[0].strip()
                
                weight = None
                label = None
                
                # Parsovat zbývající části (váha a označení)
                if len(rest_parts) > 1:
                    for part in rest_parts[1:]:
                        if part.startswith(':'):
                            label = part[1:]
                        else:
                            try:
                                weight = float(part)
                            except ValueError:
                                print(f"Varování: Neplatné ohodnocení hrany na řádku {line_num}")
                
                # Přidat hranu podle směru
                if direction == '>':
                    graph.add_edge(node1, node2, weight, label, directed=True)
                elif direction == '<':
                    graph.add_edge(node2, node1, weight, label, directed=True)
                else:  # direction == '-'
                    graph.add_edge(node1, node2, weight, label, directed=False)
        
        except Exception as e:
            print(f"Chyba při parsování řádku {line_num}: {e}")
            continue
    
    return graph


def main():
    """Hlavní funkce programu"""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          ANALYZÁTOR VLASTNOSTÍ GRAFŮ A MATIC                       ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    if len(sys.argv) < 2:
        # Interaktivní vstup
        print("\nDostupné testovací soubory:")
        print("  1. test_graph.txt - Orientovaný graf ze zadání")
        print("  2. test_complete_graph.txt - Úplný graf K₄")
        print("  3. test_bipartite_graph.txt - Bipartitní graf K₃,₃")
        print("  4. test_regular_graph.txt - Regulární graf (cyklus)")
        print("  5. test_multigraph.txt - Multigraf se smyčkami")
        print("  6. test_dag.txt - Acyklický orientovaný graf")
        print("  7. test_binary_tree.txt - Binární strom")
        print()
        
        filename = input("📂 Zadejte cestu k souboru s grafem (nebo stiskněte Enter pro test_graph.txt): ").strip()
        
        if not filename:
            filename = "../graphs/test_graph.txt"
            print(f"   → Použiji výchozí soubor: {filename}")
    else:
        filename = sys.argv[1]
    
    print(f"\n📂 Načítám soubor: {filename}")
    graph = parse_graph_file(filename)
    
    print(f"✓ Graf úspěšně načten!\n")
    
    # Vypsat kompletní analýzu
    graph.print_statistics()


def create_test_file():
    """Vytvoří testovací soubor s grafem"""
    test_content = """# Testovací graf
u A;
u B;
h A > B 1 :h1;
u C;
h B > C 1 :h2;
u D;
h A > D 2 :h3;
u E;
h A < E 2 :h4;
h B < E 3 :h5;
h C > E 3 :h6;
h D > E 4 :h8;
u F;
h C > F 4 :h7;
h E > F 5 :h9;
u G;
h D < G 5 :h10;
h E > G 6 :h11;
u H;
h H > E 6 :h12;
h F > H 7 :h13;
h G < H 7 :h14;
"""
    
    with open("../graphs/test_graph.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✓ Vytvořen testovací soubor: test_graph.txt")


if __name__ == '__main__':
    main()
