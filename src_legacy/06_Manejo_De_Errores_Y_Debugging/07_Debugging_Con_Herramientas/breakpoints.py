"""
breakpoints.py
===============

Objetivo:
- Aprender a usar breakpoints modernos en Python
- Combinar herramientas nativas y de IDE para debugging profesional
- Optimizar inspección de variables y flujo sin depender de prints
"""

# -------------------------------------------------------------------
# 1️⃣ BREAKPOINT NATIVO DE PYTHON 3.7+
# -------------------------------------------------------------------

# Desde Python 3.7 existe la función built-in `breakpoint()`
# Equivalente a `import pdb; pdb.set_trace()`, pero más flexible

def dividir(a, b):
    breakpoint()  # ⬅ Aquí se detendrá el programa
    return a / b

def main():
    x = 10
    y = 0
    resultado = dividir(x, y)
    print("Resultado:", resultado)

# -------------------------------------------------------------------
# 2️⃣ BREAKPOINTS EN IDEs MODERNOS
# -------------------------------------------------------------------

# La mayoría de IDEs (VSCode, PyCharm, PyDev) permiten:
# 1. Hacer click en el margen para crear un breakpoint
# 2. Pausar ejecución automáticamente en esa línea
# 3. Inspeccionar variables locales y globales
# 4. Evaluar expresiones sin modificar código

# Ejemplo en VSCode:
# - Coloca un breakpoint en "resultado = dividir(x, y)"
# - Ejecuta el debugger → se detendrá en esa línea
# - Inspecciona valores: x, y
# - Continúa con step over / step into según necesites

# -------------------------------------------------------------------
# 3️⃣ BREAKPOINTS CON CONDICIONES
# -------------------------------------------------------------------

# Python permite breakpoints condicionales:
x = 0
while x < 5:
    x += 1
    breakpoint() if x == 3 else None  # Solo se detiene cuando x==3
    print("Valor de x:", x)

# Uso profesional:
# - Evita saturar el debugger en bucles grandes
# - Pausa solo cuando ocurre la condición relevante

# -------------------------------------------------------------------
# 4️⃣ BREAKPOINTS REMOTOS / EN PRODUCCIÓN
# -------------------------------------------------------------------

# Técnicas avanzadas:
# 1. `pdb.set_trace()` + SSH para debugging remoto
# 2. Herramientas como `remote-pdb` permiten depurar aplicaciones en servidores
# 3. Usar siempre flags de DEBUG para no activar breakpoints accidentalmente en prod

DEBUG = True
if DEBUG:
    # Solo activamos breakpoint en desarrollo
    # breakpoint()  # Descomentar solo si necesitamos inspección
    pass

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1. Preferir breakpoint() sobre print para debugging
# 2. Usar breakpoints condicionales para bucles o errores específicos
# 3. Nunca dejar breakpoints en código de producción
# 4. Combinar con logging y tests para fail-fast
# 5. Integrar con IDEs para inspección de variables complejas
# 6. Registrar contexto antes de entrar al breakpoint si es remoto
