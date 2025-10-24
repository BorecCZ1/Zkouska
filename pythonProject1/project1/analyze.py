#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kombinovaný analyzátor grafů a matic
"""

import sys
import main
import matrix_analyzer


def main_combined():
    """Hlavní funkce pro komplexní analýzu"""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║       KOMPLEXNÍ ANALYZÁTOR GRAFŮ A MATIC                           ║")
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
        
        print("\nRežim analýzy:")
        print("  1. --graph  - pouze analýza vlastností grafu")
        print("  2. --matrix - pouze analýza matic")
        print("  3. --all    - komplexní analýza (grafy + matice)")
        print()
        
        mode_input = input("Vyberte režim (1/2/3 nebo stiskněte Enter pro --graph): ").strip()
        
        if mode_input == "1" or mode_input == "":
            mode = "--graph"
        elif mode_input == "2":
            mode = "--matrix"
        elif mode_input == "3":
            mode = "--all"
        else:
            mode = mode_input if mode_input.startswith("--") else "--graph"
        
        print(f"   → Režim: {mode}")
    else:
        filename = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "--graph"
    
    print(f"\n📂 Načítám soubor: {filename}")
    graph = main.parse_graph_file(filename)
    print(f"✓ Graf úspěšně načten!\n")
    
    if mode == "--graph" or mode == "--all":
        graph.print_statistics()
    
    if mode == "--matrix" or mode == "--all":
        analyzer = matrix_analyzer.MatrixAnalyzer(graph)
        analyzer.analyze_all()
    
    print("\n✅ Analýza dokončena!")


if __name__ == '__main__':
    main_combined()

