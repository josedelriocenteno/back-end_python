# ejercicios_patrones.py

"""
EJERCICIOS PATRONES DE DISEÑO
===============================

Objetivo:
---------
Aplicar patrones de diseño básicos en Python para estructuras de backend, 
servicios y lógica de negocio, siguiendo buenas prácticas profesionales.

1️⃣ Ejercicio 1: Factory Pattern
-------------------------------
- Crear una clase abstracta Producto con método info()
- Crear subclases ProductoA y ProductoB
- Crear una fábrica ProductoFactory que devuelva instancias según un parámetro
- Prueba creando distintos productos sin instanciarlos directamente

2️⃣ Ejercicio 2: Singleton Pattern
---------------------------------
- Crear clase Configuracion que solo pueda tener una instancia
- Añadir atributos como ruta_logs, nivel_debug
- Asegúrate que al crear varias instancias, todas apuntan al mismo objeto

3️⃣ Ejercicio 3: Strategy Pattern
--------------------------------
- Crear una clase Contexto que reciba un algoritmo como estrategia
- Crear estrategias para:
  - Ordenar números ascendentes
  - Ordenar números descendentes
  - Filtrar números pares
- Cambia la estrategia en tiempo de ejecución sin modificar Contexto

4️⃣ Ejercicio 4: Repository Pattern
----------------------------------
- Crear clase abstracta Repositorio con métodos add(item), get_all()
- Implementar RepositorioMemoria y RepositorioSQL (simulado)
- El código que usa el repositorio no debe depender de la implementación

5️⃣ Ejercicio 5: Service Layer Pattern
-------------------------------------
- Crear capa de servicios para manejar usuarios:
  - UsuarioService: métodos crear_usuario(), obtener_usuario()
  - Usa Repository para persistencia
- Asegúrate que la lógica de negocio está desacoplada de la persistencia

Consejo para tu caso:
---------------------
- Aplica estos patrones en mini proyectos de backend y pipelines de datos.
- Te ayudará a organizar código para sistemas complejos y escalables.
- Puedes combinarlos: por ejemplo, un Service Layer que use Repository y estrategias.
"""
