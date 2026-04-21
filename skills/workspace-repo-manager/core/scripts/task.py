#!/usr/bin/env python3
import sys
import os
import pathlib
import subprocess
import argparse

# Configuración por defecto
WORKSPACE_DIR = pathlib.Path.home() / "hermes-workspace"

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {e.stderr}")
        sys.exit(1)

def open_task(repo_path, task_id):
    repo_path = pathlib.Path(repo_path).absolute()
    if not repo_path.exists():
        print(f"Error: El repositorio {repo_path} no existe.")
        return

    task_name = f"task-{task_id}"
    target_path = WORKSPACE_DIR / repo_path.name / task_name
    
    print(f"Abriendo tarea '{task_id}' en {repo_path.name}...")
    
    # Crear rama y worktree
    run_command(f"git worktree add -b {task_name} {target_path}", cwd=repo_path)
    
    print(f"\n✅ Tarea abierta con éxito.")
    print(f"📂 Ubicación del Worktree: {target_path}")
    print(f"🌿 Rama: {task_name}")
    print(f"\nComando para entrar: cd {target_path}")

def close_task(repo_path, task_id):
    repo_path = pathlib.Path(repo_path).absolute()
    task_name = f"task-{task_id}"
    target_path = WORKSPACE_DIR / repo_path.name / task_name
    
    if not target_path.exists():
        print(f"Error: No se encontró el worktree en {target_path}")
        return

    print(f"Cerrando tarea '{task_id}'...")
    
    # Eliminar worktree
    run_command(f"git worktree remove {target_path}", cwd=repo_path)
    
    print(f"✅ Tarea cerrada y worktree eliminado.")

def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas Agentic (Git Worktrees)")
    subparsers = parser.add_subparsers(dest="command", help="Comandos")

    # Comando: open
    open_parser = subparsers.add_parser("open", help="Abrir una nueva tarea (crear worktree)")
    open_parser.add_argument("repo", help="Ruta al clone base o ID del proyecto")
    open_parser.add_argument("id", help="ID descriptivo de la tarea")

    # Comando: close
    close_parser = subparsers.add_parser("close", help="Cerrar una tarea (eliminar worktree)")
    close_parser.add_argument("repo", help="Ruta al clone base o ID del proyecto")
    close_parser.add_argument("id", help="ID de la tarea a cerrar")

    args = parser.parse_args()

    if args.command == "open":
        open_task(args.repo, args.id)
    elif args.command == "close":
        close_task(args.repo, args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
