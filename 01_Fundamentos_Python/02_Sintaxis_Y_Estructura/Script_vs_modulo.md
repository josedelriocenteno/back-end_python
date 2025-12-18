# Script vs Módulo en Python Profesional

## 1. Introducción

En Python, la distinción entre **script** y **módulo** es clave para desarrollar código profesional, mantenible y escalable.  
Entender esta diferencia te permite organizar proyectos correctamente y **evitar errores de importación o ejecución**.

> ⚠️ Nota:  
> Un script puede convertirse en módulo y viceversa, pero **cada uno tiene un rol específico** en un proyecto profesional.

---

## 2. Qué es un Script

- Archivo Python ejecutable directamente desde la terminal.  
- Su propósito principal es **realizar tareas o ejecutar programas**.

### 2.1 Características de un Script

- Contiene lógica completa para una tarea específica.  
- Generalmente se ejecuta con:

```bash
python script.py
Puede incluir funciones y clases, pero el foco es la ejecución inmediata.

2.2 Ejemplo de Script
python
Copiar código
# script_backup.py
import os
from datetime import datetime

def crear_backup():
    fecha = datetime.now().strftime("%Y%m%d")
    os.system(f"tar -czf backup_{fecha}.tar.gz /ruta/a/carpeta")

if __name__ == "__main__":
    crear_backup()
    print("Backup completado.")
La condición if __name__ == "__main__": asegura que el código solo se ejecute cuando se ejecuta directamente, no al importar.

3. Qué es un Módulo
Archivo Python diseñado para ser importado y reutilizado.

Contiene funciones, clases y constantes que otros scripts o módulos pueden usar.

3.1 Características de un Módulo
No se espera que se ejecute directamente (aunque puede incluir código bajo __main__).

Permite modularidad y reutilización.

Facilita pruebas unitarias y mantenimiento profesional.

3.2 Ejemplo de Módulo
python
Copiar código
# modulo_utilidades.py
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b

def restar(a: int, b: int) -> int:
    """Resta dos números enteros."""
    return a - b
3.3 Uso del módulo en un script
python
Copiar código
# script_calculos.py
from modulo_utilidades import sumar, restar

resultado = sumar(5, 3)
print(f"Suma: {resultado}")

resultado = restar(10, 4)
print(f"Resta: {resultado}")
4. Buenas prácticas
Separar scripts de módulos

Scripts → ejecutables directos

Módulos → reutilizables, importables

Usar if __name__ == "__main__":

Evita que el código se ejecute al importar un módulo

Organizar directorios por propósito

css
Copiar código
proyecto/
│
├── scripts/
│   ├── script_backup.py
│   └── script_reportes.py
│
├── modules/
│   ├── modulo_utilidades.py
│   └── modulo_datos.py
│
└── main.py
Documentar módulos y funciones

Docstrings claros con parámetros, retornos y excepciones.

5. Checklist rápido Script vs Módulo
 Scripts son ejecutables directos, módulos son importables

 Usar __main__ para scripts que también pueden ser módulos

 Modularizar funciones y clases en módulos para reutilización

 Mantener organización clara de directorios

 Documentar todos los módulos y funciones

 Evitar mezclar lógica de ejecución con lógica de librerías en el mismo archivo

6. Conclusión
Diferenciar scripts y módulos es fundamental para escribir código Python profesional, limpio y escalable.
Esta separación permite reutilización, pruebas, mantenibilidad y colaboración efectiva en proyectos backend, data e IA.