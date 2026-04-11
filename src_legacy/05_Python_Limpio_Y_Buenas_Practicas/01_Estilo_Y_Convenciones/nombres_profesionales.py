"""
nombres_profesionales.py
========================

Este archivo enseña a poner nombres profesionales en Python:
- variables
- funciones
- clases

Nombrar no es un detalle estético.
Es una de las habilidades más importantes de un ingeniero.

Un buen nombre:
- elimina comentarios
- reduce bugs
- hace el código autoexplicativo
"""

# -------------------------------------------------------------------
# 1️⃣ PRINCIPIO FUNDAMENTAL
# -------------------------------------------------------------------
#
# Un nombre debe responder a esta pregunta:
# 👉 ¿QUÉ representa o QUÉ hace?
#
# Si no puedes responderlo sin contexto adicional,
# el nombre es malo.


# -------------------------------------------------------------------
# 2️⃣ VARIABLES: MALOS NOMBRES
# -------------------------------------------------------------------

# ❌ MAL: no dicen nada
x = 10
data = []
temp = 5

# ❌ MAL: abreviaturas crípticas
usr = "Juan"
cnt = 3
flg = True

# ❌ MAL: nombres genéricos que no aportan significado
info = {}
result = None


# -------------------------------------------------------------------
# 3️⃣ VARIABLES: BUENOS NOMBRES
# -------------------------------------------------------------------

# ✅ BIEN: descriptivos y concretos
cantidad_productos = 10
usuarios_registrados = []
intentos_fallidos_login = 3

# ✅ BIEN: booleanos como preguntas
es_admin = True
tiene_descuento = False
pedido_pagado = True

# Regla práctica:
# - si es booleano → empieza por es / tiene / puede / debe
# - el nombre debe leerse como una frase


# -------------------------------------------------------------------
# 4️⃣ VARIABLES: CONTEXTO IMPLÍCITO
# -------------------------------------------------------------------
#
# Evita repetir el contexto si ya es obvio.

# ❌ MAL
usuario_nombre = "Ana"
usuario_email = "ana@email.com"

# ✅ BIEN
nombre = "Ana"
email = "ana@email.com"

# El contexto ya lo da la clase o el módulo.


# -------------------------------------------------------------------
# 5️⃣ FUNCIONES: MALOS NOMBRES
# -------------------------------------------------------------------

# ❌ MAL: verbo genérico
def procesar(datos):
    pass

# ❌ MAL: no indica efecto
def handle(user):
    pass

# ❌ MAL: ambiguo
def check(usuario):
    pass


# -------------------------------------------------------------------
# 6️⃣ FUNCIONES: BUENOS NOMBRES
# -------------------------------------------------------------------

# ✅ BIEN: verbo + intención clara
def validar_email(email: str) -> bool:
    pass


def calcular_total_pedido(pedidos) -> float:
    pass


def guardar_usuario_en_base_de_datos(usuario) -> None:
    pass

# Regla:
# - si no sabes cómo nombrar la función
# - probablemente hace demasiadas cosas


# -------------------------------------------------------------------
# 7️⃣ FUNCIONES QUE DEVUELVEN BOOLEANOS
# -------------------------------------------------------------------

# ❌ MAL
def usuario(usuario):
    return True

# ✅ BIEN
def es_usuario_activo(usuario) -> bool:
    return True

# El nombre debe dejar claro qué significa True o False.


# -------------------------------------------------------------------
# 8️⃣ CLASES: MALOS NOMBRES
# -------------------------------------------------------------------

# ❌ MAL: demasiado genérico
class Manager:
    pass

# ❌ MAL: verbo en una clase
class Calcular:
    pass

# ❌ MAL: abreviaturas
class Usr:
    pass


# -------------------------------------------------------------------
# 9️⃣ CLASES: BUENOS NOMBRES
# -------------------------------------------------------------------

# ✅ BIEN: sustantivos del dominio
class Usuario:
    pass


class Pedido:
    pass


class RepositorioUsuarios:
    pass

# Las clases:
# - representan CONCEPTOS
# - no acciones
# - no procesos


# -------------------------------------------------------------------
# 🔟 COHERENCIA EN TODO EL PROYECTO
# -------------------------------------------------------------------
#
# Esto es CLAVE y casi nadie lo hace bien.
#
# ❌ MAL
def get_user():
    pass

def guardarUsuario():
    pass

def eliminar_usuario_db():
    pass

# ❌ Estilos mezclados:
# - inglés / español
# - snake_case / camelCase
# - abreviaturas / palabras completas


# ✅ BIEN
def obtener_usuario():
    pass

def guardar_usuario():
    pass

def eliminar_usuario():
    pass

# Regla de oro:
# 👉 un proyecto = un idioma = un estilo


# -------------------------------------------------------------------
# 1️⃣1️⃣ NOMBRES LARGOS vs NOMBRES CORTOS
# -------------------------------------------------------------------
#
# Mito: "nombres largos son malos"
#
# Realidad:
# - nombres CLAROS ganan
# - aunque sean largos

# ❌ MAL
def calc(p, d, t):
    pass

# ✅ BIEN
def calcular_precio_final_con_descuento_y_impuestos(
    precio_base,
    descuento,
    tipo_usuario,
):
    pass

# Si te parece largo:
# - es porque el problema es complejo
# - no porque el nombre esté mal


# -------------------------------------------------------------------
# 1️⃣2️⃣ NOMBRES EN DATA / IA (MUY IMPORTANTE)
# -------------------------------------------------------------------
#
# En ML, los nombres MALOS destruyen la reproducibilidad.

# ❌ MAL
X = cargar_datos()
y = entrenar(X)

# ✅ BIEN
datos_entrenamiento = cargar_datos()
modelo_entrenado = entrenar_modelo(datos_entrenamiento)

# El lector debe saber QUÉ es cada cosa sin contexto extra.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Nombrar bien:
# - reduce la necesidad de comentarios
# - reduce bugs
# - mejora el diseño
#
# Si te cuesta nombrar algo:
# 👉 para y piensa
#
# Nombrar es diseño.
# No es un detalle.
