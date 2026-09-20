import sqlite3
import datetime
from typing import List, Dict, Any, Optional
from config.settings import SQLITE_DB_PATH

class AuditLogger:
    def __init__(self, db_path: str = str(SQLITE_DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_request TEXT NOT NULL,
                    selected_agent TEXT NOT NULL,
                    routing_reason TEXT,
                    documents_accessed TEXT NOT NULL,
                    status TEXT NOT NULL,
                    execution_time_ms REAL NOT NULL
                )
            """)
            conn.commit()

    def log_event(
        self,
        user_request: str,
        selected_agent: str,
        routing_reason: str,
        documents_accessed: List[str],
        status: str,
        execution_time_ms: float
    ) -> int:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        docs_str = ", ".join(documents_accessed) if documents_accessed else "None"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_logs 
                (timestamp, user_request, selected_agent, routing_reason, documents_accessed, status, execution_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, user_request, selected_agent, routing_reason, docs_str, status, execution_time_ms))
            conn.commit()
            return cursor.lastrowid

    def get_all_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM audit_logs 
                ORDER BY id DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def clear_logs(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM audit_logs")
            conn.commit()
