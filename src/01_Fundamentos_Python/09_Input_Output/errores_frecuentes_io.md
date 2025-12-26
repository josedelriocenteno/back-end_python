# Errores Frecuentes de Input/Output en Python – Backend Profesional

## 1. Concepto clave

- Input/Output (I/O) incluye **lectura y escritura de archivos, datos de consola, sockets y streams**.
- Los errores I/O son **una de las principales causas de fallos en backend**.
- Conocer los errores frecuentes permite **prevenirlos antes de que ocurran en producción**.

---

## 2. Errores comunes y cómo evitarlos

### 2.1 Abrir archivos sin cerrar

```python
f = open("archivo.txt", "r")
contenido = f.read()
# f.close() olvidado → fuga de recursos
✅ Solución profesional: usar context manager

python
Copiar código
with open("archivo.txt", "r") as f:
    contenido = f.read()
2.2 No manejar excepciones específicas
python
Copiar código
with open("archivo.txt") as f:
    contenido = f.read()
# FileNotFoundError no manejado → crash
✅ Solución:

python
Copiar código
try:
    with open("archivo.txt", "r") as f:
        contenido = f.read()
except FileNotFoundError:
    print("Archivo no encontrado")
except IOError as e:
    print(f"Error de I/O: {e}")
2.3 Leer archivos grandes sin control
python
Copiar código
# ❌ Leer todo en memoria
contenido = open("archivo_grande.txt").read()
✅ Solución:

python
Copiar código
with open("archivo_grande.txt") as f:
    for linea in f:
        procesar(linea)
2.4 Mezclar modos de lectura/escritura
python
Copiar código
# ❌ Abrir binario y leer como texto
with open("archivo.bin", "r", encoding="utf-8") as f:
    data = f.read()
✅ Solución: usar el modo correcto

python
Copiar código
with open("archivo.bin", "rb") as f:
    data = f.read()
2.5 Hardcode de rutas
python
Copiar código
# ❌ No portátil
f = open("C:\\Users\\usuario\\proyecto\\datos.txt")
✅ Solución: usar pathlib y rutas relativas

python
Copiar código
from pathlib import Path
ruta = Path(__file__).parent / "datos" / "datos.txt"
with open(ruta, "r") as f:
    contenido = f.read()
2.6 No validar datos de entrada
python
Copiar código
edad = int(input("Introduce edad: "))  # ❌ crash si input inválido
✅ Solución:

python
Copiar código
while True:
    try:
        edad = int(input("Introduce edad: "))
        break
    except ValueError:
        print("Entrada inválida, intenta de nuevo")
2.7 Ignorar encoding
python
Copiar código
with open("archivo.txt", "r") as f:  # ❌ puede fallar en UTF-8
    contenido = f.read()
✅ Solución:

python
Copiar código
with open("archivo.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
3. Buenas prácticas profesionales
Usar context managers (with) siempre

Manejar excepciones específicas

Validar entrada de usuario y datos de archivos

Controlar archivos grandes con lectura por bloques o línea a línea

Usar Pathlib y rutas relativas

Especificar encoding

Logging en vez de print para producción

4. Checklist mental backend
✔️ Archivos abiertos con with?

✔️ Excepciones específicas manejadas?

✔️ Rutas portables y Pathlib?

✔️ Datos validados?

✔️ Lectura/escritura segura para archivos grandes?

✔️ Logging profesional en lugar de print?

5. Regla de oro
Nunca confíes en la entrada o salida de datos sin validación y manejo adecuado.
Esto asegura que tu backend sea robusto, seguro y profesional desde el primer día.

yaml
Copiar código

---

🔥 **Verdad profesional**  
Los errores de I/O son **la fuente silenciosa de fallos en producción**. Dominarlos desde el principio te pone muy por delante de cualquier junior. 