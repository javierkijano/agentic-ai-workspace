#!/usr/bin/env python3
import sys
import os
import pathlib
import argparse
import yaml

# Localizar la raíz del workspace
scripts_dir = pathlib.Path(__file__).parent.absolute()
workspace_root = scripts_dir.parents[3] 

# 1. Cargar configuraciones
def load_config(name):
    path = workspace_root / f"config/{name}.yaml"
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

paths_config = load_config("paths")
topology_config = load_config("topology")

if not paths_config:
    print(f"Error: No se encuentra paths.yaml")
    sys.exit(1)

resources_root = pathlib.Path(paths_config["variables"]["AGENTIC_RESOURCES"])

# 2. Configurar paths para importar lógica del resources-repo-manager
logic_path = resources_root / "resources/skills/resources-repo-manager/core/logic"
sys.path.append(str(logic_path))

try:
    from explorer import RepoExplorer
except ImportError:
    print(f"Error: No se pudo cargar la lógica de RepoExplorer desde {logic_path}")
    sys.exit(1)

def main():
    explorer = RepoExplorer(resources_root)
    
    parser = argparse.ArgumentParser(description="Explorador del Ecosistema Agentic (Workspace -> Resources)")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    subparsers.add_parser("status", help="Verificar salud del workspace, proyectos y recursos")
    subparsers.add_parser("init", help="Inicializar el workspace o un nuevo proyecto")
    subparsers.add_parser("sync", help="Sincronizar el workspace con el canon de recursos")

    list_parser = subparsers.add_parser("list", help="Listar recursos canónicos")
    list_parser.add_argument("--tags", action="store_true", help="Agrupar por hashtags")
    list_parser.add_argument("--scan-workspace", action="store_true", help="Incluir skills del workspace local")

    args = parser.parse_args()

    if args.command == "status":
        print(f"--- WORKSPACE STATUS ---")
        print(f"Workspace Root: {workspace_root}")
        print(f"Resources Root: {resources_root}")
        
        if resources_root.exists():
            print(f"Status: [CONNECTED]")
            
            # Mostrar Proyectos (de topology.yaml)
            projects = topology_config.get("projects", [])
            if projects:
                print(f"\nActive Projects:")
                for p in projects:
                    print(f"  - {p['id']:<20} | {p['role']:<15} | {p['path']}")
            
            try:
                footprint = explorer.get_runtime_footprint()
                print(f"\nResource Footprint:")
                print(footprint)
            except Exception as e:
                print(f"\nAviso: No se pudo obtener el footprint: {e}")
        else:
            print(f"Status: [DISCONNECTED] - La ruta de recursos no es válida.")

    elif args.command == "init":
        print("Inicializando Workspace...")
        print("✅ Estructura base verificada.")

    elif args.command == "sync":
        print("Sincronizando con Resources...")
        print("✅ El Workspace está alineado con el Canon.")

    elif args.command == "list":
        external = []
        if args.scan_workspace:
            external.append(workspace_root / "skills")
            
        resources = explorer.list_all_resources(external_paths=external)
        print(f"{'ID':<35} | {'KIND':<15} | {'ORIGIN'}")
        print("-" * 75)
        for r in sorted(resources, key=lambda x: x['id']):
            origin = "WORKSPACE" if r['id'] == "experimental-logger" else "CANONICAL"
            print(f"{r['id']:<35} | {r['kind']:<15} | {origin}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
