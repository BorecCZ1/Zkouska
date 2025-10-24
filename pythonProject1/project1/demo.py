#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstrační skript - ukázka všech funkcí analyzátoru grafů
"""

import main
import matrix_analyzer
import advanced_algorithms


def print_separator(title=""):
    """Vypíše oddělovač"""
    if title:
        print(f"\n{'='*70}")
        print(f"{title:^70}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}\n")


def demo_basic_analysis():
    """Demonstrace základní analýzy grafů"""
    print_separator("DEMO 1: ZÁKLADNÍ ANALÝZA GRAFŮ")
    
    print("📊 Analyzuji úplný graf K₄...")
    graph = main.parse_graph_file("../graphs/test_complete_graph.txt")
    
    print(f"\nTyp grafu: {'Orientovaný' if graph.is_oriented() else 'Neorientovaný'}")
    print(f"Prostý graf: {'✓' if not graph.has_multiple_edges() else '✗'}")
    print(f"Jednoduchý graf: {'✓' if graph.is_simple() else '✗'}")
    print(f"Souvislý graf: {'✓' if graph.is_connected() else '✗'}")
    print(f"Úplný graf: {'✓' if graph.is_complete() else '✗'}")
    
    regularity = graph.is_regular()
    if regularity is not None:
        print(f"Regulární graf: ✓ (stupeň {regularity})")
    else:
        print(f"Regulární graf: ✗")
    
    is_bip, partition = graph.is_bipartite()
    if is_bip:
        print(f"Bipartitní graf: ✓")
    else:
        print(f"Bipartitní graf: ✗")


def demo_bipartite():
    """Demonstrace bipartitního grafu"""
    print_separator("DEMO 2: BIPARTITNÍ GRAF K₃,₃")
    
    print("📊 Analyzuji bipartitní graf...")
    graph = main.parse_graph_file("../graphs/test_bipartite_graph.txt")
    
    is_bip, partition = graph.is_bipartite()
    if is_bip and partition:
        set1, set2 = partition
        print(f"\n✓ Graf je bipartitní!")
        print(f"   Partition 1: {sorted(set1)}")
        print(f"   Partition 2: {sorted(set2)}")
        print(f"\nKaždý uzel z partition 1 je spojen se všemi uzly z partition 2")
        
        # Ukázka stupňů
        print(f"\nStupně uzlů:")
        for node in sorted(graph.nodes.keys()):
            degree = graph.get_degree(node)
            print(f"  {node}: {degree}")


def demo_matrices():
    """Demonstrace matic"""
    print_separator("DEMO 3: MATICE GRAFŮ")
    
    print("📐 Vytvářím matice pro kompletní graf K₄...")
    graph = main.parse_graph_file("../graphs/test_complete_graph.txt")
    analyzer = matrix_analyzer.MatrixAnalyzer(graph)
    
    # Matice sousednosti
    adj = analyzer.get_adjacency_matrix()
    print("\nMatice sousednosti:")
    analyzer.print_matrix(adj, "", is_float=False)
    
    # Matice stupňů
    deg = analyzer.get_degree_matrix()
    print("Matice stupňů:")
    analyzer.print_matrix(deg, "", is_float=False)
    
    # Vlastnosti
    print("Vlastnosti grafu z matic:")
    dist = analyzer.get_distance_matrix()
    max_dist = max(max(row) for row in dist if max(row) != float('inf'))
    print(f"  Maximální vzdálenost (průměr): {max_dist}")


def demo_cycles():
    """Demonstrace detekce cyklů"""
    print_separator("DEMO 4: DETEKCE CYKLŮ")
    
    # DAG
    print("📋 Testování acyklického grafu (DAG)...")
    graph_dag = main.parse_graph_file("../graphs/test_dag.txt")
    analyzer_dag = advanced_algorithms.AdvancedAnalyzer(graph_dag)
    
    has_cycle, cycle = analyzer_dag.has_cycle_directed()
    if has_cycle:
        print(f"  ✗ Graf obsahuje cyklus: {' → '.join(cycle)}")
    else:
        print(f"  ✓ Graf je acyklický (DAG)")
        
        # Topologické řazení
        topo = analyzer_dag.topological_sort()
        if topo:
            print(f"  Topologické řazení: {' → '.join(topo)}")
    
    # Graf s cyklem
    print("\n📋 Testování grafu s cyklem...")
    graph_cycle = main.parse_graph_file("../graphs/test_graph.txt")
    analyzer_cycle = advanced_algorithms.AdvancedAnalyzer(graph_cycle)
    
    has_cycle, cycle = analyzer_cycle.has_cycle_directed()
    if has_cycle:
        print(f"  ✓ Graf obsahuje cyklus: {' → '.join(cycle)}")
    else:
        print(f"  ✗ Graf je acyklický")


def demo_shortest_paths():
    """Demonstrace nejkratších cest"""
    print_separator("DEMO 5: NEJKRATŠÍ CESTY (DIJKSTRA)")
    
    print("🚀 Hledám nejkratší cesty v orientovaném grafu...")
    graph = main.parse_graph_file("../graphs/test_graph.txt")
    analyzer = advanced_algorithms.AdvancedAnalyzer(graph)
    
    start_node = 'A'
    distances = analyzer.dijkstra(start_node)
    
    print(f"\nNejkratší cesty z uzlu '{start_node}':")
    for node in sorted(graph.nodes.keys()):
        if node != start_node:
            dist = distances[node]
            if dist == float('inf'):
                print(f"  → {node:8s}: nedosažitelný")
            else:
                print(f"  → {node:8s}: {dist:6.1f}")


def demo_strongly_connected():
    """Demonstrace silně souvislých komponent"""
    print_separator("DEMO 6: SILNĚ SOUVISLÉ KOMPONENTY")
    
    print("🔗 Hledám silně souvislé komponenty...")
    graph = main.parse_graph_file("../graphs/test_graph.txt")
    analyzer = advanced_algorithms.AdvancedAnalyzer(graph)
    
    sccs = analyzer.find_strongly_connected_components()
    
    print(f"\nPočet silně souvislých komponent: {len(sccs)}")
    for i, scc in enumerate(sccs, 1):
        print(f"  {i}. {sorted(scc)}")
    
    if len(sccs) == 1:
        print("\n✓ Graf je silně souvislý (jedna komponenta obsahuje všechny uzly)")


def demo_multigraph():
    """Demonstrace multigrafu"""
    print_separator("DEMO 7: MULTIGRAF SE SMYČKAMI")
    
    print("📊 Analyzuji multigraf...")
    graph = main.parse_graph_file("../graphs/test_multigraph.txt")
    
    # Smyčky
    loops = graph.get_loops()
    if loops:
        print(f"\n✓ Graf obsahuje {len(loops)} smyček:")
        for loop in loops:
            print(f"  • {loop.from_node} → {loop.from_node}")
    
    # Násobné hrany
    if graph.has_multiple_edges():
        print(f"\n✓ Graf obsahuje násobné hrany (multigraf)")
    
    # Typ grafu
    if graph.is_oriented() and not graph.is_unoriented():
        if any(not edge.directed for edge in graph.edges):
            print(f"✓ Smíšený graf (obsahuje orientované i neorientované hrany)")
        else:
            print(f"✓ Orientovaný graf")


def demo_all():
    """Spustí všechny demonstrace"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  KOMPLETNÍ DEMONSTRACE ANALYZÁTORU GRAFŮ A MATIC".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        demo_basic_analysis()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_bipartite()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_matrices()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_cycles()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_shortest_paths()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_strongly_connected()
        input("\n[Stiskněte Enter pro pokračování...]")
        
        demo_multigraph()
        
        print_separator("KONEC DEMONSTRACE")
        print("✅ Všechny funkce byly úspěšně předvedeny!")
        print("\nPro detailní analýzu použijte:")
        print("  • python3 main.py <soubor>")
        print("  • python3 matrix_analyzer.py <soubor>")
        print("  • python3 advanced_algorithms.py <soubor>")
        print("  • python3 analyze.py <soubor> --all")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstrace přerušena uživatelem")
    except Exception as e:
        print(f"\n\n❌ Chyba během demonstrace: {e}")


if __name__ == '__main__':
    demo_all()

