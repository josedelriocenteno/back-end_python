# Reproducibilidad y Versionado Exacto

La reproducibilidad es la capacidad de recrear un entorno idéntico en cualquier momento y lugar. En el mundo del Backend y los Datos, es una obligación legal y técnica en muchos casos.

## 1. El peligro de las versiones flotantes
- `pip install fastapi`: Bajará la última versión hoy (ej: 0.103.0). Mañana bajará la 0.104.0.
- Si la 0.104.0 tiene un bug, tu servidor fallará mañana sin que hayas tocado una sola línea de tu código.

## 2. Niveles de Versionado
1. **Laxo:** `fastapi` (Peligro total).
2. **Semántico:** `fastapi>=0.100.0,<0.110.0` (Aceptable en librerías, arriesgado en apps).
3. **Exacto (Pinning):** `fastapi==0.103.0` (Recomendado para producción).
4. **Hasheado:** `fastapi==0.103.0 --hash=sha256:abcd...` (Nivel seguridad bancaria/militar).

## 3. El archivo de Lock: El contrato final
El `poetry.lock` o `requirements-lock.txt` no es solo una lista. Es una foto exacta de TODO el árbol de dependencias, incluyendo las librerías que usan tus librerías.
- **Regla Senior:** Nunca subas una imagen a producción sin un archivo de Lock. Es tu seguro de vida contra el caos externo.

## 4. Versionado de la Imagen Base
No uses `FROM python:3`.
- `3` hoy es 3.11, mañana será 3.12 y pasado 3.13.
- Usa versiones mayores y menores: `FROM python:3.11-slim`.

## 5. El Registro de Imágenes (Docker Hub)
Una vez construida la imagen, asígnale un tag único (ej: `mi-api:1.2.3` o `mi-api:commit-sha`). 
- **Nunca sobrescribas un tag en producción.** Si la versión 1.2.3 falla, debes poder hacer un rollback a la 1.2.2 instantáneamente porque esa imagen vieja sigue existiendo en el registro.

## Resumen: Cero Sorpresas
La reproducibilidad consiste en eliminar la variable del "tiempo" de tus despliegues. Un sistema senior es predecible, repetible y aburrido. En ingeniería, "aburrido" significa que todo funciona como se esperaba.
