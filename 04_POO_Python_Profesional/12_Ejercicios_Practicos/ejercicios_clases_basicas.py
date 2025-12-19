# ejercicios_clases_basicas.py

"""
EJERCICIOS DE CLASES BÁSICAS
=============================

Objetivo:
---------
Practicar la definición de clases, atributos de instancia y de clase,
métodos, y comprender cómo modelar entidades simples de manera profesional.

1️⃣ Ejercicio 1: Definir una clase Usuario
-----------------------------------------
- Atributos: nombre, email, edad
- Método: saludo() que devuelva "Hola, soy {nombre}"
- Crear 2 instancias y llamar al método saludo()

2️⃣ Ejercicio 2: Contador de instancias
---------------------------------------
- Añadir un atributo de clase `total_usuarios`
- Incrementarlo en __init__ cada vez que se crea un usuario
- Imprimir `Usuario.total_usuarios` después de crear varias instancias

3️⃣ Ejercicio 3: Métodos de clase y estáticos
---------------------------------------------
- Crear un método de clase `desde_string(cls, data_str)` que reciba "nombre,email,edad"
  y devuelva una instancia de Usuario
- Crear un método estático `validar_email(email)` que devuelva True si contiene "@"

4️⃣ Ejercicio 4: Representación profesional
--------------------------------------------
- Implementar __str__ para que devuelva "Usuario(nombre=..., email=...)"
- Implementar __repr__ para que devuelva "Usuario('nombre', 'email', edad)"

5️⃣ Ejercicio 5: Integración con un mini backend simulado
----------------------------------------------------------
- Crear una clase RepositorioUsuarios que guarde usuarios en una lista interna
- Métodos: agregar(usuario), listar_todos(), buscar_por_email(email)
- Usar las instancias de Usuario anteriores y probar todos los métodos

Consejo para tu caso:
---------------------
- Enfócate en modelar los objetos como si fueran entidades de un proyecto real.
- Piensa en cómo se podrían usar estas clases en un backend real para APIs, validaciones, y almacenamiento de datos.
- Intenta aplicar buenas prácticas de nombres, encapsulación y representaciones claras.
"""
