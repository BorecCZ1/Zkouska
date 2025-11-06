import csv
import os

class MatrixAnalyzer:
    """
    - get_adjacency_matrix() -> (matrix, node_list)
        matrix: list[list[int]] velikost n x n, matrix[i][j] = počet hran z i do j
        node_list: seřazené ID uzlů (indexy řádků/sloupců)

    - get_incidence_matrix() -> (matrix, node_list, edge_list)
        matrix: list[list[int]] velikost n_nodes x n_edges, hodnoty 1/-1/2 podle orientace/smyčky
        edge_list: seznam hran odpovídajících sloupcům (unikátní podle (u,v,direction))

    - get_weight_matrix() -> (matrix, node_list)
        matrix: list[list[float]] velikost n x n; neexistující přímé spojení = float('inf'), diagonála = 0

    - get_adjacency_power(k) -> (matrix_k, node_list)
        matrix_k: počet cest délky k mezi dvojicemi uzlů (celá čísla)

    Formátování a export:
    - _print_matrix() zarovnává sloupce podle šířky obsahu
    - _format_cell() používá `self.float_precision` a `self.inf_symbol`
    - save_matrix_csv(...) uloží CSV (prázdná buňka = žádné přímé spojení)

    TODO k rozšíření a výkonu:
    - Pro velké grafy doporučuji vytvořit lokální mapu id->index (dict) a používat ji namísto node_list.index()
    - Pokud chcete dělat numeriku (A^k) pro velké grafy, zvažte numpy arrays pro výkon
    """

    def __init__(self, graph):
        """Inicializace analyzátoru.

        Args:
            graph (Graph): Graf k analýze
        """
        self.graph = graph
        # formatting options
        # float_precision: how many decimal places to show for floating values
        # inf_symbol: symbol used to render 'infinite' / no direct connection
        self.float_precision = 1  # number of decimals to show for floats
        self.inf_symbol = '∞'
    
    """
    Vrátí matici sousednosti grafu.
    
    Returns:
        tuple: (matrix, node_list) kde matrix je 2D seznam a node_list je seznam identifikátorů uzlů
    """
    def get_adjacency_matrix(self):
        # If there are no nodes, return empty structures
        # Returns: (matrix, node_list)
        #  - matrix: n x n list of ints (counts of edges between nodes)
        #  - node_list: sorted list of node identifiers (order of rows/cols)
        if not self.graph.nodes:
            return [], []
        
        node_list = sorted(self.graph.nodes.keys())
        n = len(node_list)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # Naivní implementace: pro každý pár (u,v) projít sousední hrany u a spočítat
        # počet hran vedoucích do v. To vrací multiplicitu hran mezi dvojicí uzlů.
        # Pozn.: pro velké grafy zvážit vytvoření id->index mapy a iteraci přes adj seznamy (optimalizace).
        for i, u_id in enumerate(node_list):
            for j, v_id in enumerate(node_list):
                # Count edges from u to v
                count = 0
                for edge in self.graph.adj[u_id]:
                    if edge.v.identifier == v_id:
                        if self.graph.is_directed:
                            # pouze explicitně orientované hrany '>' se počítají jako u->v
                            if edge.direction == '>':
                                count += 1
                        else:
                            # v neorientovaném grafu každá hrana mezi uzly zvyšuje hodnotu
                            count += 1
                matrix[i][j] = count
        
        return matrix, node_list
    
    """
    Vrátí matici incidence grafu.
    
    ---

    Returns: tuple: (matrix, node_list, edge_list)
    - matrix: n_nodes x n_edges, hodnoty v buňkách jsou 1 / -1 / 2
    Semantika:
        * 1  — uzel je zvolený "zdroj" hrany (tail)
        * -1 — uzel je zvolený "cíl" hrany (head)
        * 2  — smyčka (edge spojuje uzel se sebou samým; incidenčně se započítává dvakrát)
    Edge cases: prázdný graf nebo bez hran vrátí prázdné struktury
    """
    def get_incidence_matrix(self):
        if not self.graph.nodes or not self.graph.edges:
            return [], [], []

        node_list = sorted(self.graph.nodes.keys())
        edge_list = []

        # Create a list of unique edges (avoid duplicates for undirected)
        seen_edges = set()
        for edge in self.graph.edges:
            edge_key = (edge.u.identifier, edge.v.identifier, edge.direction)
            if edge_key not in seen_edges:
                edge_list.append(edge)
                seen_edges.add(edge_key)

        # Build zero matrix sized by nodes x edges
        n_nodes = len(node_list)
        n_edges = len(edge_list)
        matrix = [[0 for _ in range(n_edges)] for _ in range(n_nodes)]

        # Build a quick lookup map id->index to avoid repeated index() calls
        node_index = {nid: idx for idx, nid in enumerate(node_list)}

        for j, edge in enumerate(edge_list):
            # map node identifiers to row indices
            u_idx = node_index[edge.u.identifier]
            v_idx = node_index[edge.v.identifier]

            # Fill according to orientation
            if edge.direction == '>':
                matrix[u_idx][j] = 1   # Outgoing
                matrix[v_idx][j] = -1  # Incoming
            elif edge.direction == '<':
                matrix[u_idx][j] = -1  # Incoming
                matrix[v_idx][j] = 1   # Outgoing
            else:  # Undirected
                matrix[u_idx][j] = 1
                matrix[v_idx][j] = 1

            # Handle self-loops: represent as 2 in the corresponding column
            if edge.u == edge.v:
                matrix[u_idx][j] = 2

        return matrix, node_list, edge_list
    
    """
    Vrátí matici vah (vzdáleností) grafu.
    
    Returns:
        tuple: (matrix, node_list)
    """
    def get_weight_matrix(self):
        # Returns (matrix, node_list)
        # matrix uses float('inf') for missing direct connection, diagonal 0
        if not self.graph.nodes:
            return [], []
        
        node_list = sorted(self.graph.nodes.keys())
        n = len(node_list)
        # Initialize with infinity for no direct connection
        INF = float('inf')
        matrix = [[INF for _ in range(n)] for _ in range(n)]
        
        # Set diagonal to 0 (distance from node to itself)
        for i in range(n):
            matrix[i][i] = 0
        
        # Fill in direct edge weights
        # Note: if weight is None we use implicit weight = 1
        # If multiple edges exist, we keep the minimum weight between nodes
        for i, u_id in enumerate(node_list):
            for edge in self.graph.adj[u_id]:
                j = node_list.index(edge.v.identifier)
                weight = edge.weight if edge.weight is not None else 1
                if isinstance(weight, (int, float)):
                    if self.graph.is_directed:
                        # only consider directed '>' edges as outgoing
                        if edge.direction == '>':
                            matrix[i][j] = min(matrix[i][j], weight)
                    else:
                        matrix[i][j] = min(matrix[i][j], weight)
                        matrix[j][i] = min(matrix[j][i], weight)
        
        return matrix, node_list
    

    def print_adjacency_matrix(self):
        """Vytiskne matici sousednosti ve čitelném formátu."""
        matrix, nodes = self.get_adjacency_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice sousednosti")
            return
        # Tisk: využíváme univerzální _print_matrix pro hezké zarovnání
        print("\nMatice sousednosti:")
        self._print_matrix(matrix, nodes, col_labels=nodes)
    
    def print_incidence_matrix(self):
        """Vytiskne matici incidence ve čitelném formátu."""
        matrix, nodes, edges = self.get_incidence_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice incidence")
            return
        # Print incidence matrix with generated edge labels e1,e2,...
        print("\nMatice incidence:")
        col_labels = [f"h{idx+1}" for idx in range(len(edges))]
        self._print_matrix(matrix, nodes, col_labels=col_labels)
    
    def print_weight_matrix(self):
        """Vytiskne matici vah ve čitelném formátu."""
        matrix, nodes = self.get_weight_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice vah")
            return
        # Tisk matice vah: _format_cell se postará o vykreslení floatů a symbolu pro inf
        print("\nMatice vah:")
        self._print_matrix(matrix, nodes, col_labels=nodes)

    def get_adjacency_power(self, k):
        """
        Vrátí matici sousednosti umocněnou na k-tou.
        (A^k)[i][j] = počet cest délky k z i do j.
        """
        # Validace vstupu: k musí být >= 1
        if k < 1:
            raise ValueError('k musí být >= 1')

        A, nodes = self.get_adjacency_matrix()
        if not A:
            return [], []

        # Maticové násobení s ignorováním nul pro úsporu operací
        def mat_mult(X, Y):
            n = len(X)
            Z = [[0]*n for _ in range(n)]
            for i in range(n):
                for p in range(n):
                    if X[i][p] == 0:
                        continue
                    xv = X[i][p]
                    for j in range(n):
                        if Y[p][j]:
                            Z[i][j] += xv * Y[p][j]
            return Z

        result = None
        base = A
        exp = k
        while exp > 0:
            if exp & 1:
                result = mat_mult(result, base) if result is not None else [row[:] for row in base]
            base = mat_mult(base, base)
            exp >>= 1

        return result, nodes

    def _format_cell(self, val):
        # Convert numeric / special values to human-readable strings
        # - float('inf') is rendered as configured inf_symbol
        # - ints are rendered without decimal point
        # - floats are rendered with self.float_precision decimal places
        if val == float('inf'):
            return self.inf_symbol
        if isinstance(val, int):
            return str(val)
        try:
            if abs(val - int(val)) < 1e-9:
                # float representing whole number -> render as int
                return str(int(val))
            fmt = f"{{:.{self.float_precision}f}}"
            return fmt.format(val)
        except Exception:
            return str(val)

    def _analyze_diagonal(self, matrix, show_values=False):
        """Analyzuje hlavní diagonálu matice.
        
        Args:
            matrix: 2D seznam
            show_values: Pokud True, vrátí i seznam všech hodnot na diagonále
            
        Returns:
            dict: Slovník s informacemi o diagonále
        """
        if not matrix:
            return None
        
        n = min(len(matrix), len(matrix[0]) if matrix else 0)
        if n == 0:
            return None
        
        diagonal_values = [matrix[i][i] for i in range(n)]
        zero_count = sum(1 for v in diagonal_values if v == 0)
        nonzero_count = sum(1 for v in diagonal_values if v != 0 and v != float('inf'))
        inf_count = sum(1 for v in diagonal_values if v == float('inf'))
        
        # Seskupení nenulových hodnot pro přehlednější výpis
        nonzero_values = []
        value_counts = {}
        for v in diagonal_values:
            if v != 0 and v != float('inf'):
                nonzero_values.append(v)
                value_counts[v] = value_counts.get(v, 0) + 1
        
        result = {
            'zero_count': zero_count,
            'nonzero_count': nonzero_count,
            'inf_count': inf_count,
            'total': n,
            'diagonal_values': diagonal_values,
            'nonzero_values': nonzero_values,
            'value_counts': value_counts
        }
        
        return result

    def _analyze_anti_diagonal(self, matrix, show_values=False):
        """Analyzuje vedlejší diagonálu matice.
        
        Args:
            matrix: 2D seznam
            show_values: Pokud True, vrátí i seznam všech hodnot na diagonále
            
        Returns:
            dict: Slovník s informacemi o vedlejší diagonále
        """
        if not matrix:
            return None
        
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        n = min(rows, cols)
        
        if n == 0:
            return None
        
        # Vedlejší diagonála: prvky matrix[i][cols-1-i]
        diagonal_values = [matrix[i][cols-1-i] for i in range(n)]
        zero_count = sum(1 for v in diagonal_values if v == 0)
        nonzero_count = sum(1 for v in diagonal_values if v != 0 and v != float('inf'))
        inf_count = sum(1 for v in diagonal_values if v == float('inf'))
        
        # Seskupení nenulových hodnot pro přehlednější výpis
        nonzero_values = []
        value_counts = {}
        for v in diagonal_values:
            if v != 0 and v != float('inf'):
                nonzero_values.append(v)
                value_counts[v] = value_counts.get(v, 0) + 1
        
        result = {
            'zero_count': zero_count,
            'nonzero_count': nonzero_count,
            'inf_count': inf_count,
            'total': n,
            'diagonal_values': diagonal_values,
            'nonzero_values': nonzero_values,
            'value_counts': value_counts,
            'cols': cols  # Potřebujeme pro výpis pozic
        }
        
        return result

    def _print_diagonal_info(self, matrix):
        """Vypíše informace o hlavní diagonále matice."""
        diag_info = self._analyze_diagonal(matrix)
        if not diag_info:
            return
        
        print()
        print("─" * 40)
        print("INFORMACE O HLAVNÍ DIAGONÁLE:")
        print(f"  Celkem prvků:       {diag_info['total']}")
        print(f"  Nulové hodnoty:     {diag_info['zero_count']}")
        print(f"  Nenulové hodnoty:   {diag_info['nonzero_count']}")
        
        if diag_info['inf_count'] > 0:
            print(f"  Nekonečno (∞):      {diag_info['inf_count']}")
        
        # Zobrazit nenulové hodnoty, pokud jich není příliš mnoho
        if diag_info['nonzero_count'] > 0:
            if diag_info['nonzero_count'] <= 20:
                print(f"  Nenulové hodnoty:   ", end="")
                formatted_values = [self._format_cell(v) for v in diag_info['nonzero_values']]
                print(", ".join(formatted_values))
            else:
                # Zobrazit pouze unikátní hodnoty a jejich počet
                print(f"  Unikátní nenulové hodnoty:")
                for val, count in sorted(diag_info['value_counts'].items()):
                    print(f"    {self._format_cell(val)}: {count}×")
        
        print("─" * 40)

    def _print_anti_diagonal_info(self, matrix):
        """Vypíše informace o vedlejší diagonále matice."""
        diag_info = self._analyze_anti_diagonal(matrix)
        if not diag_info:
            return
        
        print()
        print("─" * 40)
        print("INFORMACE O VEDLEJŠÍ DIAGONÁLE:")
        print(f"  Celkem prvků:       {diag_info['total']}")
        print(f"  Nulové hodnoty:     {diag_info['zero_count']}")
        print(f"  Nenulové hodnoty:   {diag_info['nonzero_count']}")
        
        if diag_info['inf_count'] > 0:
            print(f"  Nekonečno (∞):      {diag_info['inf_count']}")
        
        # Zobrazit nenulové hodnoty, pokud jich není příliš mnoho
        if diag_info['nonzero_count'] > 0:
            if diag_info['nonzero_count'] <= 20:
                print(f"  Nenulové hodnoty:   ", end="")
                formatted_values = [self._format_cell(v) for v in diag_info['nonzero_values']]
                print(", ".join(formatted_values))
            else:
                # Zobrazit pouze unikátní hodnoty a jejich počet
                print(f"  Unikátní nenulové hodnoty:")
                for val, count in sorted(diag_info['value_counts'].items()):
                    print(f"    {self._format_cell(val)}: {count}×")
        
        print("─" * 40)

    def _print_matrix(self, matrix, nodes, col_labels=None, show_diagonal_info=False):
        # Pretty-print a 2D matrix with column widths computed from content
        if not matrix:
            print('Prázdná matice')
            return
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0

        # Prepare string table using _format_cell
        table = [[self._format_cell(matrix[i][j]) for j in range(cols)] for i in range(rows)]

        # Compute max width per column (considering content and optional labels)
        col_widths = [max((len(table[i][j]) for i in range(rows)), default=0) for j in range(cols)]
        if col_labels:
            for j, lbl in enumerate(col_labels):
                col_widths[j] = max(col_widths[j], len(str(lbl)))

        # Width for row labels (node ids)
        row_label_width = max((len(str(n)) for n in nodes), default=0)

        # Print header
        print()
        print(' '*(row_label_width+1), end='')
        for j in range(cols):
            lbl = col_labels[j] if col_labels else j+1
            print(f"{str(lbl):>{col_widths[j]+1}}", end='')
        print()

        # Print each row with aligned cells
        for i, node in enumerate(nodes):
            print(f"{str(node):>{row_label_width}} ", end='')
            for j in range(cols):
                print(f"{table[i][j]:>{col_widths[j]+1}}", end='')
            print()
        
        # Zobrazit informace o diagonále pouze pro čtvercové matice (pokud je to požadováno)
        if show_diagonal_info and rows == cols:
            self._print_diagonal_info(matrix)

    
    """
    Uloží matici do CSV souboru.

    Args:
        matrix: 2D seznam (rows x cols)
        nodes: seznam identifikátorů uzlů (řádkové popisky)
        col_labels: seznam popisků pro sloupce (volitelné)
        path: cesta k výstupnímu CSV (pokud None vrátí CSV jako string)
    Returns:
        path (str) when written or CSV string when path is None
    """
    def save_matrix_csv(self, matrix, nodes, col_labels=None, path=None):
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0

        header = [''] + [str(l) for l in (col_labels if col_labels is not None else nodes)]

        table = []
        for i, node in enumerate(nodes):
            row = [str(node)]
            for j in range(cols):
                val = matrix[i][j]
                if val == float('inf'):
                    row.append('')
                else:
                    row.append(str(val))
            table.append(row)

        if path is None:
            from io import StringIO
            sio = StringIO()
            writer = csv.writer(sio)
            writer.writerow(header)
            writer.writerows(table)
            return sio.getvalue()

        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(table)
        return path

    # ========== Maticové operace ==========

    def sum_row(self, matrix, row_idx):
        """Vrátí součet hodnot v daném řádku."""
        if not matrix or row_idx >= len(matrix):
            return 0
        return sum(val for val in matrix[row_idx] if val != float('inf'))

    def sum_column(self, matrix, col_idx):
        """Vrátí součet hodnot v daném sloupci."""
        if not matrix or col_idx >= len(matrix[0]):
            return 0
        return sum(row[col_idx] for row in matrix if row[col_idx] != float('inf'))

    def sum_main_diagonal(self, matrix):
        """Vrátí součet hlavní diagonály (levý horní → pravý dolní)."""
        if not matrix:
            return 0
        n = min(len(matrix), len(matrix[0]) if matrix else 0)
        return sum(matrix[i][i] for i in range(n) if matrix[i][i] != float('inf'))

    def sum_anti_diagonal(self, matrix):
        """Vrátí součet vedlejší diagonály (pravý horní → levý dolní)."""
        if not matrix:
            return 0
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        n = min(rows, cols)
        return sum(matrix[i][cols-1-i] for i in range(n) if matrix[i][cols-1-i] != float('inf'))

    def sum_all(self, matrix):
        """Vrátí součet všech hodnot v matici."""
        if not matrix:
            return 0
        total = 0
        for row in matrix:
            for val in row:
                if val != float('inf'):
                    total += val
        return total

    def transpose(self, matrix):
        """Vrátí transponovanou matici."""
        if not matrix:
            return []
        return [list(row) for row in zip(*matrix)]

    def is_symmetric(self, matrix):
        """Zkontroluje, zda je matice symetrická."""
        if not matrix:
            return True
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        if rows != cols:
            return False
        for i in range(rows):
            for j in range(i+1, cols):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True

    def trace(self, matrix):
        """Vrátí stopu matice (součet prvků na hlavní diagonále)."""
        return self.sum_main_diagonal(matrix)

    def matrix_multiply(self, A, B):
        """Vynásobí dvě matice A × B."""
        if not A or not B:
            return []
        rows_A = len(A)
        cols_A = len(A[0]) if rows_A else 0
        rows_B = len(B)
        cols_B = len(B[0]) if rows_B else 0
        
        if cols_A != rows_B:
            raise ValueError(f"Matice nelze násobit: {rows_A}×{cols_A} a {rows_B}×{cols_B}")
        
        result = [[0] * cols_B for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                s = 0
                for k in range(cols_A):
                    if A[i][k] != float('inf') and B[k][j] != float('inf'):
                        s += A[i][k] * B[k][j]
                result[i][j] = s
        return result

    def search_in_matrix(self, matrix, nodes, value=None, min_val=None, max_val=None, condition=None):
        """
        Vyhledá buňky v matici podle kritérií.
        
        Args:
            matrix: 2D seznam
            nodes: seznam identifikátorů uzlů
            value: přesná hodnota k nalezení
            min_val: minimální hodnota (včetně)
            max_val: maximální hodnota (včetně)
            condition: vlastní funkce pro filtrování (lambda val: bool)
        
        Returns:
            list of dict: [{'row': idx, 'col': idx, 'row_node': id, 'col_node': id, 'value': val}, ...]
        """
        if not matrix:
            return []
        
        results = []
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        
        for i in range(rows):
            for j in range(cols):
                val = matrix[i][j]
                
                # Ignorovat nekonečno pokud není explicitně hledáno
                if val == float('inf') and value != float('inf'):
                    continue
                
                # Kontrola podmínek
                match = False
                if value is not None:
                    match = (val == value)
                elif min_val is not None and max_val is not None:
                    match = (min_val <= val <= max_val)
                elif min_val is not None:
                    match = (val >= min_val)
                elif max_val is not None:
                    match = (val <= max_val)
                elif condition is not None:
                    match = condition(val)
                else:
                    match = True  # bez podmínky vrátit vše
                
                if match:
                    results.append({
                        'row': i,
                        'col': j,
                        'row_node': nodes[i] if i < len(nodes) else i,
                        'col_node': nodes[j] if j < len(nodes) else j,
                        'value': val
                    })
        
        return results

    def find_max_in_matrix(self, matrix, nodes):
        """Najde maximální hodnotu (hodnoty) v matici."""
        if not matrix:
            return []
        
        max_val = float('-inf')
        for row in matrix:
            for val in row:
                if val != float('inf') and val > max_val:
                    max_val = val
        
        if max_val == float('-inf'):
            return []
        
        return self.search_in_matrix(matrix, nodes, value=max_val)

    def find_min_in_matrix(self, matrix, nodes):
        """Najde minimální hodnotu (hodnoty) v matici."""
        if not matrix:
            return []
        
        min_val = float('inf')
        for row in matrix:
            for val in row:
                if val != float('inf') and val < min_val:
                    min_val = val
        
        if min_val == float('inf'):
            return []
        
        return self.search_in_matrix(matrix, nodes, value=min_val)

    def find_nonzero_in_matrix(self, matrix, nodes):
        """Najde všechny nenulové buňky v matici."""
        return self.search_in_matrix(matrix, nodes, condition=lambda v: v != 0 and v != float('inf'))

    def get_cell_value(self, matrix, nodes, row, col):
        """
        Vrátí hodnotu na dané pozici v matici.
        
        Args:
            matrix: 2D seznam
            nodes: seznam identifikátorů uzlů
            row: index řádku (může být číslo nebo ID uzlu)
            col: index sloupce (může být číslo nebo ID uzlu)
        
        Returns:
            dict: {'row': idx, 'col': idx, 'row_node': id, 'col_node': id, 'value': val}
            nebo None pokud pozice neexistuje
        """
        if not matrix:
            return None
        
        # Převést ID uzlu na index pokud je třeba
        row_idx = row
        col_idx = col
        
        if isinstance(row, str):
            try:
                row_idx = nodes.index(row)
            except (ValueError, AttributeError):
                return None
        
        if isinstance(col, str):
            try:
                col_idx = nodes.index(col)
            except (ValueError, AttributeError):
                return None
        
        # Kontrola rozsahu
        if row_idx < 0 or row_idx >= len(matrix):
            return None
        if col_idx < 0 or col_idx >= len(matrix[0]):
            return None
        
        return {
            'row': row_idx,
            'col': col_idx,
            'row_node': nodes[row_idx] if row_idx < len(nodes) else row_idx,
            'col_node': nodes[col_idx] if col_idx < len(nodes) else col_idx,
            'value': matrix[row_idx][col_idx]
        }

    def interactive_matrix_operations(self, matrix, nodes, matrix_name="matice"):
        """Interaktivní menu pro práci s maticí."""
        if not matrix:
            print("Prázdná matice - žádné operace nejsou k dispozici")
            return

        while True:
            print(f"\n{'='*60}")
            print(f"OPERACE S MATICÍ ({matrix_name})")
            print("="*60)
            print("1. Součet řádku")
            print("2. Součet sloupce")
            print("3. Součet hlavní diagonály")
            print("4. Součet vedlejší diagonály")
            print("5. Celkový součet matice")
            print("6. Transpozice")
            print("7. Kontrola symetrie")
            print("8. Stopa matice (trace)")
            print("9. Zobrazit matici znovu")
            print("10. Vyhledat hodnotu")
            print("11. Vyhledat rozsah hodnot")
            print("12. Najít maximum")
            print("13. Najít minimum")
            print("14. Najít nenulové hodnoty")
            print("15. Zobrazit hodnotu na pozici [řádek, sloupec]")
            print("16. Informace o hlavní diagonále")
            print("17. Informace o vedlejší diagonále")
            print("18. Počet sledů délky k mezi dvěma uzly")
            print("19. Hledat hodnotu na hlavní diagonále")
            print("20. Hledat hodnotu na vedlejší diagonále")
            print("0. Zpět")
            print("="*60)

            try:
                choice = input("Vyberte operaci: ").strip()
                
                if choice == '0':
                    break
                elif choice == '1':
                    print(f"\nDostupné řádky: 0-{len(matrix)-1}")
                    for i, node in enumerate(nodes):
                        print(f"  [{i}] {node}")
                    row_idx = int(input("Zadejte index řádku: "))
                    if 0 <= row_idx < len(matrix):
                        total = self.sum_row(matrix, row_idx)
                        print(f"Součet řádku {row_idx} ({nodes[row_idx]}): {total}")
                    else:
                        print("Neplatný index řádku")
                
                elif choice == '2':
                    cols = len(matrix[0]) if matrix else 0
                    print(f"\nDostupné sloupce: 0-{cols-1}")
                    for j in range(cols):
                        print(f"  [{j}] {nodes[j] if j < len(nodes) else j}")
                    col_idx = int(input("Zadejte index sloupce: "))
                    if 0 <= col_idx < cols:
                        total = self.sum_column(matrix, col_idx)
                        label = nodes[col_idx] if col_idx < len(nodes) else str(col_idx)
                        print(f"Součet sloupce {col_idx} ({label}): {total}")
                    else:
                        print("Neplatný index sloupce")
                
                elif choice == '3':
                    total = self.sum_main_diagonal(matrix)
                    print(f"Součet hlavní diagonály: {total}")
                
                elif choice == '4':
                    total = self.sum_anti_diagonal(matrix)
                    print(f"Součet vedlejší diagonály: {total}")
                
                elif choice == '5':
                    total = self.sum_all(matrix)
                    print(f"Celkový součet matice: {total}")
                
                elif choice == '6':
                    transposed = self.transpose(matrix)
                    print("\nTransponovaná matice:")
                    self._print_matrix(transposed, nodes, col_labels=nodes)
                
                elif choice == '7':
                    is_sym = self.is_symmetric(matrix)
                    print(f"Matice je symetrická: {'Ano' if is_sym else 'Ne'}")
                
                elif choice == '8':
                    tr = self.trace(matrix)
                    print(f"Stopa matice (trace): {tr}")
                
                elif choice == '9':
                    print(f"\n{matrix_name.capitalize()}:")
                    self._print_matrix(matrix, nodes, col_labels=nodes)
                
                elif choice == '10':
                    val_str = input("Zadejte hodnotu k vyhledání: ").strip()
                    try:
                        # Zkusit parsovat jako číslo
                        if val_str.lower() in ['inf', '∞', 'infinity']:
                            search_val = float('inf')
                        else:
                            search_val = float(val_str) if '.' in val_str else int(val_str)
                        
                        results = self.search_in_matrix(matrix, nodes, value=search_val)
                        if results:
                            print()  # prázdný řádek
                            for r in results:
                                print(f"   [{r['row']}, {r['col']}] ({r['row_node']} → {r['col_node']}): {self._format_cell(r['value'])}")
                            print(f"\n✅ Nalezeno celkem {len(results)} buněk s hodnotou {self._format_cell(search_val)}")
                        else:
                            print(f"\n❌ Hodnota {self._format_cell(search_val)} nebyla nalezena")
                    except ValueError:
                        print("❌ Neplatná hodnota")
                
                elif choice == '11':
                    try:
                        min_str = input("Minimální hodnota (Enter pro žádnou): ").strip()
                        max_str = input("Maximální hodnota (Enter pro žádnou): ").strip()
                        
                        min_val = None if not min_str else (float(min_str) if '.' in min_str else int(min_str))
                        max_val = None if not max_str else (float(max_str) if '.' in max_str else int(max_str))
                        
                        results = self.search_in_matrix(matrix, nodes, min_val=min_val, max_val=max_val)
                        if results:
                            print()  # prázdný řádek
                            # Zobrazit max 20 výsledků
                            for r in results[:20]:
                                print(f"   [{r['row']}, {r['col']}] ({r['row_node']} → {r['col_node']}): {self._format_cell(r['value'])}")
                            
                            range_str = f"{min_val if min_val is not None else '-∞'} až {max_val if max_val is not None else '+∞'}"
                            if len(results) > 20:
                                print(f"   ... a dalších {len(results) - 20} buněk")
                            print(f"\n✅ Nalezeno celkem {len(results)} buněk v rozsahu {range_str}")
                        else:
                            print("\n❌ Žádné buňky v daném rozsahu")
                    except ValueError:
                        print("❌ Neplatný vstup")
                
                elif choice == '12':
                    results = self.find_max_in_matrix(matrix, nodes)
                    if results:
                        max_val = results[0]['value']
                        print(f"\n✅ Maximální hodnota: {self._format_cell(max_val)}")
                        for r in results:
                            print(f"   [{r['row']}, {r['col']}] ({r['row_node']} → {r['col_node']})")
                        print(f"\nNalezeno na {len(results)} pozicích")
                    else:
                        print("\n❌ Matice neobsahuje žádné platné hodnoty")
                
                elif choice == '13':
                    results = self.find_min_in_matrix(matrix, nodes)
                    if results:
                        min_val = results[0]['value']
                        print(f"\n✅ Minimální hodnota: {self._format_cell(min_val)}")
                        for r in results:
                            print(f"   [{r['row']}, {r['col']}] ({r['row_node']} → {r['col_node']})")
                        print(f"\nNalezeno na {len(results)} pozicích")
                    else:
                        print("\n❌ Matice neobsahuje žádné platné hodnoty")
                
                elif choice == '14':
                    results = self.find_nonzero_in_matrix(matrix, nodes)
                    if results:
                        print()  # prázdný řádek
                        # Zobrazit max 20 výsledků
                        for r in results[:20]:
                            print(f"   [{r['row']}, {r['col']}] ({r['row_node']} → {r['col_node']}): {self._format_cell(r['value'])}")
                        
                        if len(results) > 20:
                            print(f"   ... a dalších {len(results) - 20} buněk")
                        print(f"\n✅ Nalezeno celkem {len(results)} nenulových buněk")
                    else:
                        print("\n❌ Všechny buňky jsou nulové")
                
                elif choice == '15':
                    print("\n💡 Můžete zadat index (0-based) nebo ID uzlu")
                    print(f"Dostupné uzly: {', '.join(str(n) for n in nodes)}")
                    row_input = input("Zadejte řádek: ").strip()
                    col_input = input("Zadejte sloupec: ").strip()
                    
                    try:
                        # Zkusit parsovat jako číslo nebo použít jako ID uzlu
                        row = int(row_input) if row_input.isdigit() else row_input
                        col = int(col_input) if col_input.isdigit() else col_input
                        
                        result = self.get_cell_value(matrix, nodes, row, col)
                        if result:
                            val = result['value']
                            print(f"\n✅ Pozice [{result['row']}, {result['col']}]")
                            print(f"   Řádek (od): {result['row_node']}")
                            print(f"   Sloupec (do): {result['col_node']}")
                            print(f"   Hodnota: {self._format_cell(val)}")
                            
                            # Kontextové informace
                            if val == 0:
                                print(f"   ℹ️  Žádná přímá hrana mezi uzly")
                            elif val == float('inf'):
                                print(f"   ℹ️  Žádné spojení (nedostupné)")
                            elif result['row'] == result['col']:
                                if val > 0:
                                    print(f"   ℹ️  Smyčka na uzlu {result['row_node']}")
                                else:
                                    print(f"   ℹ️  Diagonální prvek (uzel sám se sebou)")
                            else:
                                if val > 0:
                                    print(f"   ℹ️  Existuje {int(val) if isinstance(val, (int, float)) and val == int(val) else val} hrana(n)")
                        else:
                            print("❌ Neplatná pozice nebo uzel neexistuje")
                    except Exception as e:
                        print(f"❌ Chyba: {e}")
                
                elif choice == '16':
                    # Zobrazit informace o hlavní diagonále
                    rows = len(matrix)
                    cols = len(matrix[0]) if rows else 0
                    
                    if rows != cols:
                        print("\n⚠️  Matice není čtvercová - nemá hlavní diagonálu")
                    else:
                        diag_info = self._analyze_diagonal(matrix)
                        if diag_info:
                            print()
                            print("─" * 60)
                            print("INFORMACE O HLAVNÍ DIAGONÁLE")
                            print("─" * 60)
                            print(f"Celkem prvků na diagonále:  {diag_info['total']}")
                            print(f"Nulové hodnoty:              {diag_info['zero_count']}")
                            print(f"Nenulové hodnoty:            {diag_info['nonzero_count']}")
                            
                            if diag_info['inf_count'] > 0:
                                print(f"Nekonečno (∞):               {diag_info['inf_count']}")
                            
                            # Zobrazit všechny hodnoty na diagonále
                            if diag_info['total'] > 0:
                                print(f"\nVšechny hodnoty na hlavní diagonále:")
                                for i, val in enumerate(diag_info['diagonal_values']):
                                    node_label = nodes[i] if i < len(nodes) else i
                                    print(f"  [{i}] {node_label}: {self._format_cell(val)}")
                            
                            # Zobrazit statistiku nenulových hodnot
                            if diag_info['nonzero_count'] > 0:
                                print(f"\nNenulové hodnoty - statistika:")
                                for val, count in sorted(diag_info['value_counts'].items()):
                                    print(f"  {self._format_cell(val)}: {count}× (vyskytuje se {count}krát)")
                            
                            print("─" * 60)
                        else:
                            print("\n❌ Nelze analyzovat hlavní diagonálu")
                
                elif choice == '17':
                    # Zobrazit informace o vedlejší diagonále
                    rows = len(matrix)
                    cols = len(matrix[0]) if rows else 0
                    
                    if rows != cols:
                        print("\n⚠️  Matice není čtvercová - nemá vedlejší diagonálu")
                    else:
                        diag_info = self._analyze_anti_diagonal(matrix)
                        if diag_info:
                            print()
                            print("─" * 60)
                            print("INFORMACE O VEDLEJŠÍ DIAGONÁLE")
                            print("─" * 60)
                            print(f"Celkem prvků na diagonále:  {diag_info['total']}")
                            print(f"Nulové hodnoty:              {diag_info['zero_count']}")
                            print(f"Nenulové hodnoty:            {diag_info['nonzero_count']}")
                            
                            if diag_info['inf_count'] > 0:
                                print(f"Nekonečno (∞):               {diag_info['inf_count']}")
                            
                            # Zobrazit všechny hodnoty na vedlejší diagonále
                            if diag_info['total'] > 0:
                                print(f"\nVšechny hodnoty na vedlejší diagonále:")
                                for i, val in enumerate(diag_info['diagonal_values']):
                                    # Pro vedlejší diagonálu: row=i, col=cols-1-i
                                    row_label = nodes[i] if i < len(nodes) else i
                                    col_idx = diag_info['cols'] - 1 - i
                                    col_label = nodes[col_idx] if col_idx < len(nodes) else col_idx
                                    print(f"  [{i},{col_idx}] ({row_label} → {col_label}): {self._format_cell(val)}")
                            
                            # Zobrazit statistiku nenulových hodnot
                            if diag_info['nonzero_count'] > 0:
                                print(f"\nNenulové hodnoty - statistika:")
                                for val, count in sorted(diag_info['value_counts'].items()):
                                    print(f"  {self._format_cell(val)}: {count}× (vyskytuje se {count}krát)")
                            
                            print("─" * 60)
                        else:
                            print("\n❌ Nelze analyzovat vedlejší diagonálu")
                
                elif choice == '18':
                    # Počet sledů délky k mezi dvěma uzly
                    print("\n💡 Tato funkce vypočítá počet sledů délky k mezi dvěma uzly")
                    print("   (Sled = cesta, která může procházet stejnými uzly/hranami opakovaně)")
                    print()
                    print(f"Dostupné uzly: {', '.join(str(n) for n in nodes)}")
                    
                    try:
                        start_node = input("Zadejte počáteční uzel: ").strip()
                        end_node = input("Zadejte koncový uzel: ").strip()
                        k_str = input("Zadejte délku sledů (k): ").strip()
                        
                        # Validace vstupu
                        if start_node not in nodes:
                            print(f"❌ Uzel '{start_node}' neexistuje v grafu")
                            continue
                        
                        if end_node not in nodes:
                            print(f"❌ Uzel '{end_node}' neexistuje v grafu")
                            continue
                        
                        k = int(k_str)
                        if k < 1:
                            print("❌ Délka k musí být alespoň 1")
                            continue
                        
                        # Spočítat A^k
                        print(f"\n⏳ Počítám matici sousednosti na {k}. mocninu...")
                        A_k, nodes_list = self.get_adjacency_power(k)
                        
                        if not A_k:
                            print("❌ Nepodařilo se vypočítat matici")
                            continue
                        
                        # Najít indexy uzlů
                        start_idx = nodes_list.index(start_node)
                        end_idx = nodes_list.index(end_node)
                        
                        # Získat počet sledů
                        count = A_k[start_idx][end_idx]
                        
                        # Zobrazit výsledek
                        print()
                        print("─" * 60)
                        print("VÝSLEDEK")
                        print("─" * 60)
                        print(f"Počáteční uzel:     {start_node}")
                        print(f"Koncový uzel:       {end_node}")
                        print(f"Délka sledů:        {k}")
                        print(f"Počet sledů:        {count}")
                        print("─" * 60)
                        
                        if count == 0:
                            print(f"\nℹ️  Neexistuje žádný sled délky {k} z uzlu {start_node} do uzlu {end_node}")
                        elif count == 1:
                            print(f"\n✅ Existuje přesně 1 sled délky {k} z uzlu {start_node} do uzlu {end_node}")
                        else:
                            print(f"\n✅ Existuje {count} různých sledů délky {k} z uzlu {start_node} do uzlu {end_node}")
                        
                        # Nabídnout zobrazení celé matice A^k
                        show_matrix = input(f"\nChcete zobrazit celou matici A^{k}? (a/n): ").strip().lower()
                        if show_matrix == 'a':
                            print(f"\nMatice sousednosti na {k}. mocninu:")
                            self._print_matrix(A_k, nodes_list, col_labels=nodes_list)
                        
                    except ValueError as e:
                        print(f"❌ Neplatný vstup: {e}")
                    except Exception as e:
                        print(f"❌ Chyba: {e}")
                
                elif choice == '19':
                    # Hledat hodnotu na hlavní diagonále
                    rows = len(matrix)
                    cols = len(matrix[0]) if rows else 0
                    
                    if rows != cols:
                        print("\n⚠️  Matice není čtvercová - nemá hlavní diagonálu")
                        continue
                    
                    try:
                        val_str = input("\nZadejte hodnotu k vyhledání na hlavní diagonále: ").strip()
                        
                        # Parsovat hodnotu
                        if val_str.lower() in ['inf', '∞', 'infinity']:
                            search_val = float('inf')
                        else:
                            search_val = float(val_str) if '.' in val_str else int(val_str)
                        
                        # Najít všechny výskyty na hlavní diagonále
                        diag_info = self._analyze_diagonal(matrix)
                        if not diag_info:
                            print("❌ Nelze analyzovat diagonálu")
                            continue
                        
                        matches = []
                        for i, val in enumerate(diag_info['diagonal_values']):
                            if val == search_val:
                                node_label = nodes[i] if i < len(nodes) else i
                                matches.append((i, node_label, val))
                        
                        # Zobrazit výsledky
                        print()
                        print("─" * 60)
                        print("HLEDÁNÍ NA HLAVNÍ DIAGONÁLE")
                        print("─" * 60)
                        print(f"Hledaná hodnota:    {self._format_cell(search_val)}")
                        print(f"Počet výskytů:      {len(matches)}")
                        print("─" * 60)
                        
                        if matches:
                            print(f"\n✅ Hodnota {self._format_cell(search_val)} nalezena na pozicích:")
                            for i, node_label, val in matches:
                                print(f"  [{i},{i}] uzel {node_label}: {self._format_cell(val)}")
                        else:
                            print(f"\n❌ Hodnota {self._format_cell(search_val)} nebyla na hlavní diagonále nalezena")
                        
                        print()
                        
                    except ValueError:
                        print("❌ Neplatná hodnota")
                    except Exception as e:
                        print(f"❌ Chyba: {e}")
                
                elif choice == '20':
                    # Hledat hodnotu na vedlejší diagonále
                    rows = len(matrix)
                    cols = len(matrix[0]) if rows else 0
                    
                    if rows != cols:
                        print("\n⚠️  Matice není čtvercová - nemá vedlejší diagonálu")
                        continue
                    
                    try:
                        val_str = input("\nZadejte hodnotu k vyhledání na vedlejší diagonále: ").strip()
                        
                        # Parsovat hodnotu
                        if val_str.lower() in ['inf', '∞', 'infinity']:
                            search_val = float('inf')
                        else:
                            search_val = float(val_str) if '.' in val_str else int(val_str)
                        
                        # Najít všechny výskyty na vedlejší diagonále
                        diag_info = self._analyze_anti_diagonal(matrix)
                        if not diag_info:
                            print("❌ Nelze analyzovat vedlejší diagonálu")
                            continue
                        
                        matches = []
                        for i, val in enumerate(diag_info['diagonal_values']):
                            if val == search_val:
                                row_label = nodes[i] if i < len(nodes) else i
                                col_idx = diag_info['cols'] - 1 - i
                                col_label = nodes[col_idx] if col_idx < len(nodes) else col_idx
                                matches.append((i, col_idx, row_label, col_label, val))
                        
                        # Zobrazit výsledky
                        print()
                        print("─" * 60)
                        print("HLEDÁNÍ NA VEDLEJŠÍ DIAGONÁLE")
                        print("─" * 60)
                        print(f"Hledaná hodnota:    {self._format_cell(search_val)}")
                        print(f"Počet výskytů:      {len(matches)}")
                        print("─" * 60)
                        
                        if matches:
                            print(f"\n✅ Hodnota {self._format_cell(search_val)} nalezena na pozicích:")
                            for row_i, col_i, row_label, col_label, val in matches:
                                print(f"  [{row_i},{col_i}] ({row_label} → {col_label}): {self._format_cell(val)}")
                        else:
                            print(f"\n❌ Hodnota {self._format_cell(search_val)} nebyla na vedlejší diagonále nalezena")
                        
                        print()
                        
                    except ValueError:
                        print("❌ Neplatná hodnota")
                    except Exception as e:
                        print(f"❌ Chyba: {e}")
                
                else:
                    print("Neplatná volba")
                    
            except ValueError:
                print("Neplatný vstup")
            except KeyboardInterrupt:
                print("\nPřerušeno")
                break
            except Exception as e:
                print(f"Chyba: {e}")
