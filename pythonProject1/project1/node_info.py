#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interaktivní nástroj pro zobrazení detailních informací o uzlu
"""

import sys
import os
from pathlib import Path
import main as graph_module
import matrix_analyzer as analyzer_module


def list_test_files():
    """Vypíše dostupné testovací soubory"""
    test_files = []
    
    # Soubory v kořeni
    for file in ['test_graph.txt', 'test_complete_graph.txt', 'test_bipartite_graph.txt']:
        if os.path.exists(file):
            test_files.append(file)
    
    # Soubory v grafs/
    if os.path.exists('../graphs'):
        for file in sorted(os.listdir('../graphs')):
            if file.endswith('.txt'):
                test_files.append(os.path.join('../graphs', file))
    
    return test_files


def get_graph_file():
    """Interaktivně načte cestu k souboru s grafem"""
    test_files = list_test_files()
    
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          INTERAKTIVNÍ INFORMACE O UZLECH GRAFU                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    if test_files:
        print("📂 Dostupné testovací soubory:")
        for i, file in enumerate(test_files, 1):
            print(f"  {i}. {file}")
        print()
    
    print("Zadejte cestu k souboru s grafem:")
    print("  - zadejte číslo pro výběr testovacího souboru")
    print("  - nebo přímo cestu k souboru")
    print("  - nebo stiskněte Enter pro test_complete_graph.txt")
    print()
    
    user_input = input("📂 Cesta: ").strip()
    
    if not user_input:
        return "test_complete_graph.txt"
    
    # Zkusit interpretovat jako číslo
    try:
        idx = int(user_input) - 1
        if 0 <= idx < len(test_files):
            return test_files[idx]
    except ValueError:
        pass
    
    # Použít přímo zadanou cestu
    return user_input


def select_node(graph):
    """Interaktivně vybere uzel"""
    nodes = sorted(graph.nodes.keys())
    
    print(f"\n📋 Dostupné uzly ({len(nodes)}):")
    
    # Ukázat jen prvních 20, pak zkrátit
    nodes_to_show = nodes[:20]
    for i, node in enumerate(nodes_to_show, 1):
        print(f"  {i}. {node}")
    
    if len(nodes) > 20:
        print(f"  ... a dalších {len(nodes) - 20} uzlů")
    
    print()
    print("Vyberte uzel:")
    print("  - zadejte číslo pro výběr z seznamu")
    print("  - nebo zadejte jméno uzlu přímo")
    print()
    
    user_input = input("📍 Uzel: ").strip()
    
    if not user_input:
        return nodes[0]
    
    # Zkusit interpretovat jako číslo
    try:
        idx = int(user_input) - 1
        if 0 <= idx < len(nodes):
            return nodes[idx]
    except ValueError:
        pass
    
    # Zkusit přímé jméno
    if user_input in nodes:
        return user_input
    
    # Fuzzy match - hledá podobné názvy
    matches = [n for n in nodes if user_input.lower() in n.lower()]
    if matches:
        print(f"⚠️  Uzel '{user_input}' nenalezen, ale našel jsem podobné:")
        for match in matches[:5]:
            print(f"  - {match}")
        if len(matches) > 5:
            print(f"  ... a dalších {len(matches) - 5}")
    else:
        print(f"❌ Uzel '{user_input}' nenalezen!")
    
    return None


def main():
    """Hlavní program"""
    # Získat soubor grafu
    filename = get_graph_file()
    
    print(f"\n📂 Načítám soubor: {filename}")
    
    # Načíst graf
    try:
        graph = graph_module.parse_graph_file(filename)
    except Exception as e:
        print(f"❌ Chyba při načítání: {e}")
        sys.exit(1)
    
    print(f"✓ Graf úspěšně načten! ({len(graph.nodes)} uzlů, {len(graph.edges)} hran)")
    
    # Vytvořit analyzátor
    analyzer = analyzer_module.MatrixAnalyzer(graph)
    
    # Interaktivní smyčka
    while True:
        print("\n" + "=" * 80)
        print("VOLBY:")
        print("  1. Zobrazit info o uzlu")
        print("  2. Vybrat nový graf")
        print("  3. Konec")
        print("=" * 80)
        
        choice = input("\n🎯 Volba: ").strip()
        
        if choice == "3" or choice.lower() in ["exit", "konec", "q"]:
            print("\n👋 Nashledanou!")
            break
        
        elif choice == "2":
            filename = get_graph_file()
            print(f"\n📂 Načítám soubor: {filename}")
            try:
                graph = graph_module.parse_graph_file(filename)
                analyzer = analyzer_module.MatrixAnalyzer(graph)
                print(f"✓ Graf úspěšně načten! ({len(graph.nodes)} uzlů, {len(graph.edges)} hran)")
            except Exception as e:
                print(f"❌ Chyba při načítání: {e}")
        
        elif choice == "1":
            node = select_node(graph)
            if node:
                analyzer.print_node_characteristics(node)
        
        else:
            print(f"❌ Neznámá volba '{choice}'")


if __name__ == "__main__":
    main()
