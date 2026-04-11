#!/usr/bin/env python3
"""
Demo completa Tienda Online
Ejecuta: python src/infrastructure/main.py
"""

from infrastructure.repositories.usuario_repository_sqlite import UsuarioRepositorySQLite
from infrastructure.repositories.producto_repository_sqlite import ProductoRepositorySQLite
from infrastructure.database.sqlite_db import db
from application.services.pedido_service import PedidoService
from domain.entities.usuario import Usuario
from domain.entities.producto import Producto
from domain.value_objects.id_value import IDValue
from domain.strategies.descuento_strategy import TipoDescuento

def main():
    print("🚀 Iniciando Tienda Online Demo...")
    
    # Repositories
    usuario_repo = UsuarioRepositorySQLite()
    producto_repo = ProductoRepositorySQLite()
    
    # Service (Dependency Injection)
    service = PedidoService(usuario_repo, producto_repo)
    
    # Demo 1: Crear usuarios/productos
    print("\n1️⃣ Creando datos de prueba...")
    user_id = IDValue['Usuario'].generar()
    usuario = Usuario(
        id=user_id,
        nombre="Ana López",
        email="ana@tienda.com"
    )
    usuario_repo.add(usuario)
    
    prod1 = Producto(
        id=IDValue['Producto'].generar(),
        nombre="Laptop Dell XPS",
        precio=PrecioValue.desde_float(1299.99)
    )
    prod2 = Producto(
        id=IDValue['Producto'].generar(),
        nombre="Mouse Logitech",
        precio=PrecioValue.desde_float(29.99)
    )
    producto_repo.add(prod1)
    producto_repo.add(prod2)
    
    # Demo 2: Crear pedido
    print("\n2️⃣ Creando pedido...")
    pedido = service.crear_pedido(
        usuario_id=user_id,
        productos_ids=[prod1.id, prod2.id],
        tipo_descuento=TipoDescuento.PROMO
    )
    
    # Demo 3: Consultas
    print("\n3️⃣ Consultas...")
    print(f"Usuarios total: {usuario_repo.contar()}")
    print(f"Productos total: {producto_repo.contar()}")
    
    laptop = producto_repo.get(prod1.id)
    print(f"Laptop encontrada: {laptop}")
    
    # Demo 4: Vista previa
    print("\n4️⃣ Vista previa nuevo pedido...")
    total_previo = service.calcular_total_previo(
        user_id, [prod1.id], "premium"
    )
    print(f"Total previo Premium: ${total_previo:.2f}")
    
    print("\n✅ ¡Demo completada!")
    print(f"DB guardada en: {db.db_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Adiós!")
    except Exception as e:
        print(f"❌ Error: {e}")
