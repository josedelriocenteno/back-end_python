# cuando_lanzar_excepcion.md
============================

## Objetivo
- Aprender criterios profesionales para lanzar excepciones
- Evitar abusos de raise que rompan flujo normal
- Mejorar robustez y claridad del código

---

## 1️⃣ CUÁNDO LANZAR EXCEPCIONES

1. **Estado inválido de datos o parámetros**
   - Cuando una función recibe datos que no puede procesar.
   - Ejemplo:
     ```python
     def crear_usuario(nombre: str, email: str):
         if not nombre:
             raise ValueError("Nombre vacío")
         if "@" not in email:
             raise ValueError("Email inválido")
     ```

2. **Condición que impide continuar la ejecución**
   - Cuando continuar podría causar corrupción de datos o comportamiento incorrecto.
   - Ejemplo:
     ```python
     saldo = -100
     if saldo < 0:
         raise RuntimeError("Saldo negativo no permitido")
     ```

3. **Errores externos críticos**
   - Fallos de recursos externos como base de datos, archivos o servicios.
   - Ejemplo:
     ```python
     if not conexion_db.esta_activa():
         raise ConnectionError("No se puede conectar a la DB")
     ```

4. **Validaciones obligatorias de negocio**
   - Reglas que deben cumplirse para garantizar integridad de la aplicación.
   - Ejemplo:
     ```python
     if producto.precio < 0:
         raise ProductoInvalidoError("Precio no puede ser negativo")
     ```

---

## 2️⃣ CUÁNDO NO LANZAR EXCEPCIONES

1. **Flujo normal del programa**
   - No usar raise para condicionar comportamiento estándar.
   - ❌ Ejemplo: `raise Exception("Usuario no ingresado")` cada vez que un input es opcional.
   - ✅ Mejor: return None o valor por defecto.

2. **Errores que se pueden manejar localmente**
   - Si puedes recuperar automáticamente el error, no necesitas interrumpir.
   - Ejemplo: lectura de archivo temporal, reconexión automática a servicio.

3. **Para reemplazar lógica de control**
   - No usar excepciones como reemplazo de if/else.
   - ❌ Evitar:
     ```python
     try:
         x = int(input_usuario)
     except ValueError:
         x = 0  # usar flujo normal
     ```
   - ✅ Mejor validar antes:
     ```python
     if input_usuario.isdigit():
         x = int(input_usuario)
     else:
         x = 0
     ```

---

## 3️⃣ PRINCIPIOS DE BUEN CRITERIO

- **Excepciones = situaciones excepcionales**, no el camino habitual
- Documenta qué excepciones lanza cada función
- Usa excepciones específicas para que el llamador pueda reaccionar correctamente
- No ocultes errores, captura y relanza si es necesario
- Aplica **fail-fast**: detecta problemas lo antes posible

---

## 4️⃣ RESUMEN

| Cuándo lanzar               | Cuándo no lanzar                  |
|-----------------------------|----------------------------------|
| Estado inválido de datos    | Flujo normal del programa        |
| Condición que impide continuar | Errores recuperables localmente |
| Recursos externos críticos  | Para reemplazar lógica de control|
| Validaciones de negocio     | Cuando hay alternativas seguras |

> **Regla clave:** si continuar la ejecución es inseguro o incorrecto, lanza excepción; si puedes manejarlo dentro del flujo, usa validaciones o valores por defecto.

---

Este criterio te permite escribir código **robusto, predecible y mantenible**, evitando que errores menores rompan toda tu aplicación.
