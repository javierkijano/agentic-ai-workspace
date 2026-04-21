import sqlite3
import json
from datetime import datetime
import uuid
import os

class GraphCore:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    source TEXT,
                    status TEXT,
                    metadata TEXT,
                    surface_text TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS edges (
                    id TEXT PRIMARY KEY,
                    from_node_id TEXT NOT NULL,
                    to_node_id TEXT NOT NULL,
                    relation_label TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    source TEXT,
                    metadata TEXT,
                    FOREIGN KEY (from_node_id) REFERENCES nodes (id),
                    FOREIGN KEY (to_node_id) REFERENCES nodes (id)
                )
            ''')
            # Indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_node_label ON nodes(label)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_edge_from ON edges(from_node_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_edge_to ON edges(to_node_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_edge_relation ON edges(relation_label)')

            # FTS for text search
            self.conn.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
                    id UNINDEXED,
                    label,
                    surface_text,
                    content="nodes",
                    content_rowid="rowid"
                )
            ''')
            # Triggers to keep FTS updated
            self.conn.executescript('''
                CREATE TRIGGER IF NOT EXISTS nodes_ai AFTER INSERT ON nodes BEGIN
                    INSERT INTO nodes_fts(rowid, id, label, surface_text) 
                    VALUES (new.rowid, new.id, new.label, new.surface_text);
                END;
                CREATE TRIGGER IF NOT EXISTS nodes_ad AFTER DELETE ON nodes BEGIN
                    INSERT INTO nodes_fts(nodes_fts, rowid, id, label, surface_text) 
                    VALUES ('delete', old.rowid, old.id, old.label, old.surface_text);
                END;
                CREATE TRIGGER IF NOT EXISTS nodes_au AFTER UPDATE ON nodes BEGIN
                    INSERT INTO nodes_fts(nodes_fts, rowid, id, label, surface_text) 
                    VALUES ('delete', old.rowid, old.id, old.label, old.surface_text);
                    INSERT INTO nodes_fts(rowid, id, label, surface_text) 
                    VALUES (new.rowid, new.id, new.label, new.surface_text);
                END;
            ''')

    def add_node(self, label, surface_text=None, source=None, status="active", metadata=None, node_id=None):
        node_id = node_id or str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        metadata_str = json.dumps(metadata) if metadata else "{}"
        
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO nodes (id, label, created_at, updated_at, source, status, metadata, surface_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (node_id, label, now, now, source, status, metadata_str, surface_text))
        return node_id

    def add_edge(self, from_id, to_id, relation_label, source=None, metadata=None, edge_id=None):
        edge_id = edge_id or str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        metadata_str = json.dumps(metadata) if metadata else "{}"
        
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO edges (id, from_node_id, to_node_id, relation_label, created_at, source, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (edge_id, from_id, to_id, relation_label, now, source, metadata_str))
        return edge_id

    def get_node(self, node_id):
        cursor = self.conn.execute('SELECT * FROM nodes WHERE id = ?', (node_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_nodes(self, query, limit=10):
        cursor = self.conn.execute('''
            SELECT id, label, surface_text 
            FROM nodes_fts 
            WHERE nodes_fts MATCH ? 
            ORDER BY rank 
            LIMIT ?
        ''', (query, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_neighborhood(self, node_id, hops=1):
        # A simple BFS for 1 or 2 hops
        visited_nodes = set([node_id])
        queue = [node_id]
        edges = []
        
        for _ in range(hops):
            next_queue = []
            for n_id in queue:
                # Outgoing
                cursor = self.conn.execute('SELECT * FROM edges WHERE from_node_id = ?', (n_id,))
                for row in cursor.fetchall():
                    edge = dict(row)
                    edges.append(edge)
                    if edge['to_node_id'] not in visited_nodes:
                        visited_nodes.add(edge['to_node_id'])
                        next_queue.append(edge['to_node_id'])
                # Incoming
                cursor = self.conn.execute('SELECT * FROM edges WHERE to_node_id = ?', (n_id,))
                for row in cursor.fetchall():
                    edge = dict(row)
                    edges.append(edge)
                    if edge['from_node_id'] not in visited_nodes:
                        visited_nodes.add(edge['from_node_id'])
                        next_queue.append(edge['from_node_id'])
            queue = next_queue
            
        # Fetch all visited nodes
        nodes = []
        for n_id in visited_nodes:
            node = self.get_node(n_id)
            if node:
                nodes.append(node)
                
        return {"nodes": nodes, "edges": edges}
    
    def close(self):
        self.conn.close()
