from .graph_core import GraphCore
import re

class Ingestor:
    def __init__(self, db_path):
        self.graph = GraphCore(db_path)

    def _normalize(self, text):
        # Basic cleanup: trim spaces, fix multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _chunk_text(self, text):
        # Simple pragmatic chunking by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        chunks = [p.strip() for p in paragraphs if p.strip()]
        return chunks

    def ingest(self, text, source="unknown", context_metadata=None):
        text = self._normalize(text)
        chunks = self._chunk_text(text)
        if not chunks:
            return None

        # Create a document/root node for this ingestion
        doc_label = "Document"
        if context_metadata and "title" in context_metadata:
            doc_label = f"Document: {context_metadata['title']}"

        doc_id = self.graph.add_node(
            label=doc_label,
            surface_text=text,
            source=source,
            metadata=context_metadata
        )

        previous_chunk_id = None
        
        for i, chunk_text in enumerate(chunks):
            # Create node for chunk
            chunk_id = self.graph.add_node(
                label="Fragment",
                surface_text=chunk_text,
                source=source,
                metadata={"order": i, "parent_id": doc_id}
            )
            
            # Relation: Document contains Fragment
            self.graph.add_edge(
                from_id=doc_id,
                to_id=chunk_id,
                relation_label="contains"
            )
            self.graph.add_edge(
                from_id=chunk_id,
                to_id=doc_id,
                relation_label="part_of"
            )

            # Relation: Order (sigue_a)
            if previous_chunk_id:
                self.graph.add_edge(
                    from_id=previous_chunk_id,
                    to_id=chunk_id,
                    relation_label="next"
                )
                self.graph.add_edge(
                    from_id=chunk_id,
                    to_id=previous_chunk_id,
                    relation_label="previous"
                )
            
            previous_chunk_id = chunk_id
            
            # Basic concept extraction: capitalized words (just a pragmatic heuristic for MVP)
            # In later phases, the LM will propose these.
            words = re.findall(r'\b[A-Z][a-z]+\b', chunk_text)
            unique_concepts = set(words)
            
            for concept in unique_concepts:
                # Discard stop-word like short capitalized words (At, The, In, etc)
                if len(concept) < 3:
                    continue
                
                concept_id = self.graph.add_node(
                    label="Concept",
                    surface_text=concept,
                    source="auto_extraction"
                )
                
                # Relation: Fragment mentions Concept
                self.graph.add_edge(
                    from_id=chunk_id,
                    to_id=concept_id,
                    relation_label="mentions"
                )
                
        return doc_id
