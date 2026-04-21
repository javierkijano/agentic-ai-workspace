#!/usr/bin/env python3
import sys
import argparse
import os
import json

# Ajustar path para importar modules locales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.logic.ingestor import Ingestor

DB_PATH = os.path.join(os.path.dirname(__file__), '../core/data/memory.db')

def main():
    parser = argparse.ArgumentParser(description="Ingerir texto en la memoria-grafo")
    parser.add_argument("text", type=str, help="Texto a ingerir (o ruta a archivo si usas cat | ... y lees desde stdin. Para simplificar MVP, pasamos string)")
    parser.add_argument("--source", type=str, default="cli", help="Origen del texto")
    parser.add_argument("--title", type=str, default="", help="Título opcional del documento")
    
    args = parser.parse_args()
    
    # Manejo simple de stdin si 'text' es "-"
    input_text = args.text
    if input_text == "-":
        input_text = sys.stdin.read()
        
    ingestor = Ingestor(DB_PATH)
    meta = {"title": args.title} if args.title else {}
    doc_id = ingestor.ingest(input_text, source=args.source, context_metadata=meta)
    
    if doc_id:
        print(json.dumps({"status": "success", "doc_id": doc_id}))
    else:
        print(json.dumps({"status": "failed", "error": "No text provided"}))

if __name__ == "__main__":
    main()
