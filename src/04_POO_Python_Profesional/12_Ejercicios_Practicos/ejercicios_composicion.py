# ejercicios_composicion.py

"""
EJERCICIOS DE COMPOSICIÓN
=========================

Objetivo:
---------
Practicar el principio de composición frente a herencia.
Aprender a "tener un" en lugar de "ser un" y diseñar sistemas más flexibles
y desacoplados, tal como se usa en backends y servicios reales.

1️⃣ Ejercicio 1: Composición básica
-----------------------------------
- Crear una clase Motor con un método encender() que imprima "Motor encendido"
- Crear una clase Coche que tenga un atributo motor de tipo Motor
- Método conducir() de Coche debe llamar a motor.encender() y luego imprimir "Coche en movimiento"

2️⃣ Ejercicio 2: Composición con múltiples componentes
------------------------------------------------------
- Crear clase Rueda con método inflar()
- La clase Coche debe tener 4 ruedas (lista de Rueda) y un motor
- Método mantenimiento() de Coche debe inflar todas las ruedas

3️⃣ Ejercicio 3: Integración con un mini backend
-------------------------------------------------
- Crear clase ServicioMantenimiento con método ejecutar(coche)
- Este método debe llamar a coche.mantenimiento() y registrar la acción
- Crear una lista de coches y ejecutar mantenimiento sobre todos usando ServicioMantenimiento

4️⃣ Ejercicio 4: Refactor de herencia a composición
---------------------------------------------------
- Imagina que tenías clase Vehiculo -> Coche heredaba de Vehiculo
- Refactorízalo para que Coche no herede de Vehiculo, sino que tenga un motor y ruedas como composición
- Observa cómo es más flexible añadir nuevos tipos de vehículos sin cambiar la jerarquía

Consejo para tu caso:
---------------------
- Siempre piensa en términos de "tiene un" para servicios, repositorios y componentes de backend.
- Evita jerarquías rígidas, favorece la reutilización y la extensibilidad.
- Practica con ejemplos que simulen tu futuro entorno en aplicaciones y pipelines.
"""
