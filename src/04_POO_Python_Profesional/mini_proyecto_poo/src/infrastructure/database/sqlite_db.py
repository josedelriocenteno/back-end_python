import sqlite3
import atexit
from contextlib import contextmanager
from typing import Optional, Iterator, Any
from pathlib import Path

class SQLiteDB:
    """Manejador central SQLite con conexión pooling"""
    
    def __init__(self, db_path: str = "tienda.db"):
        self.db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()
        atexit.register(self.close)
    
    def _init_db(self):
        """Inicializa DB y tablas base"""
        with self.get_connection() as conn:
            # Tabla pedidos (base)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id TEXT PRIMARY KEY,
                    usuario_id TEXT NOT NULL,
                    total DECIMAL(10,2),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )
            """)
            conn.commit()
    
    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager conexión thread-safe"""
        if self._conn is None:
            self._conn = sqlite3.connect(
                self.db_path, 
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            self._conn.row_factory = sqlite3.Row
        try:
            yield self._conn
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        # No close aquí (pooling)
    
    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        """Query genérica"""
        with self.get_connection() as conn:
            return conn.execute(query, params).fetchall()
    
    def execute_script(self, script: str):
        """Ejecuta múltiples statements"""
        with self.get_connection() as conn:
            conn.executescript(script)
    
    def close(self):
        """Cierra conexión"""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    @property
    def db_path(self) -> Path:
        return self.db_path
    
    def backup(self, backup_path: str):
        """Backup DB"""
        import shutil
        shutil.copy2(self.db_path, backup_path)

# Singleton global (opcional)
db = SQLiteDB()
