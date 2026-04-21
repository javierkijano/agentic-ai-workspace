from .graph_core import GraphCore
import json

class Retriever:
    def __init__(self, db_path):
        self.graph = GraphCore(db_path)

    def search_and_expand(self, query, limit=5, hops=1):
        """
        Recuperación híbrida:
        1. Búsqueda textual (FTS) para anclar nodos base.
        2. Recuperación topológica (vecindad) desde esos anclajes.
        """
        # 1. Recuperar anclajes
        search_results = self.graph.search_nodes(query, limit=limit)
        if not search_results:
            return {"anchors": [], "subgraph": {"nodes": [], "edges": []}}

        # 2. Expandir vecindad
        all_nodes = {}
        all_edges = []
        
        for anchor in search_results:
            subgraph = self.graph.get_neighborhood(anchor['id'], hops=hops)
            for node in subgraph['nodes']:
                all_nodes[node['id']] = node
            for edge in subgraph['edges']:
                all_edges.append(edge)
                
        # Deduplicate edges (basic way)
        unique_edges = []
        seen_edges = set()
        for edge in all_edges:
            if edge['id'] not in seen_edges:
                seen_edges.add(edge['id'])
                unique_edges.append(edge)

        return {
            "anchors": search_results,
            "subgraph": {
                "nodes": list(all_nodes.values()),
                "edges": unique_edges
            }
        }
