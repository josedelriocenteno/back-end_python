import sqlite3
from typing import List
from contextlib import contextmanager
from application.ports.producto_repository import ProductoRepository
from domain.entities.producto import Producto
from domain.value_objects.id_value import IDValue
from domain.value_objects.precio_value import PrecioValue

class ProductoRepositorySQLite(ProductoRepository):
    def __init__(self, db_path: str = "tienda.db"):
        self.db_path = db_path
        self._crear_tabla()
    
    def _crear_tabla(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL
                )
            """)
            conn.commit()
    
    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add(self, producto: Producto) -> None:
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "INSERT INTO productos (id, nombre, precio) VALUES (?, ?, ?)",
                    (producto.id.string, producto.nombre, str(producto.precio.value))
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"Producto ya existe: {producto.id}")
    
    def get(self, id: IDValue['Producto']) -> Producto:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT id, nombre, precio FROM productos WHERE id = ?",
                (id.string,)
            ).fetchone()
            
            if not row:
                raise ValueError(f"Producto no encontrado: {id}")
            
            return Producto(
                id=IDValue['Producto'].desde_string(row['id']),
                nombre=row['nombre'],
                precio=PrecioValue.desde_string(str(row['precio']))
            )
    
    def get_by_nombre(self, nombre: str, exacto: bool = False) -> List[Producto]:
        with self._get_conn() as conn:
            if exacto:
                query = "SELECT id, nombre, precio FROM productos WHERE nombre = ?"
                rows = conn.execute(query, (nombre,)).fetchall()
            else:
                query = "SELECT id, nombre, precio FROM productos WHERE nombre LIKE ?"
                rows = conn.execute(query, (f"%{nombre}%",)).fetchall()
            
            return [
                Producto(
                    id=IDValue['Producto'].desde_string(row['id']),
                    nombre=row['nombre'],
                    precio=PrecioValue.desde_string(str(row['precio']))
                ) for row in rows
            ]
    
    def update_precio(self, id: IDValue['Producto'], nuevo_precio: PrecioValue) -> Producto:
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE productos SET precio = ? WHERE id = ?",
                (str(nuevo_precio.value), id.string)
            )
            if conn.total_changes == 0:
                raise ValueError(f"Producto no encontrado: {id}")
            return self.get(id)  # Devuelve actualizado
    
    def delete(self, id: IDValue['Producto']) -> bool:
        with self._get_conn() as conn:
            result = conn.execute(
                "DELETE FROM productos WHERE id = ?",
                (id.string,)
            ).rowcount > 0
            return bool(result)
    
    def listar_todos(self) -> List[Producto]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT id, nombre, precio FROM productos").fetchall()
            return [
                Producto(
                    id=IDValue['Producto'].desde_string(row['id']),
                    nombre=row['nombre'],
                    precio=PrecioValue.desde_string(str(row['precio']))
                ) for row in rows
            ]
    
    def listar_activos(self) -> List[Producto]:
        # Asumimos todos activos (sin campo deleted)
        return self.listar_todos()
    
    def contar(self) -> int:
        with self._get_conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
