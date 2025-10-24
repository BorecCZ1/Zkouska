#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analýza matic a jejich vlastností
"""

import sys
from typing import Dict, List, Set, Tuple, Optional


def analyze_matrix_properties(graph):
    """Analyzuje matice grafu"""
    print(f"\n📊 ZÁKLADNÍ INFORMACE:")
    print(f"  Počet uzlů: {len(graph.nodes)}")
    print(f"  Počet hran: {len(graph.edges)}")
    print(f"  Uzly: {sorted(graph.nodes.keys())}")
    
    # Interaktivní menu pro matice
    while True:
        print(f"\n" + "="*80)
        print("VOLBY PRO MATICE:")
        print("  1. Matice sousednosti")
        print("  2. Znaménková matice")
        print("  3. Mocniny matice sousednosti")
        print("  4. Matice incidence")
        print("  5. Matice délek")
        print("  6. Matice předchůdců")
        print("  7. Tabulka incidentních hran")
        print("  8. Seznam sousedů")
        print("  9. Seznam uzlů a hran")
        print("  10. Všechny matice")
        print("  11. Konec")
        print("="*80)
        
        choice = input("\n🎯 Volba: ").strip()
        
        if choice == "11" or choice.lower() in ["konec", "exit", "q"]:
            break
        
        elif choice == "1":
            print_matrix_section("MATICE SOUSEDNOSTI", lambda: get_adjacency_matrix(graph))
        
        elif choice == "2":
            print_matrix_section("ZNAMÉNKOVÁ MATICE", lambda: get_signed_matrix(graph))
        
        elif choice == "3":
            print_power_matrices(graph)
        
        elif choice == "4":
            print_matrix_section("MATICE INCIDENCE", lambda: get_incidence_matrix(graph))
        
        elif choice == "5":
            print_matrix_section("MATICE DÉLEK", lambda: get_distance_matrix(graph))
        
        elif choice == "6":
            print_matrix_section("MATICE PŘEDCHŮDCŮ", lambda: get_predecessor_matrix(graph))
        
        elif choice == "7":
            print_edge_list_table(graph)
        
        elif choice == "8":
            print_adjacency_list(graph)
        
        elif choice == "9":
            print_node_edge_list(graph)
        
        elif choice == "10":
            print_all_matrices(graph)
        
        else:
            print(f"❌ Neznámá volba '{choice}'")


def print_matrix_section(title: str, matrix_func):
    """Vytiskne sekci s maticí"""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")
    
    try:
        matrix = matrix_func()
        if matrix is None:
            print("❌ Matice nelze vytvořit pro tento typ grafu")
            return
        
        # Zkontrolovat velikost
        if len(matrix) > 20 or (matrix and len(matrix[0]) > 20):
            print(f"ℹ️  Matice je příliš velká na vypsání ({len(matrix)}×{len(matrix[0]) if matrix else 0})")
            print(f"   (Zobrazují se pouze matice o velikosti max 20×20)")
            print_matrix_info(matrix)
        else:
            print_matrix(matrix)
            print_matrix_info(matrix)
        
        # Nabídnout vyhledávání hodnot
        offer_value_search(matrix)
        
        # Nabídnout počítání hodnot
        offer_value_count(matrix)
    
    except Exception as e:
        print(f"❌ Chyba při vytváření matice: {e}")


def print_matrix(matrix: List[List]):
    """Vytiskne matici"""
    if not matrix:
        print("(Matice je prázdná)")
        return
    
    n = len(matrix)
    m = len(matrix[0]) if matrix else 0
    
    # Hlavička
    print("     " + "".join(f"{i:>6}" for i in range(m)))
    print("─" * (6 * m + 5))
    
    # Řádky
    for i, row in enumerate(matrix):
        row_str = "".join(f"{val:>6.1f}" if isinstance(val, float) and val != float('inf') else f"{val:>6}" for val in row)
        print(f"{i:>3} │{row_str}")


def print_matrix_info(matrix: List[List]):
    """Vytiskne informace o matici"""
    if not matrix:
        return
    
    n = len(matrix)
    m = len(matrix[0]) if matrix else 0
    
    print(f"\n📊 INFORMACE O MATICI:")
    print(f"  Rozměr: {n} × {m}")
    print(f"  Celkem prvků: {n * m}")
    
    # Statistiky
    all_values = []
    for row in matrix:
        for val in row:
            if val != float('inf'):
                all_values.append(val)
    
    if all_values:
        print(f"  Minimální hodnota: {min(all_values)}")
        print(f"  Maximální hodnota: {max(all_values)}")
        
        # Počty hodnot
        from collections import Counter
        value_counts = Counter(all_values)
        print(f"  Počty hodnot:")
        for val, count in sorted(value_counts.items()):
            if val == 0:
                print(f"    Nuly (0): {count}")
            elif val == 1:
                print(f"    Jedničky (1): {count}")
            else:
                print(f"    Hodnota {val}: {count}")


def offer_value_search(matrix: List[List]):
    """Nabídne vyhledávání hodnot v matici"""
    if not matrix:
        return
    
    # Zkontrolovat, zda má matice zajímavé hodnoty
    all_values = []
    for row in matrix:
        for val in row:
            if val != float('inf'):
                all_values.append(val)
    
    if not all_values:
        return
    
    # Najít všechny dostupné hodnoty
    from collections import Counter
    value_counts = Counter(all_values)
    all_unique_values = sorted(set(all_values))
    
    if not all_unique_values:
        return
    
    print(f"\n🔍 VYHLEDÁVÁNÍ HODNOT V MATICI:")
    print(f"   Dostupné hodnoty: {all_unique_values}")
    
    while True:
        try:
            search_input = input(f"\nZadejte hodnotu k vyhledání (nebo 'konec'): ").strip()
            
            if search_input.lower() in ['konec', 'exit', 'q', '']:
                break
            
            # Zkusit převést na číslo
            try:
                search_value = float(search_input) if '.' in search_input else int(search_input)
            except ValueError:
                print("❌ Zadejte platné číslo")
                continue
            
            # Vyhledat hodnotu
            results = find_value_in_matrix(matrix, search_value)
            
            if results:
                print(f"\n✅ Nalezeno {len(results)} výskytů hodnoty {search_value}:")
                
                # Omezit výpis pro velké matice
                max_show = 20
                for i, (row, col, val) in enumerate(results[:max_show], 1):
                    print(f"   {i:>2}. [{row}][{col}] = {val}")
                
                if len(results) > max_show:
                    print(f"   ... a dalších {len(results) - max_show} výskytů")
                
                # Statistiky
                print(f"\n📊 STATISTIKY:")
                print(f"   • Celkem výskytů: {len(results)}")
                print(f"   • V řádcích: {len(set(r[0] for r in results))}")
                print(f"   • Ve sloupcích: {len(set(r[1] for r in results))}")
                
            else:
                print(f"❌ Hodnota {search_value} se v matici nevyskytuje")
                print(f"   Dostupné hodnoty: {sorted(set(all_values))}")
        
        except KeyboardInterrupt:
            break


def find_value_in_matrix(matrix: List[List], search_value) -> List[Tuple[int, int, any]]:
    """Vyhledá všechny výskyty hodnoty v matici"""
    results = []
    
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            # Porovnání s tolerancí pro float
            if isinstance(val, float) and isinstance(search_value, (int, float)):
                if abs(val - float(search_value)) < 1e-10:
                    results.append((i, j, val))
            elif val == search_value:
                results.append((i, j, val))
    
    return results


def offer_value_count(matrix: List[List]):
    """Nabídne počítání hodnot v matici"""
    if not matrix:
        return
    
    # Zkontrolovat, zda má matice nějaké hodnoty
    all_values = []
    for row in matrix:
        for val in row:
            if val != float('inf'):
                all_values.append(val)
    
    if not all_values:
        return
    
    print(f"\n🔢 POČÍTÁNÍ HODNOT V MATICI:")
    
    while True:
        try:
            count_input = input(f"\nChcete spočítat nějakou hodnotu? (ano/ne): ").strip().lower()
            
            if count_input in ['ne', 'n', 'konec', 'exit', 'q', '']:
                break
            elif count_input not in ['ano', 'a', 'yes', 'y']:
                print("❌ Zadejte 'ano' nebo 'ne'")
                continue
            
            # Zeptat se na hodnotu
            value_input = input(f"Zadejte hodnotu k spočítání: ").strip()
            
            try:
                search_value = float(value_input) if '.' in value_input else int(value_input)
            except ValueError:
                print("❌ Zadejte platné číslo")
                continue
            
            # Spočítat hodnotu
            count = count_value_in_matrix(matrix, search_value)
            
            print(f"\n📊 VÝSLEDEK:")
            print(f"   Hodnota {search_value} se v matici vyskytuje {count}×")
            
            # Dodatečné statistiky
            if count > 0:
                percentage = (count / len(all_values)) * 100
                print(f"   To je {percentage:.1f}% všech hodnot v matici")
                
                # Najít pozice pro malé matice
                if len(matrix) <= 10 and len(matrix[0]) <= 10:
                    positions = find_value_in_matrix(matrix, search_value)
                    if positions:
                        print(f"   Pozice: {[f'[{r}][{c}]' for r, c, _ in positions[:10]]}")
                        if len(positions) > 10:
                            print(f"   ... a dalších {len(positions) - 10} pozic")
            else:
                print(f"   Dostupné hodnoty: {sorted(set(all_values))}")
        
        except KeyboardInterrupt:
            break


def count_value_in_matrix(matrix: List[List], search_value) -> int:
    """Spočítá výskyty hodnoty v matici"""
    count = 0
    
    for row in matrix:
        for val in row:
            # Porovnání s tolerancí pro float
            if isinstance(val, float) and isinstance(search_value, (int, float)):
                if abs(val - float(search_value)) < 1e-10:
                    count += 1
            elif val == search_value:
                count += 1
    
    return count


def get_adjacency_matrix(graph) -> List[List[int]]:
    """Vytvoří matici sousednosti"""
    nodes = sorted(graph.nodes.keys())
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    
    for edge in graph.edges:
        i = nodes.index(edge.from_node)
        j = nodes.index(edge.to_node)
        
        if edge.directed:
            matrix[i][j] += 1
        else:
            matrix[i][j] += 1
            matrix[j][i] += 1
    
    return matrix


def get_signed_matrix(graph) -> List[List[int]]:
    """Vytvoří znaménkovou matici (pouze pro orientované grafy)"""
    if not any(edge.directed for edge in graph.edges):
        return None  # Pouze pro orientované grafy
    
    nodes = sorted(graph.nodes.keys())
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    
    for edge in graph.edges:
        if edge.directed:
            i = nodes.index(edge.from_node)
            j = nodes.index(edge.to_node)
            matrix[i][j] = 1
            matrix[j][i] = -1
    
    return matrix


def print_power_matrices(graph):
    """Vytiskne mocniny matice sousednosti"""
    print(f"\n{'='*80}")
    print("MOCNINY MATICE SOUSEDNOSTI")
    print(f"{'='*80}")
    
    adj_matrix = get_adjacency_matrix(graph)
    if not adj_matrix:
        print("❌ Nelze vytvořit matici sousednosti")
        return
    
    # Zeptat se na mocninu
    while True:
        try:
            power = input(f"\nZadejte mocninu (1-10, nebo 'konec'): ").strip()
            
            if power.lower() in ['konec', 'exit', 'q', '']:
                break
            
            power = int(power)
            if power < 1 or power > 10:
                print("❌ Mocnina musí být mezi 1 a 10")
                continue
            
            # Vypočítat a zobrazit
            print(f"\n📊 A^{power} ({power}. mocnina matice sousednosti):")
            result_matrix = matrix_power(adj_matrix, power)
            print_matrix_section(f"A^{power}", lambda: result_matrix)
            
        except ValueError:
            print("❌ Zadejte platné číslo")
        except KeyboardInterrupt:
            break


def matrix_power(matrix: List[List], power: int) -> List[List]:
    """Vypočítá mocninu matice"""
    if power == 1:
        return matrix
    
    result = matrix
    for _ in range(power - 1):
        result = matrix_multiply(result, matrix)
    
    return result


def matrix_multiply(a: List[List], b: List[List]) -> List[List]:
    """Vynásobí dvě matice"""
    n = len(a)
    m = len(b[0]) if b else 0
    k = len(a[0]) if a else 0
    
    result = [[0] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            for l in range(k):
                result[i][j] += a[i][l] * b[l][j]
    
    return result


def get_incidence_matrix(graph) -> List[List[int]]:
    """Vytvoří matici incidence"""
    nodes = sorted(graph.nodes.keys())
    edges = graph.edges
    n = len(nodes)
    m = len(edges)
    
    matrix = [[0] * m for _ in range(n)]
    
    for j, edge in enumerate(edges):
        i_from = nodes.index(edge.from_node)
        i_to = nodes.index(edge.to_node)
        
        if edge.directed:
            matrix[i_from][j] = 1
            matrix[i_to][j] = -1
        else:
            matrix[i_from][j] = 1
            matrix[i_to][j] = 1
    
    return matrix


def get_distance_matrix(graph) -> List[List[float]]:
    """Vytvoří matici délek (Floyd-Warshall)"""
    nodes = sorted(graph.nodes.keys())
    n = len(nodes)
    
    # Inicializace
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    
    # Přidat hrany
    for edge in graph.edges:
        i = nodes.index(edge.from_node)
        j = nodes.index(edge.to_node)
        weight = edge.weight if edge.weight is not None else 1.0
        
        if edge.directed:
            dist[i][j] = weight
        else:
            dist[i][j] = weight
            dist[j][i] = weight
    
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


def get_predecessor_matrix(graph) -> List[List[int]]:
    """Vytvoří matici předchůdců"""
    nodes = sorted(graph.nodes.keys())
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    
    for edge in graph.edges:
        if edge.directed:
            i = nodes.index(edge.from_node)
            j = nodes.index(edge.to_node)
            matrix[j][i] = 1  # j má předchůdce i
    
    return matrix


def print_edge_list_table(graph):
    """Vytiskne tabulku incidentních hran"""
    print(f"\n{'='*80}")
    print("TABULKA INCIDENTNÍCH HRAN")
    print(f"{'='*80}")
    
    print(f"Celkem hran: {len(graph.edges)}")
    print(f"{'ID':>4} {'Z uzlu':>15} {'Typ':>4} {'Do uzlu':>15} {'Váha':>10} {'Označení':>20}")
    print("─" * 100)
    
    for i, edge in enumerate(graph.edges, 1):
        weight_str = str(edge.weight) if edge.weight is not None else '-'
        label_str = edge.label if edge.label else '-'
        direction = "→" if edge.directed else "—"
        print(f"{i:>4} {edge.from_node:>15} {direction:>4} {edge.to_node:>15} {weight_str:>10} {label_str:>20}")


def print_adjacency_list(graph):
    """Vytiskne seznam sousedů"""
    print(f"\n{'='*80}")
    print("SEZNAM SOUSEDŮ (Dynamický seznam sousedů)")
    print(f"{'='*80}")
    
    nodes = sorted(graph.nodes.keys())
    
    for node in nodes:
        neighbors = []
        for edge in graph.edges:
            if edge.from_node == node:
                neighbors.append(edge.to_node)
            elif edge.to_node == node:
                neighbors.append(edge.from_node)
        
        neighbors = sorted(list(set(neighbors)))
        print(f"{node}: {neighbors if neighbors else '(žádní sousedé)'}")


def print_node_edge_list(graph):
    """Vytiskne seznam uzlů a hran"""
    print(f"\n{'='*80}")
    print("SEZNAM UZLŮ A HRAN")
    print(f"{'='*80}")
    
    print(f"\n📋 UZLY ({len(graph.nodes)}):")
    for node_name in sorted(graph.nodes.keys()):
        node_obj = graph.nodes[node_name]
        weight_str = f" (váha: {node_obj.weight})" if node_obj.weight is not None else ""
        print(f"  • {node_name}{weight_str}")
    
    print(f"\n🔗 HRANY ({len(graph.edges)}):")
    for i, edge in enumerate(graph.edges, 1):
        weight_str = f" (váha: {edge.weight})" if edge.weight is not None else ""
        label_str = f" [{edge.label}]" if edge.label else ""
        direction = "→" if edge.directed else "—"
        print(f"  {i:>2}. {edge.from_node} {direction} {edge.to_node}{weight_str}{label_str}")


def print_all_matrices(graph):
    """Vytiskne všechny matice"""
    print(f"\n{'='*80}")
    print("VŠECHNY MATICE GRAFU")
    print(f"{'='*80}")
    
    # 1. Matice sousednosti
    print_matrix_section("1. MATICE SOUSEDNOSTI", lambda: get_adjacency_matrix(graph))
    
    # 2. Znaménková matice
    print_matrix_section("2. ZNAMÉNKOVÁ MATICE", lambda: get_signed_matrix(graph))
    
    # 3. Matice incidence
    print_matrix_section("3. MATICE INCIDENCE", lambda: get_incidence_matrix(graph))
    
    # 4. Matice délek
    print_matrix_section("4. MATICE DÉLEK", lambda: get_distance_matrix(graph))
    
    # 5. Matice předchůdců
    print_matrix_section("5. MATICE PŘEDCHŮDCŮ", lambda: get_predecessor_matrix(graph))
    
    # 6. Tabulka incidentních hran
    print_edge_list_table(graph)
    
    # 7. Seznam sousedů
    print_adjacency_list(graph)
    
    # 8. Seznam uzlů a hran
    print_node_edge_list(graph)
