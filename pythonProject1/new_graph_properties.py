#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analýza vlastností grafů
"""

import re
from typing import Dict, List, Set, Tuple, Optional


class Node:
    """Třída pro uzel grafu"""
    def __init__(self, identifier: str, weight: Optional[float] = None):
        self.identifier = identifier
        self.weight = weight
    
    def __str__(self):
        return self.identifier


class Edge:
    """Třída pro hranu grafu"""
    def __init__(self, from_node: str, to_node: str, directed: bool, 
                 weight: Optional[float] = None, label: Optional[str] = None):
        self.from_node = from_node
        self.to_node = to_node
        self.directed = directed
        self.weight = weight
        self.label = label
    
    def __str__(self):
        direction = ">" if self.directed else "-"
        weight_str = f" {self.weight}" if self.weight is not None else ""
        label_str = f" :{self.label}" if self.label else ""
        return f"{self.from_node} {direction} {self.to_node}{weight_str}{label_str}"


class Graph:
    """Třída pro graf"""
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
    
    def add_node(self, identifier: str, weight: Optional[float] = None):
        """Přidá uzel do grafu"""
        self.nodes[identifier] = Node(identifier, weight)
    
    def add_edge(self, from_node: str, to_node: str, directed: bool,
                 weight: Optional[float] = None, label: Optional[str] = None):
        """Přidá hranu do grafu"""
        self.edges.append(Edge(from_node, to_node, directed, weight, label))


def parse_graph_file(filename: str) -> Graph:
    """Načte graf ze souboru"""
    graph = Graph()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Soubor '{filename}' nebyl nalezen")
    except Exception as e:
        raise Exception(f"Chyba při čtení souboru: {e}")
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        try:
            # Parsování uzlu: u identifikátor [ohodnocení];
            if line.startswith('u '):
                match = re.match(r'u\s+([^;]+);', line)
                if not match:
                    raise ValueError(f"Neplatný formát uzlu na řádku {line_num}")
                
                parts = match.group(1).strip().split()
                identifier = parts[0]
                weight = None
                
                if len(parts) > 1:
                    try:
                        weight = float(parts[1])
                    except ValueError:
                        raise ValueError(f"Neplatné ohodnocení uzlu na řádku {line_num}")
                
                graph.add_node(identifier, weight)
            
            # Parsování hrany: h uzel1 (<|-|>) uzel2 [ohodnocení] [:označení];
            elif line.startswith('h '):
                match = re.match(r'h\s+([^\s]+)\s+([<>\-])\s+([^\s]+)(?:\s+([^\s:]+))?(?:\s*:\s*([^;]+))?;', line)
                if not match:
                    raise ValueError(f"Neplatný formát hrany na řádku {line_num}")
                
                from_node = match.group(1)
                direction = match.group(2)
                to_node = match.group(3)
                weight_str = match.group(4)
                label = match.group(5)
                
                # Kontrola existence uzlů
                if from_node not in graph.nodes:
                    raise ValueError(f"Uzel '{from_node}' neexistuje na řádku {line_num}")
                if to_node not in graph.nodes:
                    raise ValueError(f"Uzel '{to_node}' neexistuje na řádku {line_num}")
                
                # Určení směru
                directed = direction in ['<', '>']
                
                # Parsování váhy
                weight = None
                if weight_str:
                    try:
                        weight = float(weight_str)
                    except ValueError:
                        raise ValueError(f"Neplatná váha hrany na řádku {line_num}")
                
                graph.add_edge(from_node, to_node, directed, weight, label)
            
            else:
                raise ValueError(f"Neplatný řádek na {line_num}: {line}")
        
        except Exception as e:
            raise Exception(f"Chyba na řádku {line_num}: {e}")
    
    return graph


def analyze_graph_properties(graph: Graph):
    """Analyzuje vlastnosti grafu (a-j)"""
    print(f"\n📊 ZÁKLADNÍ INFORMACE:")
    print(f"  Počet uzlů (|V|): {len(graph.nodes)}")
    print(f"  Počet hran (|E|): {len(graph.edges)}")
    print(f"  Seznam uzlů: {sorted(graph.nodes.keys())}")
    
    print(f"\n" + "="*80)
    print("ROZHODNĚTE O NÁSLEDUJÍCÍCH VLASTNOSTECH:")
    print("="*80)
    
    # a) Ohodnocený
    has_node_weights = any(node.weight is not None for node in graph.nodes.values())
    has_edge_weights = any(edge.weight is not None for edge in graph.edges)
    
    print(f"\na) OHODNOCENÝ (vážený):")
    if has_node_weights or has_edge_weights:
        print(f"   ✓ ANO - Graf je ohodnocený")
        if has_node_weights:
            print(f"     → Uzly mají ohodnocení")
        if has_edge_weights:
            print(f"     → Hrany mají váhy")
    else:
        print(f"   ✗ NE - Graf není ohodnocený (žádné váhy)")
    
    # b) Orientovaný
    print(f"\nb) ORIENTOVANÝ (směrovaný):")
    directed_edges = [e for e in graph.edges if e.directed]
    undirected_edges = [e for e in graph.edges if not e.directed]
    
    if len(directed_edges) == len(graph.edges):
        print(f"   ✓ ANO - Orientovaný graf (všechny hrany mají směr)")
    elif len(undirected_edges) == len(graph.edges):
        print(f"   ✗ NE - Neorientovaný graf (všechny hrany bez směru)")
    else:
        print(f"   ⚠ ČÁSTEČNĚ - Smíšený graf (obsahuje orientované i neorientované hrany)")
    
    # c) Souvislý
    print(f"\nc) SOUVISLÝ (spojitý):")
    is_connected = check_connected(graph)
    if is_connected:
        print(f"   ✓ ANO - Graf je souvislý")
        print(f"     → Existuje cesta mezi každými dvěma uzly")
    else:
        print(f"   ✗ NE - Graf není souvislý")
        isolated = get_isolated_nodes(graph)
        if isolated:
            print(f"     → Izolované uzly: {isolated}")
    
    # d) Prostý
    print(f"\nd) PROSTÝ (bez násobných hran):")
    has_multiple = has_multiple_edges(graph)
    if not has_multiple:
        print(f"   ✓ ANO - Prostý graf (bez násobných hran)")
        print(f"     → Mezi každými dvěma uzly max. 1 hrana")
    else:
        print(f"   ✗ NE - Multigraf (obsahuje násobné hrany)")
    
    # e) Jednoduchý
    print(f"\ne) JEDNODUCHÝ (bez smyček a násobných hran):")
    loops = get_loops(graph)
    if not has_multiple and not loops:
        print(f"   ✓ ANO - Jednoduchý graf")
        print(f"     → Bez smyček a násobných hran")
    else:
        print(f"   ✗ NE - Není jednoduchý graf")
        if loops:
            print(f"     → Obsahuje {len(loops)} smyček")
        if has_multiple:
            print(f"     → Obsahuje násobné hrany")
    
    # f) Rovinný
    print(f"\nf) ROVINNÝ (planární):")
    print(f"   ? NELZE AUTOMATICKY URČIT")
    print(f"     → Rovinnost je NP-úplný problém")
    print(f"     → Pro malé grafy: zkuste nakreslit bez křížení hran")
    if len(graph.nodes) <= 4:
        print(f"     → Graf s max 4 uzly je vždy rovinný")
    
    # g) Konečný
    print(f"\ng) KONEČNÝ:")
    print(f"   ✓ ANO - Graf je konečný")
    print(f"     → Má konečný počet uzlů ({len(graph.nodes)}) a hran ({len(graph.edges)})")
    
    # h) Úplný
    print(f"\nh) ÚPLNÝ (kompletní, K_n):")
    is_complete = check_complete(graph)
    if is_complete:
        print(f"   ✓ ANO - Úplný graf")
        print(f"     → Každý uzel je spojen se všemi ostatními")
        if len(undirected_edges) == len(graph.edges):
            expected = len(graph.nodes) * (len(graph.nodes) - 1) // 2
            print(f"     → Pro {len(graph.nodes)} uzlů: {expected} hran (K_{len(graph.nodes)})")
    else:
        print(f"   ✗ NE - Není úplný graf")
    
    # i) Regulární
    print(f"\ni) REGULÁRNÍ (pravidelný):")
    regularity = check_regular(graph)
    if regularity is not None:
        print(f"   ✓ ANO - Regulární graf stupně {regularity}")
        print(f"     → Všechny uzly mají stupeň {regularity}")
    else:
        print(f"   ✗ NE - Není regulární graf")
        degrees = [get_degree(graph, node) for node in graph.nodes]
        print(f"     → Stupně uzlů: min={min(degrees)}, max={max(degrees)}")
    
    # j) Bipartitní
    print(f"\nj) BIPARTITNÍ (2-barevný):")
    is_bip, partition = check_bipartite(graph)
    if is_bip:
        print(f"   ✓ ANO - Bipartitní graf")
        if partition:
            set1, set2 = partition
            print(f"     → Partice 1 ({len(set1)} uzlů): {sorted(set1)}")
            print(f"     → Partice 2 ({len(set2)} uzlů): {sorted(set2)}")
    else:
        print(f"   ✗ NE - Není bipartitní graf")
        print(f"     → Nelze rozdělit do dvou množin bez hran uvnitř")
    
    # k) Acyklický
    print(f"\nk) ACYKLICKÝ (bez cyklů):")
    is_acyclic = check_acyclic(graph)
    if is_acyclic:
        print(f"   ✓ ANO - Acyklický graf")
        print(f"     → Neobsahuje žádné cykly")
    else:
        print(f"   ✗ NE - Obsahuje cykly")
        cycles = find_cycles(graph)
        if cycles:
            print(f"     → Nalezeno {len(cycles)} cyklů")
    
    # l) Strom
    print(f"\nl) STROM (souvislý acyklický):")
    is_tree = check_tree(graph)
    if is_tree:
        print(f"   ✓ ANO - Strom")
        print(f"     → Souvislý a acyklický graf")
        print(f"     → n uzlů, n-1 hran")
    else:
        print(f"   ✗ NE - Není strom")
        if not check_connected(graph):
            print(f"     → Není souvislý")
        if not is_acyclic:
            print(f"     → Obsahuje cykly")
    
    # m) Les
    print(f"\nm) LES (sjednocení stromů):")
    is_forest = check_forest(graph)
    if is_forest:
        print(f"   ✓ ANO - Les")
        print(f"     → Acyklický graf (sjednocení stromů)")
        components = get_connected_components(graph)
        print(f"     → Obsahuje {len(components)} komponent")
    else:
        print(f"   ✗ NE - Není les")
        print(f"     → Obsahuje cykly")
    
    # Interaktivní analýza uzlů
    print(f"\n" + "="*80)
    print("ANALÝZA KONKRÉTNÍCH UZLŮ")
    print("="*80)
    
    while True:
        print(f"\n📋 Dostupné uzly: {sorted(graph.nodes.keys())}")
        print(f"\nVyberte uzel pro analýzu (nebo 'konec' pro ukončení):")
        node = input("📍 Uzel: ").strip()
        
        if node.lower() in ['konec', 'exit', 'q', '']:
            break
        
        if node not in graph.nodes:
            print(f"❌ Uzel '{node}' neexistuje!")
            continue
        
        analyze_single_node(graph, node)


def analyze_single_node(graph: Graph, node: str):
    """Analyzuje konkrétní uzel"""
    print(f"\n{'='*60}")
    print(f"ANALÝZA UZLU: {node}")
    print(f"{'='*60}")
    
    # a) Následníci uzlu
    successors = get_successors(graph, node)
    print(f"\na) NÁSLEDNÍCI uzlu {node}:")
    if successors:
        print(f"   ✓ {successors}")
        print(f"     → Uzly, do kterých vede hrana Z uzlu {node}")
    else:
        print(f"   ✗ Žádní následníci")
        print(f"     → Z uzlu {node} nevede žádná hrana")
    
    # b) Předchůdci uzlu
    predecessors = get_predecessors(graph, node)
    print(f"\nb) PŘEDCHŮDCI uzlu {node}:")
    if predecessors:
        print(f"   ✓ {predecessors}")
        print(f"     → Uzly, ze kterých vede hrana DO uzlu {node}")
    else:
        print(f"   ✗ Žádní předchůdci")
        print(f"     → Do uzlu {node} nevede žádná hrana")
    
    # c) Sousedé uzlu
    neighbors = get_neighbors(graph, node)
    print(f"\nc) SOUSEDÉ uzlu {node}:")
    if neighbors:
        print(f"   ✓ {neighbors}")
        print(f"     → Všechny uzly spojené hranou s uzlem {node}")
    else:
        print(f"   ✗ Žádní sousedé")
        print(f"     → Uzel {node} je izolovaný")
    
    # d) Výstupní okolí uzlu
    out_neighborhood = get_out_neighborhood(graph, node)
    print(f"\nd) VÝSTUPNÍ OKOLÍ uzlu {node}:")
    if out_neighborhood:
        print(f"   ✓ {out_neighborhood}")
        print(f"     → Množina všech následníků uzlu {node}")
    else:
        print(f"   ✗ Prázdné výstupní okolí")
        print(f"     → Z uzlu {node} nevede žádná hrana")
    
    # e) Vstupní okolí uzlu
    in_neighborhood = get_in_neighborhood(graph, node)
    print(f"\ne) VSTUPNÍ OKOLÍ uzlu {node}:")
    if in_neighborhood:
        print(f"   ✓ {in_neighborhood}")
        print(f"     → Množina všech předchůdců uzlu {node}")
    else:
        print(f"   ✗ Prázdné vstupní okolí")
        print(f"     → Do uzlu {node} nevede žádná hrana")
    
    # f) Okolí uzlu (sjednocení vstupního a výstupního)
    all_neighborhood = get_all_neighborhood(graph, node)
    print(f"\nf) OKOLÍ uzlu {node} (všichni sousedé):")
    if all_neighborhood:
        print(f"   ✓ {all_neighborhood}")
        print(f"     → Sjednocení vstupního a výstupního okolí")
    else:
        print(f"   ✗ Prázdné okolí")
        print(f"     → Uzel {node} je izolovaný")
    
    # g) Výstupní stupeň uzlu
    out_degree = get_out_degree(graph, node)
    print(f"\ng) VÝSTUPNÍ STUPEŇ uzlu {node}:")
    print(f"   ✓ {out_degree}")
    print(f"     → Počet hran vycházejících z uzlu {node}")
    
    # h) Vstupní stupeň uzlu
    in_degree = get_in_degree(graph, node)
    print(f"\nh) VSTUPNÍ STUPEŇ uzlu {node}:")
    print(f"   ✓ {in_degree}")
    print(f"     → Počet hran vstupujících do uzlu {node}")
    
    # i) Celkový stupeň uzlu
    total_degree = get_total_degree(graph, node)
    print(f"\ni) CELKOVÝ STUPEŇ uzlu {node}:")
    print(f"   ✓ {total_degree}")
    print(f"     → Součet vstupního a výstupního stupně")
    
    # Dodatečné informace
    print(f"\n📊 DODATEČNÉ INFORMACE:")
    print(f"   • Vstupní stupeň: {in_degree}")
    print(f"   • Výstupní stupeň: {out_degree}")
    print(f"   • Celkový stupeň: {total_degree}")
    print(f"   • Počet sousedů: {len(neighbors)}")
    
    if in_degree == 0 and out_degree > 0:
        print(f"   • Typ uzlu: ZDROJ (source)")
    elif out_degree == 0 and in_degree > 0:
        print(f"   • Typ uzlu: STOK (sink)")
    elif in_degree == 0 and out_degree == 0:
        print(f"   • Typ uzlu: IZOLOVANÝ")
    else:
        print(f"   • Typ uzlu: OBECNÝ")


def get_successors(graph: Graph, node: str) -> List[str]:
    """Vrátí seznam následníků uzlu"""
    successors = []
    for edge in graph.edges:
        if edge.from_node == node:
            successors.append(edge.to_node)
    return sorted(list(set(successors)))


def get_predecessors(graph: Graph, node: str) -> List[str]:
    """Vrátí seznam předchůdců uzlu"""
    predecessors = []
    for edge in graph.edges:
        if edge.to_node == node:
            predecessors.append(edge.from_node)
    return sorted(list(set(predecessors)))


def get_neighbors(graph: Graph, node: str) -> List[str]:
    """Vrátí seznam všech sousedů uzlu"""
    neighbors = set()
    for edge in graph.edges:
        if edge.from_node == node:
            neighbors.add(edge.to_node)
        elif edge.to_node == node:
            neighbors.add(edge.from_node)
    return sorted(list(neighbors))


def get_out_neighborhood(graph: Graph, node: str) -> List[str]:
    """Vrátí výstupní okolí uzlu (následníci)"""
    return get_successors(graph, node)


def get_in_neighborhood(graph: Graph, node: str) -> List[str]:
    """Vrátí vstupní okolí uzlu (předchůdci)"""
    return get_predecessors(graph, node)


def get_all_neighborhood(graph: Graph, node: str) -> List[str]:
    """Vrátí okolí uzlu (všichni sousedé)"""
    return get_neighbors(graph, node)


def get_out_degree(graph: Graph, node: str) -> int:
    """Vrátí výstupní stupeň uzlu"""
    count = 0
    for edge in graph.edges:
        if edge.from_node == node:
            count += 1
    return count


def get_in_degree(graph: Graph, node: str) -> int:
    """Vrátí vstupní stupeň uzlu"""
    count = 0
    for edge in graph.edges:
        if edge.to_node == node:
            count += 1
    return count


def get_total_degree(graph: Graph, node: str) -> int:
    """Vrátí celkový stupeň uzlu"""
    return get_in_degree(graph, node) + get_out_degree(graph, node)


def check_connected(graph: Graph) -> bool:
    """Zkontroluje, zda je graf souvislý"""
    if not graph.nodes:
        return True
    
    # BFS pro neorientovaný graf
    start_node = list(graph.nodes.keys())[0]
    visited = set()
    queue = [start_node]
    
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        
        # Najít všechny sousední uzly
        for edge in graph.edges:
            if edge.from_node == node and edge.to_node not in visited:
                queue.append(edge.to_node)
            elif edge.to_node == node and edge.from_node not in visited:
                queue.append(edge.from_node)
    
    return len(visited) == len(graph.nodes)


def get_isolated_nodes(graph: Graph) -> List[str]:
    """Vrátí seznam izolovaných uzlů"""
    isolated = []
    for node in graph.nodes:
        has_edges = any(edge.from_node == node or edge.to_node == node for edge in graph.edges)
        if not has_edges:
            isolated.append(node)
    return isolated


def has_multiple_edges(graph: Graph) -> bool:
    """Zkontroluje, zda má graf násobné hrany"""
    edge_pairs = set()
    for edge in graph.edges:
        # Normalizovat hranu pro neorientované grafy
        if not edge.directed:
            pair = tuple(sorted([edge.from_node, edge.to_node]))
        else:
            pair = (edge.from_node, edge.to_node)
        
        if pair in edge_pairs:
            return True
        edge_pairs.add(pair)
    
    return False


def get_loops(graph: Graph) -> List[Edge]:
    """Vrátí seznam smyček"""
    loops = []
    for edge in graph.edges:
        if edge.from_node == edge.to_node:
            loops.append(edge)
    return loops


def check_complete(graph: Graph) -> bool:
    """Zkontroluje, zda je graf úplný"""
    if len(graph.nodes) <= 1:
        return True
    
    # Pro neorientovaný graf
    undirected_edges = [e for e in graph.edges if not e.directed]
    if len(undirected_edges) == len(graph.edges):
        expected_edges = len(graph.nodes) * (len(graph.nodes) - 1) // 2
        return len(undirected_edges) == expected_edges
    
    # Pro orientovaný graf
    directed_edges = [e for e in graph.edges if e.directed]
    if len(directed_edges) == len(graph.edges):
        expected_edges = len(graph.nodes) * (len(graph.nodes) - 1)
        return len(directed_edges) == expected_edges
    
    return False


def get_degree(graph: Graph, node: str) -> int:
    """Vrátí stupeň uzlu"""
    degree = 0
    for edge in graph.edges:
        if edge.from_node == node or edge.to_node == node:
            degree += 1
    return degree


def is_directed(graph: Graph) -> bool:
    """Zkontroluje, zda je graf orientovaný"""
    for edge in graph.edges:
        if edge.directed:
            return True
    return False


def check_regular(graph: Graph) -> Optional[int]:
    """Zkontroluje, zda je graf regulární"""
    if not graph.nodes:
        return None
    
    # Pro orientované grafy: zkontrolovat vstupní a výstupní stupně
    if is_directed(graph):
        in_degrees = [get_in_degree(graph, node) for node in graph.nodes]
        out_degrees = [get_out_degree(graph, node) for node in graph.nodes]
        
        # Všechny uzly musí mít stejný vstupní i výstupní stupeň
        if (all(d == in_degrees[0] for d in in_degrees) and 
            all(d == out_degrees[0] for d in out_degrees)):
            return in_degrees[0]  # Vrátí stupeň
        return None
    else:
        # Pro neorientované grafy: celkový stupeň
        degrees = [get_degree(graph, node) for node in graph.nodes]
        if all(d == degrees[0] for d in degrees):
            return degrees[0]
        return None


def check_bipartite(graph: Graph) -> Tuple[bool, Optional[Tuple[Set[str], Set[str]]]]:
    """Zkontroluje, zda je graf bipartitní"""
    if not graph.nodes:
        return True, (set(), set())
    
    # BFS s barvením
    colors = {}
    queue = []
    
    # Začít s prvním uzlem
    start_node = list(graph.nodes.keys())[0]
    colors[start_node] = 0
    queue.append(start_node)
    
    while queue:
        node = queue.pop(0)
        current_color = colors[node]
        
        # Najít sousední uzly
        for edge in graph.edges:
            neighbor = None
            if edge.from_node == node:
                neighbor = edge.to_node
            elif edge.to_node == node:
                neighbor = edge.from_node
            
            if neighbor is not None:
                if neighbor not in colors:
                    colors[neighbor] = 1 - current_color
                    queue.append(neighbor)
                elif colors[neighbor] == current_color:
                    return False, None
    
    # Rozdělit do dvou množin podle barev
    set1 = {node for node, color in colors.items() if color == 0}
    set2 = {node for node, color in colors.items() if color == 1}
    
    return True, (set1, set2)




def check_acyclic(graph: Graph) -> bool:
    """Zkontroluje, zda je graf acyklický (neobsahuje cykly)"""
    if not graph.nodes:
        return True
    
    # DFS pro detekci cyklů
    visited = set()
    rec_stack = set()
    
    def has_cycle_dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        # Najít všechny sousední uzly
        for edge in graph.edges:
            neighbor = None
            if edge.from_node == node:
                neighbor = edge.to_node
            elif edge.to_node == node:
                neighbor = edge.from_node
            
            if neighbor is not None:
                if neighbor not in visited:
                    if has_cycle_dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
        
        rec_stack.remove(node)
        return False
    
    # Zkontrolovat všechny komponenty
    for node in graph.nodes:
        if node not in visited:
            if has_cycle_dfs(node):
                return False
    
    return True


def find_cycles(graph: Graph) -> List[List[str]]:
    """Najde všechny cykly v grafu"""
    cycles = []
    if not graph.nodes:
        return cycles
    
    visited = set()
    rec_stack = set()
    path = []
    
    def find_cycles_dfs(node, parent):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        # Najít všechny sousední uzly
        for edge in graph.edges:
            neighbor = None
            if edge.from_node == node:
                neighbor = edge.to_node
            elif edge.to_node == node:
                neighbor = edge.from_node
            
            if neighbor is not None and neighbor != parent:
                if neighbor not in visited:
                    find_cycles_dfs(neighbor, node)
                elif neighbor in rec_stack:
                    # Našli jsme cyklus
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
        
        rec_stack.remove(node)
        path.pop()
    
    # Zkontrolovat všechny komponenty
    for node in graph.nodes:
        if node not in visited:
            find_cycles_dfs(node, None)
    
    return cycles


def check_tree(graph: Graph) -> bool:
    """Zkontroluje, zda je graf strom"""
    if not graph.nodes:
        return True
    
    # Strom je souvislý a acyklický
    return check_connected(graph) and check_acyclic(graph)


def check_forest(graph: Graph) -> bool:
    """Zkontroluje, zda je graf les (sjednocení stromů)"""
    if not graph.nodes:
        return True
    
    # Les je acyklický (nemusí být souvislý)
    return check_acyclic(graph)


def get_connected_components(graph: Graph) -> List[Set[str]]:
    """Vrátí seznam souvislých komponent"""
    if not graph.nodes:
        return []
    
    visited = set()
    components = []
    
    def dfs_component(node, component):
        visited.add(node)
        component.add(node)
        
        # Najít všechny sousední uzly
        for edge in graph.edges:
            neighbor = None
            if edge.from_node == node:
                neighbor = edge.to_node
            elif edge.to_node == node:
                neighbor = edge.from_node
            
            if neighbor is not None and neighbor not in visited:
                dfs_component(neighbor, component)
    
    for node in graph.nodes:
        if node not in visited:
            component = set()
            dfs_component(node, component)
            components.append(component)
    
    return components
