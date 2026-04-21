#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.logic.ingestor import Ingestor

DB_PATH = os.path.join(os.path.dirname(__file__), '../core/data/memory.db')

def main():
    ingestor = Ingestor(DB_PATH)
    
    seed_texts = [
        {
            "title": "Definiciones Iniciales",
            "text": "Un sistema es un conjunto de partes interrelacionadas.\n\nUna memoria es la persistencia del estado en un sistema."
        },
        {
            "title": "Relaciones",
            "text": "El tiempo ordena los eventos en secuencias predecibles.\n\nUn metaconcepto agrupa conceptos más simples."
        }
    ]
    
    print("Iniciando Bootstrap Ontológico...")
    for seed in seed_texts:
        print(f"Ingiriendo: {seed['title']}...")
        doc_id = ingestor.ingest(seed["text"], source="bootstrap", context_metadata={"title": seed["title"]})
        print(f"-> OK (Doc ID: {doc_id})")
        
    print("Bootstrap finalizado.")

if __name__ == "__main__":
    main()
