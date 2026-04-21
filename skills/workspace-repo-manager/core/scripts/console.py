#!/usr/bin/env python3
import os
import sys
import pathlib

# Encontrar el path absoluto del menú
current_dir = pathlib.Path(__file__).parent
menu_path = current_dir.parent / "resources/skills/repository-manager/core/cli/menu.py"

if __name__ == "__main__":
    os.system(f"python3 {menu_path}")
