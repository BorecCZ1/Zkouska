#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hlavní skript pro analýzu grafů
"""

import sys
import os
from pathlib import Path
import new_graph_properties
import new_matrix_properties


def list_test_files():
    """Vypíše dostupné testovací soubory"""
    test_files = []
    
    # Soubory v kořeni
    for file in ['graph_test.txt', 'test_graph.txt', 'test_complete_graph.txt', 'test_bipartite_graph.txt']:
        if os.path.exists(file):
            test_files.append(file)
    
    # Soubory v graphs/
    if os.path.exists('graphs'):
        for file in sorted(os.listdir('graphs')):
            if file.endswith('.txt') or file.endswith('.tg'):
                test_files.append(os.path.join('graphs', file))
    
    return test_files


def get_graph_file():
    """Interaktivně načte cestu k souboru s grafem"""
    test_files = list_test_files()
    
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                    ANALÝZA GRAFŮ A MATIC                          ║")
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
    print("  - nebo stiskněte Enter pro graph_test.txt")
    print()
    
    user_input = input("📂 Cesta: ").strip()
    
    if not user_input:
        return "graph_test.txt"
    
    # Zkusit interpretovat jako číslo
    try:
        idx = int(user_input) - 1
        if 0 <= idx < len(test_files):
            return test_files[idx]
    except ValueError:
        pass
    
    # Použít přímo zadanou cestu
    return user_input


def main():
    """Hlavní program"""
    # Získat soubor grafu
    filename = get_graph_file()
    
    print(f"\n📂 Načítám soubor: {filename}")
    
    # Načíst graf
    try:
        graph = new_graph_properties.parse_graph_file(filename)
    except Exception as e:
        print(f"❌ Chyba při načítání: {e}")
        sys.exit(1)
    
    print(f"✓ Graf úspěšně načten! ({len(graph.nodes)} uzlů, {len(graph.edges)} hran)")
    
    # Interaktivní menu
    while True:
        print("\n" + "=" * 80)
        print("VOLBY:")
        print("  1. Vlastnosti grafu (a-j)")
        print("  2. Matice a statistiky")
        print("  3. Vybrat nový graf")
        print("  4. Konec")
        print("=" * 80)
        
        choice = input("\n🎯 Volba: ").strip()
        
        if choice == "4" or choice.lower() in ["exit", "konec", "q"]:
            print("\n👋 Nashledanou!")
            break
        
        elif choice == "3":
            filename = get_graph_file()
            print(f"\n📂 Načítám soubor: {filename}")
            try:
                graph = new_graph_properties.parse_graph_file(filename)
                print(f"✓ Graf úspěšně načten! ({len(graph.nodes)} uzlů, {len(graph.edges)} hran)")
            except Exception as e:
                print(f"❌ Chyba při načítání: {e}")
        
        elif choice == "1":
            print("\n" + "=" * 80)
            print("ANALÝZA VLASTNOSTÍ GRAFU")
            print("=" * 80)
            new_graph_properties.analyze_graph_properties(graph)
        
        elif choice == "2":
            print("\n" + "=" * 80)
            print("ANALÝZA MATIC")
            print("=" * 80)
            new_matrix_properties.analyze_matrix_properties(graph)
        
        else:
            print(f"❌ Neznámá volba '{choice}'")


if __name__ == "__main__":
    main()
