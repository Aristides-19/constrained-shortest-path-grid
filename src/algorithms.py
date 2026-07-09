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
    # Obtiene el mapa de adyacencia del grafo (diccionario de diccionarios con pesos de calles)
    adjacency_map = graph.to_adjacency_map()
    
    # Cola de prioridad: almacena tuplas (costo_acumulado, nodo_actual, camino_recorrido)
    # Se inicializa con costo 0, el nodo de inicio y el camino inicial que solo contiene 'start'
    queue = [(0, start, [start])]
    
    # Diccionario para registrar el menor costo conocido para llegar a cada nodo visitado
    visited: Dict[Node, int] = {}
    
    while queue:
        # Extrae de la cola el elemento con el menor costo acumulado
        cost, current, path = heapq.heappop(queue)
        
        # Si llegamos al nodo destino, retornamos el camino y el costo total
        if current == end:
            return path, float(cost)
            
        # Si el nodo ya fue visitado con un costo menor o igual, descartamos este camino
        if current in visited and visited[current] <= cost:
            continue
        # Registramos/actualizamos el menor costo para el nodo actual
        visited[current] = cost
        
        # Iteramos sobre los vecinos del nodo actual y sus respectivos pesos (costos de cuadra)
        for neighbor, weight in adjacency_map[current].items():
            # Calculamos el nuevo costo acumulado para llegar al vecino
            new_cost = cost + weight
            # Si el vecino no ha sido visitado, o encontramos un camino más barato hacia él:
            if neighbor not in visited or new_cost < visited.get(neighbor, float('inf')):
                # Insertamos el nuevo estado en la cola de prioridad
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
                
    # Si la cola se vacía y no encontramos un camino, retornamos None e infinito
    return None, float('inf')

def find_all_paths(graph: GridGraph, start: Node, end: Node, max_cost: int) -> List[Tuple[Path, int]]:
    """
    Encuentra todos los caminos simples desde 'start' hasta 'end' con un costo menor o igual a 'max_cost'.
    Utiliza búsqueda en profundidad (DFS) con poda de costo.
    """
    # Obtiene el mapa de adyacencia del grafo
    adjacency_map = graph.to_adjacency_map()
    # Lista para almacenar los resultados: parejas de (camino, costo_total)
    paths: List[Tuple[Path, int]] = []
    
    # Función auxiliar recursiva para realizar la búsqueda en profundidad (DFS)
    def dfs(curr: Node, path: Path, cost: int) -> None:
        # Si el costo acumulado supera el costo máximo permitido, podamos la búsqueda y regresamos
        if cost > max_cost:
            return
        # Si el nodo actual es el destino, guardamos una copia del camino y su costo
        if curr == end:
            paths.append((list(path), cost))
            return
        
        # Exploramos todos los vecinos del nodo actual
        for neighbor, weight in adjacency_map[curr].items():
            # Evitamos ciclos asegurando que el vecino no esté ya en el camino actual
            if neighbor not in path:
                # Agregamos el vecino al camino actual
                path.append(neighbor)
                # Llamada recursiva avanzando al vecino con el costo actualizado
                dfs(neighbor, path, cost + weight)
                # Backtracking: removemos el vecino para explorar otras rutas alternativas
                path.pop()
                
    # Iniciamos la búsqueda DFS desde el nodo start con costo inicial 0
    dfs(start, [start], 0)
    # Retornamos todos los caminos válidos encontrados
    return paths

def get_node_times_backwards(path: Path, total_cost: int, graph: GridGraph) -> Dict[Node, int]:
    """
    Calcula los instantes de tiempo en los que se encuentra en cada nodo del camino,
    alineando la llegada al destino final (último nodo del camino) en el tiempo T = 0.
    Retorna un diccionario {nodo: tiempo_fisico_relativo}.
    """
    # Diccionario para asociar cada nodo del camino con su instante de tiempo relativo
    node_times: Dict[Node, int] = {}
    # El tiempo al llegar al destino (último nodo de la lista) se define como 0
    curr_time = 0 
    node_times[path[-1]] = curr_time
    
    # Obtiene el mapa de adyacencia del grafo para consultar los pesos de las aristas
    adjacency_map = graph.to_adjacency_map()
    
    # Retrocedemos en el camino: desde el penúltimo nodo (índice len-2) hasta el inicial (índice 0)
    for i in range(len(path) - 2, -1, -1):
        u = path[i]        # Nodo anterior
        v = path[i+1]      # Nodo siguiente
        # Consultamos el tiempo/costo de transitar entre u y v
        weight = adjacency_map[u][v]
        # Restamos el costo del viaje para saber cuándo debió salir de u
        curr_time -= weight
        # Guardamos el tiempo de visita para el nodo u
        node_times[u] = curr_time
        
    # Retorna el mapa {nodo: tiempo_relativo} (todos los tiempos antes del destino serán negativos)
    return node_times

def get_edge_intervals_backwards(path: Path, graph: GridGraph) -> List[EdgeInterval]:
    """
    Calcula los intervalos de tiempo en los que se recorre cada arista (calle).
    Retorna una lista de tuplas: (arista_normalizada, t_inicio, t_fin)
    Donde arista_normalizada es una tupla ordenada de los dos nodos.
    """
    # Lista para almacenar los intervalos de tiempo de cada arista transitada
    intervals: List[EdgeInterval] = []
    # El tiempo al llegar al destino final se define como 0
    curr_time = 0
    # Obtiene el mapa de adyacencia del grafo
    adjacency_map = graph.to_adjacency_map()
    
    # Retrocedemos en el camino: desde el penúltimo nodo hasta el inicial
    for i in range(len(path) - 2, -1, -1):
        u = path[i]        # Nodo de salida en el sentido directo
        v = path[i+1]      # Nodo de llegada en el sentido directo
        # Peso/tiempo de tránsito por esta calle
        weight = adjacency_map[u][v]
        # El tránsito inicia a las (tiempo de llegada v - duración weight)
        t_start = curr_time - weight
        # El tránsito termina a las (tiempo de llegada v)
        t_end = curr_time
        
        # Ordenamos los nodos para representar la arista de forma no dirigida (normalizada)
        sorted_nodes = sorted([u, v])
        edge: Edge = (sorted_nodes[0], sorted_nodes[1])
        # Guardamos el intervalo de la arista en la lista
        intervals.append((edge, t_start, t_end))
        # Actualizamos el tiempo actual al momento de salida de u para la siguiente cuadra hacia atrás
        curr_time -= weight
        
    # Retorna la lista de intervalos de tiempo por arista
    return intervals

def check_conflict(path_j: Path, cost_j: int, path_a: Path, cost_a: int, graph: GridGraph) -> bool:
    """
    Verifica si existen conflictos de cruce físico o temporal entre las dos rutas.
    Alinea la llegada al destino común a las 12:00 (o tiempo final = 0).
    
    Returns:
        bool: True si hay conflicto, False si no hay conflicto.
    """
    # 1. Conflicto de Vértice (estar en la misma intersección al mismo tiempo)
    # Obtenemos los tiempos de visita a cada nodo para Javier
    times_j = get_node_times_backwards(path_j, cost_j, graph)
    # Obtenemos los tiempos de visita a cada nodo para Andreína
    times_a = get_node_times_backwards(path_a, cost_a, graph)
    
    # El destino final común no cuenta como conflicto porque allí es donde deben encontrarse
    destination = path_j[-1]
    
    # Iteramos por cada nodo visitado por Javier
    for node in times_j:
        # Si no es el destino, y Andreína también pasa por ese nodo:
        if node != destination and node in times_a:
            # Comparamos si coinciden en el nodo al mismo tiempo absoluto (diferencia insignificante)
            if abs(times_j[node] - times_a[node]) < 0.001:
                return True # Conflicto detectado
                
    # 2. Conflicto de Arista (caminar por la misma cuadra/calle en intervalos de tiempo superpuestos)
    # Obtenemos los intervalos de tiempo en las calles para Javier
    edges_j = get_edge_intervals_backwards(path_j, graph)
    # Obtenemos los intervalos de tiempo en las calles para Andreína
    edges_a = get_edge_intervals_backwards(path_a, graph)
    
    # Comparamos cada calle transitada por Javier con cada calle transitada por Andreína
    for edge_j, start_j, end_j in edges_j:
        for edge_a, start_a, end_a in edges_a:
            # Si coinciden en la misma calle (sin importar la dirección):
            if edge_j == edge_a:
                # Comprobamos si sus intervalos de tránsito se solapan en el tiempo
                if max(start_j, start_a) < min(end_j, end_a):
                    return True # Conflicto detectado (caminan juntos o se cruzan en la calle)
                    
    # Si no se detectó ningún tipo de conflicto, las rutas son compatibles
    return False

def find_optimal_paths(graph: GridGraph, start_j: Node, start_a: Node, destination: Node) -> Optional[Dict[str, Any]]:
    """
    Encuentra las rutas óptimas para Javier y Andreína que minimizan el costo total
    sin conflictos temporales ni espaciales (sin caminar juntos).
    Utiliza una búsqueda por incremento gradual de costo (Iterative Deepening cost search).
    """
    # 1. Obtener costos mínimos individuales mediante el algoritmo de Dijkstra
    _, min_cost_j = dijkstra(graph, start_j, destination)
    _, min_cost_a = dijkstra(graph, start_a, destination)
    
    # Si alguno de los dos no tiene un camino disponible hacia el destino, retornamos None
    if min_cost_j == float('inf') or min_cost_a == float('inf'):
        return None
        
    # Inicializar límites de búsqueda de costo para cada persona con su costo mínimo individual
    limit_j = int(min_cost_j)
    limit_a = int(min_cost_a)
    
    # Número máximo de iteraciones para expandir el costo buscando soluciones viables
    max_iterations = 10
    iteration = 0
    
    # Bucle de incremento de costo (Iterative Deepening)
    while iteration < max_iterations:
        # Encontrar todos los caminos posibles dentro de los límites de costo actuales para Javier y Andreína
        paths_j = find_all_paths(graph, start_j, destination, limit_j)
        paths_a = find_all_paths(graph, start_a, destination, limit_a)
        
        # Generar todos los pares posibles (combinaciones) de caminos
        candidates: List[Tuple[Path, int, Path, int]] = []
        for p_j, c_j in paths_j:
            for p_a, c_a in paths_a:
                candidates.append((p_j, c_j, p_a, c_a))
                
        # Ordenar los pares candidatos por la suma de sus costos acumulados (menor costo combinado primero)
        candidates.sort(key=lambda x: x[1] + x[3])
        
        # Verificar secuencialmente cada combinación candidata de menor a mayor costo total
        for p_j, c_j, p_a, c_a in candidates:
            # Si no hay conflicto entre las rutas, encontramos el par de caminos óptimo
            if not check_conflict(p_j, c_j, p_a, c_a, graph):
                # Retornamos las rutas y sus respectivos costos individuales
                return {
                    "javier": {"path": p_j, "cost": c_j},
                    "andreina": {"path": p_a, "cost": c_a}
                }
                
        # Si ninguna combinación en este rango de costos está libre de conflictos, incrementamos el límite
        limit_j += 2 # Aumenta el límite de Javier para explorar rutas ligeramente más largas
        limit_a += 2 # Aumenta el límite de Andreína para explorar rutas ligeramente más largas
        iteration += 1 # Pasamos a la siguiente iteración
        
    # Si tras 10 iteraciones no se encuentra un conjunto de rutas libre de conflictos, retornamos None
    return None
