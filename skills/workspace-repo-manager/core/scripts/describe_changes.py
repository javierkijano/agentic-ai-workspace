#!/usr/bin/env python3
import os
import sys
import pathlib
import yaml

# Cargar path de recursos desde la configuración del workspace
scripts_dir = pathlib.Path(__file__).parent.absolute()
workspace_root = scripts_dir.parents[3]
config_path = workspace_root / "config/paths.yaml"

if not config_path.exists():
    print("Error: No se encuentra config/paths.yaml")
    sys.exit(1)

with open(config_path, "r") as f:
    paths = yaml.safe_load(f)

resources_root = pathlib.Path(paths["variables"]["AGENTIC_RESOURCES"])
logic_path = resources_root / "resources/skills/resources-repo-manager/core/logic/describe_changes.py"

if __name__ == "__main__":
    if not logic_path.exists():
        print(f"Error: No se encuentra la lógica canónica en {logic_path}")
        sys.exit(1)
    os.system(f"python3 {logic_path} {' '.join(sys.argv[1:])}")
