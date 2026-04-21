#!/usr/bin/env python3
import sys
import argparse
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.logic.graph_core import GraphCore

DB_PATH = os.path.join(os.path.dirname(__file__), '../core/data/memory.db')

def main():
    parser = argparse.ArgumentParser(description="Inspeccionar la vecindad de un nodo específico")
    parser.add_argument("node_id", type=str, help="ID del nodo a inspeccionar")
    parser.add_argument("--hops", type=int, default=1, help="Saltos topológicos")
    
    args = parser.parse_args()
    
    graph = GraphCore(DB_PATH)
    
    # Check if node exists first
    node = graph.get_node(args.node_id)
    if not node:
        print(json.dumps({"error": f"Node {args.node_id} not found."}))
        return
        
    result = graph.get_neighborhood(args.node_id, hops=args.hops)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
