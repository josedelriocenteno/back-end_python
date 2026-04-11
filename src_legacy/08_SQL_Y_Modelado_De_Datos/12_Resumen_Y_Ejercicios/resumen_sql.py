"""
RESUMEN DEL TEMA 08: SQL Y MODELADO DE DATOS PARA BACKEND
-----------------------------------------------------------------------------
Este archivo condensa los conceptos clave que un desarrollador de Python debe 
dominar para trabajar con bases de datos relacionales a nivel profesional.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class SQLMastery:
    topic: str
    key_takeaway: str
    pro_tip: str

summary_points = [
    SQLMastery(
        topic="DDL (Estructura)",
        key_takeaway="Diseña tipos de datos precisos (NUMERIC para dinero, UUID para IDs).",
        pro_tip="Las constraints (NOT NULL, UNIQUE, CHECK) son tu última línea de defensa."
    ),
    SQLMastery(
        topic="DML (Manipulación)",
        key_takeaway="SELECT explícito, RETURNING para capturar IDs y UPSERT para evitar errores.",
        pro_tip="Un UPDATE o DELETE sin WHERE es un error inadmisible en producción."
    ),
    SQLMastery(
        topic="Consultas Avanzadas",
        key_takeaway="Domina JOINs, Subqueries y Window Functions para analítica.",
        pro_tip="Usa CTEs (WITH) para que tus queries complejas sean legibles y mantenibles."
    ),
    SQLMastery(
        topic="Modelado de Datos",
        key_takeaway="Normaliza hasta 3NF para evitar redundancia e inconsistencia.",
        pro_tip="Desnormaliza solo tras medir el rendimiento real con EXPLAIN ANALYZE."
    ),
    SQLMastery(
        topic="Índices y Rendimiento",
        key_takeaway="Los índices aceleran lecturas, pero penalizan las escrituras.",
        pro_tip="Usa EXPLAIN ANALYZE para entender cómo Postgres ejecuta tus consultas."
    ),
    SQLMastery(
        topic="SQL desde Python",
        key_takeaway="Usa siempre parámetros (%s) para prevenir SQL Injection.",
        pro_tip="Gestiona las transacciones con context managers (with conn:) para asegurar ACID."
    ),
    SQLMastery(
        topic="PostgreSQL Avanzado",
        key_takeaway="JSONB permite manejar metadatos NoSQL con potencia relacional.",
        pro_tip="Automatiza auditorías con Triggers y extiende el motor con extensiones."
    ),
    SQLMastery(
        topic="Migraciones",
        key_takeaway="Trata tu esquema como código. Versiona todo con Alembic.",
        pro_tip="Prueba siempre el 'downgrade' antes de desplegar en producción."
    )
]

def print_summary():
    print("=== MASTERING SQL FOR BACKEND PYTHON ===\n")
    for p in summary_points:
        print(f"[{p.topic}]")
        print(f"  > Concepto: {p.key_takeaway}")
        print(f"  > Pro Tip:  {p.pro_tip}\n")

if __name__ == "__main__":
    print_summary()
