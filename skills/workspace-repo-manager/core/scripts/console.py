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
menu_path = resources_root / "resources/skills/resources-repo-manager/core/cli/menu.py"

if __name__ == "__main__":
    if not menu_path.exists():
        print(f"Error: No se encuentra el menú canónico en {menu_path}")
        sys.exit(1)
    os.system(f"python3 {menu_path}")
