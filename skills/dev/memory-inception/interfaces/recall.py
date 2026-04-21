#!/usr/bin/env python3
import sys
import argparse
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.logic.retriever import Retriever

DB_PATH = os.path.join(os.path.dirname(__file__), '../core/data/memory.db')

def main():
    parser = argparse.ArgumentParser(description="Recuperar contexto de la memoria")
    parser.add_argument("query", type=str, help="Consulta de texto")
    parser.add_argument("--limit", type=int, default=5, help="Límite de anclajes")
    parser.add_argument("--hops", type=int, default=1, help="Saltos topológicos a explorar")
    
    args = parser.parse_args()
    
    retriever = Retriever(DB_PATH)
    result = retriever.search_and_expand(args.query, limit=args.limit, hops=args.hops)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
