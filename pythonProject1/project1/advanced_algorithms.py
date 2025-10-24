#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pokročilé algoritmy pro analýzu grafů
- Detekce cyklů
- Topologické řazení
- Silně souvislé komponenty
- Nejkratší cesty
- Minimální kostra
"""

import sys
from collections import defaultdict, deque
from typing import List, Set, Dict, Optional, Tuple
import main as graph_module


class AdvancedAnalyzer:
    """Pokročilá analýza grafů"""
    
    def __init__(self, graph: graph_module.Graph):
        self.graph = graph
        self.nodes_list = sorted(graph.nodes.keys())
    
    def has_cycle_directed(self) -> Tuple[bool, List[str]]:
        """
        Detekuje cyklus v orientovaném grafu pomocí DFS.
        Vrací (má_cyklus, cyklus_pokud_existuje)
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self.graph.nodes}
        parent = {node: None for node in self.graph.nodes}
        cycle = []
        
        def dfs(node):
            nonlocal cycle
            color[node] = GRAY
            
            for neighbor in self.graph.adjacency_list.get(node, []):
                if color[neighbor] == GRAY:
                    # Našli jsme zpětnou hranu - cyklus
                    cycle.append(neighbor)
                    current = node
                    while current != neighbor:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(neighbor)
                    cycle.reverse()
                    return True
                elif color[neighbor] == WHITE:
                    parent[neighbor] = node
                    if dfs(neighbor):
                        return True
            
            color[node] = BLACK
            return False
        
        for node in self.graph.nodes:
            if color[node] == WHITE:
                if dfs(node):
                    return True, cycle
        
        return False, []
    
    def has_cycle_undirected(self) -> Tuple[bool, List[str]]:
        """
        Detekuje cyklus v neorientovaném grafu pomocí DFS.
        """
        visited = set()
        parent = {}
        cycle = []
        
        def dfs(node, par):
            nonlocal cycle
            visited.add(node)
            parent[node] = par
            
            neighbors = self.graph.undirected_adjacency.get(node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != par:
                    # Našli jsme cyklus
                    cycle.append(neighbor)
                    current = node
                    while current != neighbor:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(neighbor)
                    cycle.reverse()
                    return True
            return False
        
        for node in self.graph.nodes:
            if node not in visited:
                if dfs(node, None):
                    return True, cycle
        
        return False, []
    
    def topological_sort(self) -> Optional[List[str]]:
        """
        Topologické řazení (pouze pro acyklické orientované grafy).
        Vrací None, pokud graf obsahuje cyklus.
        """
        # Nejdřív zkontrolujeme, zda graf obsahuje cyklus
        has_cycle, _ = self.has_cycle_directed()
        if has_cycle:
            return None
        
        # Kahn's algoritmus
        in_degree = {node: self.graph.get_in_degree(node) for node in self.graph.nodes}
        queue = deque([node for node in self.graph.nodes if in_degree[node] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.graph.adjacency_list.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.graph.nodes):
            return None  # Graf obsahuje cyklus
        
        return result
    
    def find_strongly_connected_components(self) -> List[Set[str]]:
        """
        Najde silně souvislé komponenty v orientovaném grafu (Tarjanův algoritmus).
        """
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = defaultdict(bool)
        sccs = []
        
        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            on_stack[node] = True
            stack.append(node)
            
            for neighbor in self.graph.adjacency_list.get(node, []):
                if neighbor not in index:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], index[neighbor])
            
            if lowlinks[node] == index[node]:
                component = set()
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.add(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for node in self.graph.nodes:
            if node not in index:
                strongconnect(node)
        
        return sccs
    
    def find_bridges(self) -> List[Tuple[str, str]]:
        """
        Najde mosty (hrany, jejichž odebrání zvýší počet komponent).
        """
        visited = set()
        disc = {}
        low = {}
        parent = {}
        bridges = []
        time = [0]
        
        def dfs_bridge(u):
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1
            
            # Pro neorientované hrany
            for v in self.graph.undirected_adjacency.get(u, []):
                if v not in visited:
                    parent[v] = u
                    dfs_bridge(v)
                    low[u] = min(low[u], low[v])
                    
                    if low[v] > disc[u]:
                        bridges.append((u, v))
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
        
        for node in self.graph.nodes:
            if node not in visited:
                parent[node] = None
                dfs_bridge(node)
        
        return bridges
    
    def find_articulation_points(self) -> Set[str]:
        """
        Najde artikulační body (uzly, jejichž odebrání zvýší počet komponent).
        """
        visited = set()
        disc = {}
        low = {}
        parent = {}
        ap = set()
        time = [0]
        
        def dfs_ap(u):
            children = 0
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1
            
            for v in self.graph.get_all_neighbors(u):
                if v not in visited:
                    children += 1
                    parent[v] = u
                    dfs_ap(v)
                    low[u] = min(low[u], low[v])
                    
                    if parent.get(u) is None and children > 1:
                        ap.add(u)
                    
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        ap.add(u)
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
        
        for node in self.graph.nodes:
            if node not in visited:
                parent[node] = None
                dfs_ap(node)
        
        return ap
    
    def dijkstra(self, start: str) -> Dict[str, float]:
        """
        Dijkstrův algoritmus pro nejkratší cesty z jednoho uzlu.
        """
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[start] = 0
        unvisited = set(self.graph.nodes.keys())
        
        while unvisited:
            # Najdi uzel s minimální vzdáleností
            current = min(unvisited, key=lambda node: distances[node])
            
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            
            # Pro orientované hrany
            for edge in self.graph.edges:
                if edge.from_node == current and edge.to_node in unvisited:
                    weight = edge.weight if edge.weight is not None else 1.0
                    new_dist = distances[current] + weight
                    if new_dist < distances[edge.to_node]:
                        distances[edge.to_node] = new_dist
                
                # Pro neorientované hrany
                if not edge.directed:
                    if edge.to_node == current and edge.from_node in unvisited:
                        weight = edge.weight if edge.weight is not None else 1.0
                        new_dist = distances[current] + weight
                        if new_dist < distances[edge.from_node]:
                            distances[edge.from_node] = new_dist
        
        return distances
    
    def bellman_ford(self, start: str) -> Tuple[Dict[str, float], bool]:
        """
        Bellman-Fordův algoritmus (podporuje záporné váhy).
        Vrací (vzdálenosti, má_záporný_cyklus)
        """
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[start] = 0
        
        # Relaxace hran |V|-1 krát
        for _ in range(len(self.graph.nodes) - 1):
            for edge in self.graph.edges:
                weight = edge.weight if edge.weight is not None else 1.0
                
                if edge.directed:
                    if distances[edge.from_node] + weight < distances[edge.to_node]:
                        distances[edge.to_node] = distances[edge.from_node] + weight
                else:
                    if distances[edge.from_node] + weight < distances[edge.to_node]:
                        distances[edge.to_node] = distances[edge.from_node] + weight
                    if distances[edge.to_node] + weight < distances[edge.from_node]:
                        distances[edge.from_node] = distances[edge.to_node] + weight
        
        # Kontrola záporných cyklů
        for edge in self.graph.edges:
            weight = edge.weight if edge.weight is not None else 1.0
            if edge.directed:
                if distances[edge.from_node] + weight < distances[edge.to_node]:
                    return distances, True
            else:
                if distances[edge.from_node] + weight < distances[edge.to_node]:
                    return distances, True
                if distances[edge.to_node] + weight < distances[edge.from_node]:
                    return distances, True
        
        return distances, False
    
    def kruskal_mst(self) -> Tuple[List[graph_module.Edge], float]:
        """
        Kruskalův algoritmus pro minimální kostru (pouze neorientované grafy).
        Vrací (seznam_hran, celková_váha)
        """
        # Union-Find struktura
        parent = {node: node for node in self.graph.nodes}
        rank = {node: 0 for node in self.graph.nodes}
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            
            if root1 != root2:
                if rank[root1] < rank[root2]:
                    parent[root1] = root2
                elif rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root2] = root1
                    rank[root1] += 1
                return True
            return False
        
        # Seřadit hrany podle váhy
        edges = [edge for edge in self.graph.edges if not edge.directed]
        edges.sort(key=lambda e: e.weight if e.weight is not None else 1.0)
        
        mst = []
        total_weight = 0
        
        for edge in edges:
            if union(edge.from_node, edge.to_node):
                mst.append(edge)
                total_weight += edge.weight if edge.weight is not None else 1.0
                
                if len(mst) == len(self.graph.nodes) - 1:
                    break
        
        return mst, total_weight
    
    def analyze_all(self):
        """Provede kompletní pokročilou analýzu"""
        print("\n" + "=" * 70)
        print("POKROČILÁ ANALÝZA GRAFU")
        print("=" * 70)
        
        # Detekce cyklů
        print("\n🔄 DETEKCE CYKLŮ:")
        print("─" * 70)
        
        if self.graph.is_oriented():
            has_cycle, cycle = self.has_cycle_directed()
            if has_cycle:
                print(f"  ✓ Graf obsahuje cyklus: {' → '.join(cycle)}")
            else:
                print(f"  ✗ Graf neobsahuje cyklus (je acyklický)")
        else:
            has_cycle, cycle = self.has_cycle_undirected()
            if has_cycle:
                print(f"  ✓ Graf obsahuje cyklus: {' — '.join(cycle)}")
            else:
                print(f"  ✗ Graf neobsahuje cyklus (je acyklický)")
        
        # Topologické řazení
        if self.graph.is_oriented():
            print("\n📋 TOPOLOGICKÉ ŘAZENÍ:")
            print("─" * 70)
            topo_sort = self.topological_sort()
            if topo_sort:
                print(f"  ✓ {' → '.join(topo_sort)}")
            else:
                print(f"  ✗ Topologické řazení neexistuje (graf obsahuje cyklus)")
        
        # Silně souvislé komponenty
        if self.graph.is_oriented():
            print("\n🔗 SILNĚ SOUVISLÉ KOMPONENTY:")
            print("─" * 70)
            sccs = self.find_strongly_connected_components()
            for i, scc in enumerate(sccs, 1):
                print(f"  {i}. {sorted(scc)}")
        
        # Mosty
        if not self.graph.is_oriented() and not self.graph.is_discrete():
            print("\n🌉 MOSTY (kritické hrany):")
            print("─" * 70)
            bridges = self.find_bridges()
            if bridges:
                for u, v in bridges:
                    print(f"  • {u} — {v}")
            else:
                print(f"  ✗ Graf neobsahuje mosty")
        
        # Artikulační body
        if not self.graph.is_discrete():
            print("\n🎯 ARTIKULAČNÍ BODY (kritické uzly):")
            print("─" * 70)
            ap = self.find_articulation_points()
            if ap:
                for node in sorted(ap):
                    print(f"  • {node}")
            else:
                print(f"  ✗ Graf neobsahuje artikulační body")
        
        # Dijkstrův algoritmus
        if len(self.graph.nodes) > 0 and len(self.graph.edges) > 0:
            print("\n🚀 NEJKRATŠÍ CESTY (Dijkstra):")
            print("─" * 70)
            start_node = self.nodes_list[0]
            print(f"  Z uzlu '{start_node}':")
            distances = self.dijkstra(start_node)
            for node in sorted(self.graph.nodes.keys()):
                if node != start_node:
                    dist = distances[node]
                    if dist == float('inf'):
                        print(f"    → {node}: nedosažitelný")
                    else:
                        print(f"    → {node}: {dist}")
        
        # Minimální kostra
        has_undirected = any(not edge.directed for edge in self.graph.edges)
        if has_undirected and self.graph.is_connected():
            print("\n🌲 MINIMÁLNÍ KOSTRA (Kruskal):")
            print("─" * 70)
            mst, total_weight = self.kruskal_mst()
            print(f"  Celková váha: {total_weight}")
            print(f"  Hrany:")
            for edge in mst:
                weight_str = f", váha={edge.weight}" if edge.weight else ""
                print(f"    • {edge.from_node} — {edge.to_node}{weight_str}")
        
        print("\n" + "=" * 70)


def main():
    """Hlavní funkce"""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           POKROČILÉ ALGORITMY PRO ANALÝZU GRAFŮ                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    if len(sys.argv) < 2:
        # Interaktivní vstup
        print("\nDostupné testovací soubory:")
        print("  1. test_graph.txt - Orientovaný graf ze zadání")
        print("  2. test_complete_graph.txt - Úplný graf K₄")
        print("  3. test_bipartite_graph.txt - Bipartitní graf K₃,₃")
        print("  4. test_regular_graph.txt - Regulární graf (cyklus)")
        print("  5. test_multigraph.txt - Multigraf se smyčkami")
        print("  6. test_dag.txt - Acyklický orientovaný graf (doporučeno)")
        print("  7. test_binary_tree.txt - Binární strom")
        print()
        
        filename = input("📂 Zadejte cestu k souboru s grafem (nebo stiskněte Enter pro test_dag.txt): ").strip()
        
        if not filename:
            filename = "../graphs/test_dag.txt"
            print(f"   → Použiji výchozí soubor: {filename}")
    else:
        filename = sys.argv[1]
    
    print(f"\n📂 Načítám soubor: {filename}")
    
    graph = graph_module.parse_graph_file(filename)
    print(f"✓ Graf úspěšně načten!\n")
    
    analyzer = AdvancedAnalyzer(graph)
    analyzer.analyze_all()


if __name__ == '__main__':
    main()

