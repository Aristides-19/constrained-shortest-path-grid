import heapq
from typing import List, Dict, Tuple, Any, Optional
from src.graph import GridGraph
from src.types import Node, Edge, Path, EdgeInterval

# TODO check como funciona

def dijkstra(graph: GridGraph, start: Node, end: Node) -> Tuple[Optional[Path], float]:
    """
    Algoritmo de Dijkstra estándar para encontrar el camino más corto.
    
    Args:
        graph (GridGraph): Instancia del grafo.
        start (tuple): Nodo de inicio (calle, carrera).
        end (tuple): Nodo de destino (calle, carrera).
        
    Returns:
        tuple: (camino, costo)
    """
    adjacency_map = graph.to_adjacency_map()
    
    # Cola de prioridad: (costo_acumulado, nodo_actual, camino_recorrido)
    queue = [(0, start, [start])]
    visited: Dict[Node, int] = {}
    
    while queue:
        cost, current, path = heapq.heappop(queue)
        
        if current == end:
            return path, float(cost)
            
        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        
        for neighbor, weight in adjacency_map[current].items():
            new_cost = cost + weight
            if neighbor not in visited or new_cost < visited.get(neighbor, float('inf')):
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
                
    return None, float('inf')

def find_all_paths(graph: GridGraph, start: Node, end: Node, max_cost: int) -> List[Tuple[Path, int]]:
    """
    Encuentra todos los caminos simples desde 'start' hasta 'end' con un costo menor o igual a 'max_cost'.
    Utiliza búsqueda en profundidad (DFS) con poda de costo.
    """
    adjacency_map = graph.to_adjacency_map()
    paths: List[Tuple[Path, int]] = []
    
    def dfs(curr: Node, path: Path, cost: int) -> None:
        if cost > max_cost:
            return
        if curr == end:
            paths.append((list(path), cost))
            return
        
        for neighbor, weight in adjacency_map[curr].items():
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path, cost + weight)
                path.pop()
                
    dfs(start, [start], 0)
    return paths

def get_node_times_backwards(path: Path, total_cost: int, graph: GridGraph) -> Dict[Node, int]:
    """
    Calcula los instantes de tiempo en los que se encuentra en cada nodo del camino,
    alineando la llegada al destino final (último nodo del camino) en el tiempo T = 0.
    Retorna un diccionario {nodo: tiempo_fisico_relativo}.
    """
    node_times: Dict[Node, int] = {}
    curr_time = 0 # Tiempo de llegada al destino es 0
    node_times[path[-1]] = curr_time
    
    adjacency_map = graph.to_adjacency_map()
    
    # Retroceder desde el destino hacia el inicio
    for i in range(len(path) - 2, -1, -1):
        u = path[i]
        v = path[i+1]
        weight = adjacency_map[u][v]
        curr_time -= weight
        node_times[u] = curr_time
        
    return node_times

def get_edge_intervals_backwards(path: Path, graph: GridGraph) -> List[EdgeInterval]:
    """
    Calcula los intervalos de tiempo en los que se recorre cada arista (calle).
    Retorna una lista de tuplas: (arista_normalizada, t_inicio, t_fin)
    Donde arista_normalizada es una tupla ordenada de los dos nodos.
    """
    intervals: List[EdgeInterval] = []
    curr_time = 0
    adjacency_map = graph.to_adjacency_map()
    
    for i in range(len(path) - 2, -1, -1):
        u = path[i]
        v = path[i+1]
        weight = adjacency_map[u][v]
        t_start = curr_time - weight
        t_end = curr_time
        
        sorted_nodes = sorted([u, v])
        edge: Edge = (sorted_nodes[0], sorted_nodes[1])
        intervals.append((edge, t_start, t_end))
        curr_time -= weight
        
    return intervals

def check_conflict(path_j: Path, cost_j: int, path_a: Path, cost_a: int, graph: GridGraph) -> bool:
    """
    Verifica si existen conflictos de cruce físico o temporal entre las dos rutas.
    Alinea la llegada al destino común a las 12:00 (o tiempo final = 0).
    
    Returns:
        bool: True si hay conflicto, False si no hay conflicto.
    """
    # 1. Conflicto de Vértice (estar en la misma intersección al mismo tiempo)
    times_j = get_node_times_backwards(path_j, cost_j, graph)
    times_a = get_node_times_backwards(path_a, cost_a, graph)
    
    # El destino final común no cuenta como conflicto porque allí se encuentran
    destination = path_j[-1]
    
    for node in times_j:
        if node != destination and node in times_a:
            # Si coinciden en el mismo nodo al mismo tiempo exacto
            if abs(times_j[node] - times_a[node]) < 0.001:
                return True
                
    # 2. Conflicto de Arista (caminar por la misma cuadra/calle en intervalos de tiempo superpuestos)
    edges_j = get_edge_intervals_backwards(path_j, graph)
    edges_a = get_edge_intervals_backwards(path_a, graph)
    
    for edge_j, start_j, end_j in edges_j:
        for edge_a, start_a, end_a in edges_a:
            if edge_j == edge_a:
                # Si es la misma arista, comprobar si los intervalos de tiempo se solapan
                if max(start_j, start_a) < min(end_j, end_a):
                    return True
                    
    return False

def find_optimal_paths(graph: GridGraph, start_j: Node, start_a: Node, destination: Node) -> Optional[Dict[str, Any]]:
    """
    Encuentra las rutas óptimas para Javier y Andreína que minimizan el costo total
    sin conflictos temporales ni espaciales (sin caminar juntos).
    Utiliza una búsqueda por incremento gradual de costo (Iterative Deepening cost search).
    """
    # 1. Obtener costos mínimos individuales
    _, min_cost_j = dijkstra(graph, start_j, destination)
    _, min_cost_a = dijkstra(graph, start_a, destination)
    
    if min_cost_j == float('inf') or min_cost_a == float('inf'):
        return None
        
    # Inicializar límites de búsqueda
    limit_j = int(min_cost_j)
    limit_a = int(min_cost_a)
    
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        # Encontrar todos los caminos dentro de los límites de costo actuales
        paths_j = find_all_paths(graph, start_j, destination, limit_j)
        paths_a = find_all_paths(graph, start_a, destination, limit_a)
        
        # Generar pares y ordenarlos por costo total acumulado
        candidates: List[Tuple[Path, int, Path, int]] = []
        for p_j, c_j in paths_j:
            for p_a, c_a in paths_a:
                candidates.append((p_j, c_j, p_a, c_a))
                
        # Ordenar por costo combinado mínimo (tiempo total de la pareja)
        candidates.sort(key=lambda x: x[1] + x[3])
        
        # Verificar cada candidato
        for p_j, c_j, p_a, c_a in candidates:
            if not check_conflict(p_j, c_j, p_a, c_a, graph):
                # Encontrado el par óptimo libre de conflictos
                return {
                    "javier": {"path": p_j, "cost": c_j},
                    "andreina": {"path": p_a, "cost": c_a}
                }
                
        # Si no hay combinación libre de conflictos, incrementamos el límite de búsqueda
        limit_j += 2
        limit_a += 2
        iteration += 1
        
    return None
