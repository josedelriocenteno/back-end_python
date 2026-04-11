# ejercicios_solid.py

"""
EJERCICIOS PRINCIPIOS SOLID
============================

Objetivo:
---------
Poner en práctica los principios SOLID para escribir código Python profesional,
desacoplado y mantenible, orientado a sistemas backend y futuros proyectos de IA.

1️⃣ Ejercicio 1: Single Responsibility Principle (SRP)
------------------------------------------------------
- Crear una clase Reporte que tenga métodos para:
  - generar_reporte(datos)
  - imprimir_reporte()
  - guardar_reporte(archivo)
- Refactoriza para que cada clase tenga solo una responsabilidad:
  - Reporte -> generar datos
  - Impresora -> imprimir
  - Almacenador -> guardar

2️⃣ Ejercicio 2: Open/Closed Principle (OCP)
---------------------------------------------
- Crear una clase Calculadora con método calcular(valor, operacion)
- Inicialmente soporta suma y resta
- Extiende sin modificar la clase para soportar multiplicación y división usando herencia o composición

3️⃣ Ejercicio 3: Liskov Substitution Principle (LSP)
-----------------------------------------------------
- Crear clase Figura con método area()
- Crear subclases Rectangulo, Cuadrado
- Asegúrate de que puedes sustituir Rectangulo por Cuadrado sin romper el código que usa Figura

4️⃣ Ejercicio 4: Interface Segregation Principle (ISP)
------------------------------------------------------
- Crear una interfaz Animal con métodos volar(), nadar(), caminar()
- Refactoriza para que cada animal implemente solo los métodos que le corresponden:
  - Pato -> volar(), nadar(), caminar()
  - Pez -> nadar()
  - Perro -> caminar(), nadar()

5️⃣ Ejercicio 5: Dependency Inversion Principle (DIP)
-----------------------------------------------------
- Crear clase ServicioEnvio con método enviar(mensaje)
- Crear clases Email, SMS que implementen un método enviar()
- ServicioEnvio no debe depender de Email o SMS directamente, sino de una abstracción
- Inyecta la dependencia al crear el servicio

Consejo para tu caso:
---------------------
- Piensa en tus clases de backend, pipelines o APIs: cada una debe tener una responsabilidad clara.
- Usa interfaces y composición para poder cambiar implementaciones sin tocar el resto del sistema.
- Esto te prepara para proyectos más complejos y escalables.
"""
