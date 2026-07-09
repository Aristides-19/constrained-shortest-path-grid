import unittest
import os
import sys

# Agregar src a la ruta de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_config
from src.graph import GridGraph
from src.algorithms import dijkstra, find_optimal_paths, check_conflict

class TestRoutingProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Utilizar la configuración real
        cls.config = load_config()
        cls.graph = GridGraph(cls.config)

    def test_grid_size(self):
        """Verifica que se generen los 36 nodos en la cuadrícula de 6x6 (Calles 50-55 y Carreras 10-15)."""
        self.assertEqual(len(self.graph.nodes), 36)
        # Verificar extremos
        self.assertIn((50, 10), self.graph.nodes)
        self.assertIn((55, 15), self.graph.nodes)

    def test_weights(self):
        """Verifica que los pesos especiales de calles/carreras se carguen y calculen correctamente."""
        adj_map = self.graph.to_adjacency_map()
        
        # Caso 1: Calle 51 (debe tardar 10 min en recorrerse)
        # Movimiento horizontal por calle 51
        w_calle_51 = adj_map[(51, 14)][(51, 13)]
        self.assertEqual(w_calle_51, 10)
        
        # Caso 2: Carrera 13 (debe tardar 7 min en recorrerse)
        # Movimiento vertical por carrera 13
        w_carrera_13 = adj_map[(54, 13)][(53, 13)]
        self.assertEqual(w_carrera_13, 7)
        
        # Caso 3: Calle normal y Carrera normal
        # Movimiento por calle 54 y carrera 14
        w_normal = adj_map[(54, 14)][(53, 14)] # Carrera 14 (normal)
        self.assertEqual(w_normal, 5)
        
        w_normal_calle = adj_map[(54, 14)][(54, 13)] # Calle 54 (normal)
        self.assertEqual(w_normal_calle, 5)

    def test_dijkstra(self):
        """Verifica el funcionamiento del Dijkstra simple sin restricciones."""
        # Ruta simple para Javier a The Darkness (50, 14) desde (54, 14)
        path, cost = dijkstra(self.graph, (54, 14), (50, 14))
        # Debe ser ir recto hacia el sur por carrera 14: (54,14) -> (53,14) -> (52,14) -> (51,14) -> (50,14)
        expected_path = [(54, 14), (53, 14), (52, 14), (51, 14), (50, 14)]
        self.assertEqual(path, expected_path)
        # 4 tramos normales a 5 min cada uno = 20 min
        self.assertEqual(cost, 20)

    def test_optimal_conflict_free_paths(self):
        """Prueba que el buscador de caminos libres de conflicto encuentre soluciones válidas."""
        start_j = (54, 14)
        start_a = (52, 13)
        destination = (50, 14) # Discoteca The Darkness
        
        result = find_optimal_paths(self.graph, start_j, start_a, destination)
        self.assertIsNotNone(result)
        if not result: return None
        
        path_j = result["javier"]["path"]
        cost_j = result["javier"]["cost"]
        path_a = result["andreina"]["path"]
        cost_a = result["andreina"]["cost"]
        
        # El destino debe ser el final de ambos caminos
        self.assertEqual(path_j[-1], destination)
        self.assertEqual(path_a[-1], destination)
        
        # El origen de ambos debe coincidir
        self.assertEqual(path_j[0], start_j)
        self.assertEqual(path_a[0], start_a)
        
        # Verificar que no exista conflicto temporal ni de arista
        conflict = check_conflict(path_j, cost_j, path_a, cost_a, self.graph)
        self.assertFalse(conflict, "Se detectó un conflicto en las rutas sugeridas.")

if __name__ == '__main__':
    unittest.main()
