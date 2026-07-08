from typing import List, Dict
from src.types import Config, GridLimits, SpecialWeights, Node

class GridGraph:
    def __init__(self, config: Config) -> None:
        """
        Inicializa el grafo de la cuadrícula a partir de la configuración.
        
        Args:
            config (Config): Configuración cargada del archivo JSON.
        """
        self.config: Config = config
        self.limits: GridLimits = config["grid_limits"]
        self.default_weight: int = config["default_weight"]
        self.special_weights: SpecialWeights = config["special_weights"]
        
        # Estructura principal interna (Diccionario de Adyacencia / Adjacency Map)
        self.nodes: List[Node] = []
        self.adjacency_map: Dict[Node, Dict[Node, int]] = {}
        
        self._build_graph()

    def _build_graph(self) -> None:
        """Construye dinámicamente los nodos y aristas basados en los límites y restricciones."""
        calle_min = self.limits["calle_min"]
        calle_max = self.limits["calle_max"]
        carrera_min = self.limits["carrera_min"]
        carrera_max = self.limits["carrera_max"]
        
        # 1. Generar todos los nodos (intersecciones)
        # Nodos son tuplas: (calle, carrera)
        for calle in range(calle_min, calle_max + 1):
            for carrera in range(carrera_min, carrera_max + 1):
                node = (calle, carrera)
                self.nodes.append(node)
                self.adjacency_map[node] = {}
        
        # 2. Conectar nodos adyacentes (Cuadrícula perfecta)
        for (calle, carrera) in self.nodes:
            # Posibles vecinos
            neighbors: List[Node] = []
            if calle < calle_max:
                neighbors.append((calle + 1, carrera)) # Norte
            if calle > calle_min:
                neighbors.append((calle - 1, carrera)) # Sur
            if carrera < carrera_max:
                neighbors.append((calle, carrera + 1)) # Oeste
            if carrera > carrera_min:
                neighbors.append((calle, carrera - 1)) # Este
                
            for neighbor in neighbors:
                weight = self._calculate_weight((calle, carrera), neighbor)
                self.adjacency_map[(calle, carrera)][neighbor] = weight

    def _calculate_weight(self, node_from: Node, node_to: Node) -> int:
        """Calcula el tiempo de caminata entre dos intersecciones contiguas."""
        c1, k1 = node_from
        c2, k2 = node_to
        
        # Si nos movemos por una Calle (c1 == c2), caminamos sobre la calle c1
        if c1 == c2:
            calle_str = str(c1)
            special_calles = self.special_weights.get("calles", {})
            if calle_str in special_calles:
                return special_calles[calle_str]
            return self.default_weight
            
        # Si nos movemos por una Carrera (k1 == k2), caminamos sobre la carrera k1
        if k1 == k2:
            carrera_str = str(k1)
            special_carreras = self.special_weights.get("carreras", {})
            if carrera_str in special_carreras:
                return special_carreras[carrera_str]
            return self.default_weight
            
        # Por seguridad de diseño (no debería ocurrir en cuadrícula perfecta de paso simple)
        return self.default_weight

    def to_adjacency_map(self) -> Dict[Node, Dict[Node, int]]:
        """
        Representación del Grafo: Diccionario de Adyacencia (Adjacency Map).
        Estructura: {nodo_origen: {nodo_destino: peso, ...}, ...}
        """
        return self.adjacency_map
