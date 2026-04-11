# mini_proyecto_poo.py

"""
MINI PROYECTO POO: GESTIÓN DE USUARIOS Y PEDIDOS
=================================================

Objetivo:
---------
Integrar todo lo aprendido en POO: clases, herencia, composición, 
encapsulación, métodos especiales, patrones de diseño y buenas prácticas.

Escenario:
----------
Un sistema simplificado de e-commerce que gestiona usuarios y pedidos.

Requisitos:
-----------
1️⃣ Clases de Dominio
--------------------
- Usuario:
    - Atributos: id, nombre, email
    - Métodos: __str__, validar_email()
- Producto:
    - Atributos: id, nombre, precio
    - Método: __repr__ para mostrar info
- Pedido:
    - Atributos: id, usuario (Usuario), lista_productos
    - Métodos: total(), agregar_producto(producto)

2️⃣ Patrones y Buenas Prácticas
--------------------------------
- Repository Pattern:
    - UsuarioRepository: add(usuario), get(id)
    - ProductoRepository: add(producto), get(id)
- Service Layer:
    - PedidoService: crear_pedido(usuario_id, productos_ids)
    - Obtener total del pedido y persistirlo
- Strategy Pattern:
    - Estrategia de cálculo de descuento: normal, promo, premium
    - Aplicar descuento al calcular total del pedido

3️⃣ Inmutabilidad y Value Objects
--------------------------------
- Usar dataclasses frozen para Producto
- ID de Usuario y Pedido como Value Objects inmutables

4️⃣ Testing y Mocks
-------------------
- Crear tests para Usuario, Producto, Pedido
- Mockear repositorios para probar PedidoService sin persistencia real

Sugerencias:
------------
- Aplica encapsulación (_protected, __private)
- Implementa métodos especiales (__str__, __repr__, __eq__)
- Usa composición en lugar de herencia donde tenga sentido
- Aplica SOLID: responsabilidades claras, desacoplamiento
- Este mini proyecto debe ser ejecutable y mostrar interacciones:
    - Crear usuarios, productos
    - Crear pedidos y mostrar totales
    - Cambiar estrategia de descuento y recalcular totales
"""
