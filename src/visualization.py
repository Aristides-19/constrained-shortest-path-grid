from typing import List, Tuple, Optional, Dict
import matplotlib.pyplot as plt
import networkx as nx
from src.graph import GridGraph
from src.types import Node, Path, Edge

def draw_routes(
    graph: GridGraph,
    path_j: Optional[Path],
    path_a: Optional[Path],
    destination: Node,
    filename: str = "routes_map.png"
) -> None:
    """
    Dibuja el grafo de la cuadrícula y las rutas calculadas para Javier y Andreína.
    
    Args:
        graph (GridGraph): El grafo.
        path_j (list): Camino de Javier.
        path_a (list): Camino de Andreína.
        destination (tuple): Coordenada de destino.
        filename (str): Nombre de archivo para guardar el mapa.
    """
    # 1. Crear el objeto DiGraph de NetworkX para dibujar flechas de dirección
    G = nx.DiGraph()
    
    # 2. Agregar nodos y definir posiciones geográficas correctas de Bogotá
    # Carrera crece hacia el Oeste (derecha a izquierda en pantalla)
    # Calle crece hacia el Norte (abajo a arriba en pantalla)
    pos: Dict[Node, Tuple[int, int]] = {}
    for node in graph.nodes:
        calle, carrera = node
        x = 15 - carrera # Carrera 15 a la izquierda (x=0), Carrera 10 a la derecha (x=5)
        y = calle - 50   # Calle 50 abajo (y=0), Calle 55 arriba (y=5)
        pos[node] = (x, y)
        G.add_node(node)
        
    # 3. Agregar aristas del mapa
    adjacency_map = graph.to_adjacency_map()
    for u in adjacency_map:
        for v, w in adjacency_map[u].items():
            G.add_edge(u, v, weight=w)
            
    # Configurar el gráfico
    plt.figure(figsize=(10, 8))
    plt.title(f"Rutas de Javier y Andreína hacia {destination}", fontsize=14, fontweight="bold", pad=15)
    
    # 4. Dibujar todas las calles de fondo
    normal_edges: List[Edge] = []
    slow_edges: List[Edge] = []
    
    for u, v, data in G.edges(data=True):
        w = data['weight']
        edge: Edge = (u, v)
        if w > 5:
            slow_edges.append(edge)
        else:
            normal_edges.append(edge)
            
    # Dibujar calles normales (gris claro) y lentas (naranja)
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color="#cccccc", width=2, arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=slow_edges, edge_color="#e67e22", width=3, arrows=False, label="Vía lenta (7-10 min)")
    
    # Dibujar etiquetas de los nodos (ej: "54,14")
    labels: Dict[Node, str] = {node: f"C{node[0]}\nK{node[1]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family="sans-serif")
    
    # Dibujar todos los nodos en un color suave de fondo
    nx.draw_networkx_nodes(G, pos, node_color="#f5f6fa", node_size=600, edgecolors="#718093", linewidths=1.5)

    # 5. Dibujar la ruta de Javier (Azul)
    if path_j:
        edges_j: List[Edge] = [(path_j[i], path_j[i+1]) for i in range(len(path_j)-1)]
        nx.draw_networkx_edges(
            G, pos, edgelist=edges_j, edge_color="#3498db", width=4, 
            arrows=True, arrowstyle="-|>", arrowsize=15, connectionstyle="arc3,rad=0.08"
        )
        
    # 6. Dibujar la ruta de Andreína (Fucsia/Magenta)
    if path_a:
        edges_a: List[Edge] = [(path_a[i], path_a[i+1]) for i in range(len(path_a)-1)]
        nx.draw_networkx_edges(
            G, pos, edgelist=edges_a, edge_color="#e84393", width=4, 
            arrows=True, arrowstyle="-|>", arrowsize=15, connectionstyle="arc3,rad=-0.08"
        )
        
    # 7. Resaltar puntos clave (Origen Javier, Origen Andreína, Destino)
    start_j: Optional[Node] = path_j[0] if path_j else None
    start_a: Optional[Node] = path_a[0] if path_a else None
    
    if start_j:
        nx.draw_networkx_nodes(G, pos, nodelist=[start_j], node_color="#2980b9", node_size=700, edgecolors="#1a5276", linewidths=2)
        plt.plot([], [], 'o', color='#2980b9', markersize=10, label="Origen Javier (C54, K14)")
        
    if start_a:
        nx.draw_networkx_nodes(G, pos, nodelist=[start_a], node_color="#c2185b", node_size=700, edgecolors="#880e4f", linewidths=2)
        plt.plot([], [], 'o', color='#c2185b', markersize=10, label="Origen Andreína (C52, K13)")
        
    nx.draw_networkx_nodes(G, pos, nodelist=[destination], node_color="#27ae60", node_size=800, edgecolors="#1e8449", linewidths=2)
    plt.plot([], [], 'o', color='#27ae60', markersize=10, label="Destino (Encuentro)")

    # Añadir dummy plots para la leyenda de las rutas
    plt.plot([], [], color="#3498db", linewidth=3, label="Ruta Javier")
    plt.plot([], [], color="#e84393", linewidth=3, label="Ruta Andreína")
    plt.plot([], [], color="#e67e22", linewidth=2.5, label="Calles lentas (C51, K11-13)")

    plt.legend(loc="upper left", scatterpoints=1)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.axis("on")
    plt.xlabel("Carreras (Crecen hacia la izquierda)")
    plt.ylabel("Calles (Crecen hacia arriba)")
    
    # Ajustar límites del plot
    plt.xlim(-0.5, 5.5)
    plt.ylim(-0.5, 5.5)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
