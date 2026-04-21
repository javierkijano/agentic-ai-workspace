# Memory Inception (Dev)

Skill experimental de memoria operativa y evolutiva basada en grafos relacionales y metaconceptos.

## Arquitectura
- **Graph Core (SQLite)**: Base de datos embebida con soporte para grafos (Nodes, Edges) y Full-Text Search (FTS).
- **Ingestor**: Trocea documentos y genera nodos/fragmentos, extrayendo conceptos heurísticamente.
- **Retriever**: Realiza búsquedas híbridas (FTS + Expansión Topológica por saltos).

## Interfaces (CLI)
- `remember.py <text>`: Ingiere texto nuevo.
- `recall.py <query>`: Recupera subgrafo de contexto.
- `inspect.py <node_id>`: Inspecciona vecindad.
- `bootstrap.py`: Inicializa la ontología con el corpus semilla.
