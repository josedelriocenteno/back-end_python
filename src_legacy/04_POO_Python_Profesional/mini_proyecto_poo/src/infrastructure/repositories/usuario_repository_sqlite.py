import sqlite3
import uuid
from typing import Optional, List
from contextlib import contextmanager
from application.ports.usuario_repository import UsuarioRepository
from domain.entities.usuario import Usuario
from domain.value_objects.id_value import IDValue

class UsuarioRepositorySQLite(UsuarioRepository):
    def __init__(self, db_path: str = "tienda.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        """Crea tabla si no existe"""
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()
    
    @contextmanager
    def _get_conn(self):
        """Context manager conexión"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Dict-like rows
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add(self, usuario: Usuario) -> None:
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "INSERT INTO usuarios (id, nombre, email) VALUES (?, ?, ?)",
                    (usuario.id.string, usuario.nombre, usuario.email)
                )
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Usuario ya existe: {e}")
    
    def get(self, id: IDValue['Usuario']) -> Usuario:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT id, nombre, email FROM usuarios WHERE id = ?",
                (id.string,)
            ).fetchone()
            
            if not row:
                raise ValueError(f"Usuario no encontrado: {id}")
            
            return Usuario(
                id=IDValue['Usuario'].desde_string(row['id']),
                nombre=row['nombre'],
                email=row['email']
            )
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT id, nombre, email FROM usuarios WHERE email = ?",
                (email,)
            ).fetchone()
            
            if not row:
                return None
            
            return Usuario(
                id=IDValue['Usuario'].desde_string(row['id']),
                nombre=row['nombre'],
                email=row['email']
            )
    
    def update(self, usuario: Usuario) -> None:
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE usuarios SET nombre = ?, email = ? WHERE id = ?",
                (usuario.nombre, usuario.email, usuario.id.string)
            )
            if conn.total_changes == 0:
                raise ValueError(f"Usuario no encontrado: {usuario.id}")
    
    def delete(self, id: IDValue['Usuario']) -> bool:
        with self._get_conn() as conn:
            result = conn.execute(
                "DELETE FROM usuarios WHERE id = ?",
                (id.string,)
            ).rowcount > 0
            return bool(result)
    
    def listar_todos(self) -> List[Usuario]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT id, nombre, email FROM usuarios").fetchall()
            return [
                Usuario(
                    id=IDValue['Usuario'].desde_string(row['id']),
                    nombre=row['nombre'],
                    email=row['email']
                ) for row in rows
            ]
    
    def contar(self) -> int:
        with self._get_conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
