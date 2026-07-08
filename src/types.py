from typing import TypedDict, Dict, Tuple, List

Node = Tuple[int, int]
Edge = Tuple[Node, Node]
Path = List[Node]
EdgeInterval = Tuple[Edge, int, int]

class GridLimits(TypedDict):
    calle_min: int
    calle_max: int
    carrera_min: int
    carrera_max: int

class SpecialWeights(TypedDict):
    carreras: Dict[str, int]
    calles: Dict[str, int]

class Coordinate(TypedDict):
    calle: int
    carrera: int

class StartLocations(TypedDict):
    Javier: Coordinate
    Andreina: Coordinate

class Config(TypedDict):
    grid_limits: GridLimits
    default_weight: int
    special_weights: SpecialWeights
    start_locations: StartLocations
    establishments: Dict[str, Coordinate]
