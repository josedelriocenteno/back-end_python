# Rutas y Paths en Python – Backend Profesional

## 1. Concepto clave

- Una **ruta** indica la localización de un archivo o directorio en el sistema de archivos.
- Un **path** puede ser absoluto o relativo.
- La correcta gestión de rutas es **crítica en proyectos de backend**, especialmente en entornos multiplataforma.

---

## 2. Tipos de rutas

1. **Ruta absoluta**
   - Comienza desde la raíz del sistema.
   - Ejemplo Linux: `/home/usuario/proyecto/datos.txt`
   - Ejemplo Windows: `C:\Users\usuario\proyecto\datos.txt`

2. **Ruta relativa**
   - Basada en la ubicación del script que se ejecuta.
   - Ejemplo: `../datos/usuarios.txt`
   - ✔️ Preferido en proyectos para evitar hardcode de paths absolutos.

---

## 3. Uso de Pathlib (Profesional)

```python
from pathlib import Path

# Ruta relativa
ruta = Path("datos") / "usuarios.txt"

# Crear directorios si no existen
ruta.parent.mkdir(parents=True, exist_ok=True)

# Comprobar existencia
if ruta.exists():
    print("Archivo existe")
else:
    print("Archivo no existe")
✔️ Funciona en Linux, Windows y MacOS

✔️ Permite operaciones de path seguras y legibles

4. Conversión entre Path y string
python
Copiar código
str_path = str(ruta)  # Path -> string
path_obj = Path(str_path)  # string -> Path
Evita errores al usar funciones que solo aceptan strings.

5. Obtener rutas dinámicas
python
Copiar código
# Ruta del script actual
ruta_script = Path(__file__).resolve().parent

# Ruta a un archivo dentro del proyecto
ruta_datos = ruta_script / "datos" / "usuarios.txt"
✔️ Evita problemas cuando el script se ejecuta desde otro directorio

✔️ Base sólida para proyectos escalables

6. Evitar errores comunes
❌ Concatenar strings con + → errores de separador entre sistemas (/ vs \)

❌ Hardcode de paths absolutos → no portátil

❌ No comprobar existencia de carpetas → errores en producción

❌ Mezclar os.path con Pathlib sin criterio → confusión

7. Buenas prácticas profesionales
Usar Pathlib siempre que sea posible

Evitar hardcode de rutas

Comprobar existencia de archivos y carpetas antes de operar

Crear carpetas necesarias automáticamente

Usar rutas relativas basadas en __file__ para módulos internos

Documentar paths esperados y estructura de directorios

8. Checklist mental backend
✔️ Uso de Pathlib para todas las rutas?

✔️ Rutas relativas y portables?

✔️ Existencia de carpetas verificada?

✔️ No hardcode de paths absolutos?

✔️ Compatible Linux/Windows/Mac?

✔️ Código limpio y mantenible?

9. Regla de oro
Gestionar rutas y paths de forma profesional evita errores silenciosos, hace tu backend portable y escalable, y prepara el proyecto para producción sin sorpresas.

yaml
Copiar código

---

🔥 **Verdad profesional**  
El 80% de errores de producción por archivos vienen de **rutas mal gestionadas o hardcodeadas**. 