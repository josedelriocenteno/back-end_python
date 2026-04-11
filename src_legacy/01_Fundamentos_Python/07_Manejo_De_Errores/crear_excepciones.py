# crear_excepciones.py
"""
Crear Excepciones Personalizadas en Python – Backend Profesional

Este módulo cubre:
- Cómo definir tus propias excepciones
- Buenas prácticas de nomenclatura y jerarquía
- Cuándo usarlas en lugar de las estándar
- Evitar errores comunes en producción
"""

# -------------------------------------------------
# 1. Definición básica de una excepción
# -------------------------------------------------
class ErrorPersonalizado(Exception):
    """Excepción base para nuestro proyecto."""
    pass

# Usando la excepción
try:
    raise ErrorPersonalizado("Ocurrió un error personalizado")
except ErrorPersonalizado as e:
    print(f"Caught: {e}")


# -------------------------------------------------
# 2. Jerarquía de excepciones
# -------------------------------------------------
class ErrorValidacion(ErrorPersonalizado):
    """Error cuando los datos de entrada son inválidos."""
    pass

class ErrorConexionBD(ErrorPersonalizado):
    """Error relacionado con la base de datos."""
    pass

# Manejo diferenciado
try:
    raise ErrorValidacion("Campo obligatorio vacío")
except ErrorValidacion as e:
    print(f"Validación fallida: {e}")
except ErrorConexionBD as e:
    print(f"Error de BD: {e}")
except ErrorPersonalizado as e:
    print(f"Error general del proyecto: {e}")


# -------------------------------------------------
# 3. Agregar información útil a la excepción
# -------------------------------------------------
class ErrorAutenticacion(ErrorPersonalizado):
    def __init__(self, usuario: str, mensaje: str):
        self.usuario = usuario
        self.mensaje = mensaje
        super().__init__(f"Usuario: {usuario} -> {mensaje}")

try:
    raise ErrorAutenticacion("juan", "Contraseña incorrecta")
except ErrorAutenticacion as e:
    print(e)  # Usuario: juan -> Contraseña incorrecta


# -------------------------------------------------
# 4. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Nombrar excepciones terminando en "Error"
# ✔️ Crear jerarquía clara: base genérica y subtipos específicos
# ✔️ Incluir información útil para logging y debugging
# ✔️ No usar excepciones genéricas (Exception) en tu código
# ✔️ Usar excepciones para flujos anómalos, no para control normal


# -------------------------------------------------
# 5. Errores comunes de juniors
# -------------------------------------------------
# ❌ Capturar Exception genérico → oculta problemas reales
# ❌ No diferenciar tipos de error → debugging difícil
# ❌ No documentar qué puede lanzar la función
# ❌ Mezclar excepciones de librerías con propias sin criterio


# -------------------------------------------------
# 6. Checklist mental backend
# -------------------------------------------------
# ✔️ La excepción refleja el tipo de error real?
# ✔️ La jerarquía está clara y escalable?
# ✔️ Mensaje útil para logs y debugging?
# ✔️ Se diferencia de otras excepciones del proyecto?
# ✔️ Fácil de testear?


# -------------------------------------------------
# 7. Regla de oro
# -------------------------------------------------
"""
Crear tus propias excepciones es esencial para backend profesional:
- Permite un manejo claro y seguro de errores
- Facilita logging, testing y debugging
- Mantiene tu código limpio y mantenible
"""
