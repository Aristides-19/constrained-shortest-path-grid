import sys
from typing import List, Optional
from rich import print
from src.utils import load_config, save_config, format_time
from src.graph import GridGraph
from src.algorithms import find_optimal_paths
from src.visualization import draw_routes
from src.types import Config, Node, Path

def print_header() -> None:
    print("[bold magenta]==================================================[/bold magenta]")
    print("[bold white]   PROYECTO: JAVIER Y ANDREÍNA EN BOGOTÁ          [/bold white]")
    print("[bold magenta]==================================================[/bold magenta]\n")

def display_menu(config: Config) -> List[str]:
    print("[bold cyan]Seleccione el destino de encuentro:[/bold cyan]")
    
    establishments = config["establishments"]
    options = list(establishments.keys())
    
    for idx, name in enumerate(options, 1):
        loc = establishments[name]
        print(f" [bold green]{idx}.[/bold green] {name} (Calle {loc['calle']}, Carrera {loc['carrera']})")
        
    print(f" [bold green]{len(options) + 1}.[/bold green] Agregar y buscar destino personalizado")
    print(f" [bold green]{len(options) + 2}.[/bold green] Salir")
    print()
    return options

def handle_custom_destination(config: Config) -> Optional[str]:
    print("\n[bold yellow]--- AGREGAR DESTINO PERSONALIZADO ---[/bold yellow]")
    
    # Validar límites de la cuadrícula
    calle_min = config["grid_limits"]["calle_min"]
    calle_max = config["grid_limits"]["calle_max"]
    carrera_min = config["grid_limits"]["carrera_min"]
    carrera_max = config["grid_limits"]["carrera_max"]
    
    # Nombre del establecimiento
    name = input("Ingrese el nombre del nuevo establecimiento: ").strip()
    if not name:
        name = "Establecimiento Personalizado"
        
    # Obtener Calle
    try:
        calle = int(input(f"Ingrese la Calle ({calle_min} - {calle_max}): "))
        if not (calle_min <= calle <= calle_max):
            print(f"[bold red]Error: La Calle debe estar entre {calle_min} y {calle_max}.[/bold red]")
            return None
    except ValueError:
        print("[bold red]Error: Debe ingresar un número entero.[/bold red]")
        return None
        
    # Obtener Carrera
    try:
        carrera = int(input(f"Ingrese la Carrera ({carrera_min} - {carrera_max}): "))
        if not (carrera_min <= carrera <= carrera_max):
            print(f"[bold red]Error: La Carrera debe estar entre {carrera_min} y {carrera_max}.[/bold red]")
            return None
    except ValueError:
        print("[bold red]Error: Debe ingresar un número entero.[/bold red]")
        return None
        
    # Añadir a la configuración y guardar en JSON para persistir
    config["establishments"][name] = {"calle": calle, "carrera": carrera}
    save_config(config)
    print(f"[bold green]✓ '{name}' guardado correctamente en la configuración.[/bold green]\n")
    return name

def format_path_str(path: Path) -> str:
    return " -> ".join([f"(C{c}, K{k})" for c, k in path])

def process_routing(graph: GridGraph, config: Config, dest_name: str) -> None:
    dest_loc = config["establishments"][dest_name]
    destination: Node = (dest_loc["calle"], dest_loc["carrera"])
    
    start_j: Node = (config["start_locations"]["Javier"]["calle"], config["start_locations"]["Javier"]["carrera"])
    start_a: Node = (config["start_locations"]["Andreina"]["calle"], config["start_locations"]["Andreina"]["carrera"])
    
    print(f"\n[bold yellow]Calculando rutas libres de conflictos hacia {dest_name} {destination}...[/bold yellow]")
    
    result = find_optimal_paths(graph, start_j, start_a, destination)
    
    if not result:
        print("[bold red]No se pudo encontrar una combinación de rutas válida sin conflictos.[/bold red]\n")
        return
        
    path_j = result["javier"]["path"]
    cost_j = result["javier"]["cost"]
    
    path_a = result["andreina"]["path"]
    cost_a = result["andreina"]["cost"]
    
    # Mostrar resultados
    print("\n[bold green]==================================================[/bold green]")
    print("[bold white]                  RESULTADOS                     [/bold white]")
    print("[bold green]==================================================[/bold green]")
    
    print(f"\n[bold blue]Javier:[/bold blue]")
    print(f"  • Ruta: [cyan]{format_path_str(path_j)}[/cyan]")
    print(f"  • Tiempo de caminata: [yellow]{format_time(cost_j)}[/yellow]")
    
    print(f"\n[bold magenta]Andreína:[/bold magenta]")
    print(f"  • Ruta: [cyan]{format_path_str(path_a)}[/cyan]")
    print(f"  • Tiempo de caminata: [yellow]{format_time(cost_a)}[/yellow]")
    
    print("\n[bold yellow]Instrucciones de Salida:[/bold yellow]")
    if cost_j == cost_a:
        print("  • Ambos tienen el mismo tiempo de caminata. [bold green]Deben salir al mismo tiempo[/bold green].")
    elif cost_j > cost_a:
        diff = cost_j - cost_a
        print(f"  • Javier camina más tiempo. [bold blue]Javier debe salir primero[/bold blue].")
        print(f"  • Andreína debe salir [bold yellow]{format_time(diff)}[/bold yellow] después que Javier.")
    else:
        diff = cost_a - cost_j
        print(f"  • Andreína camina más tiempo. [bold magenta]Andreína debe salir primero[/bold magenta].")
        print(f"  • Javier debe salir [bold yellow]{format_time(diff)}[/bold yellow] después que Andreína.")
        
    print("\n[bold cyan]Generando visualización del mapa...[/bold cyan]")
    filename = "routes_map.png"
    draw_routes(graph, path_j, path_a, destination, filename=filename)
    print(f"[bold green]✓ Mapa guardado correctamente en: [white underline]{filename}[/white underline][/bold green]")
    print("[bold green]==================================================[/bold green]\n")

def main() -> None:
    print_header()
    
    # Cargar configuración e inicializar grafo
    config = load_config()
    graph = GridGraph(config)
    
    while True:
        options = display_menu(config)
        choice_str = input("Seleccione una opción: ").strip()
        
        if not choice_str.isdigit():
            print("[bold red]Por favor ingrese un número válido.[/bold red]\n")
            continue
            
        choice = int(choice_str)
        
        if 1 <= choice <= len(options):
            dest_name = options[choice - 1]
            process_routing(graph, config, dest_name)
            
        elif choice == len(options) + 1:
            new_dest_name = handle_custom_destination(config)
            if new_dest_name:
                # Recargar el grafo para incluir el nuevo destino
                graph = GridGraph(config)
                process_routing(graph, config, new_dest_name)
                
        elif choice == len(options) + 2:
            print("\n[bold green]Saliendo...[/bold green]")
            sys.exit(0)
        else:
            print("[bold red]Opción fuera de rango.[/bold red]\n")

if __name__ == "__main__":
    main()
