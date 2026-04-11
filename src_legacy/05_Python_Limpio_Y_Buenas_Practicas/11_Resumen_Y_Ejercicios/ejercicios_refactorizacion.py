"""
ejercicios_refactorizacion.py
=============================

Ejercicios prácticos: de código sucio a código limpio

Objetivo:
- Aplicar todo lo aprendido en Python limpio y buenas prácticas
- Mejorar legibilidad, mantenibilidad y reproducibilidad
- Practicar refactorización paso a paso
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO 1: Función gigante → funciones pequeñas
# -------------------------------------------------------------------

# ❌ Código sucio
def procesar_pedido_sucio(pedido):
    total = 0
    for p in pedido["productos"]:
        total += p["precio"] * p["cantidad"]
    print("Total:", total)
    if total > 100:
        print("Pedido VIP")
    else:
        print("Pedido normal")
    for p in pedido["productos"]:
        p["stock"] -= p["cantidad"]

# ✅ Código limpio
from typing import List, Dict

def calcular_total(productos: List[Dict]) -> float:
    """Calcula total de los productos"""
    return sum(p["precio"] * p["cantidad"] for p in productos)

def clasificar_pedido(total: float) -> str:
    """Devuelve tipo de pedido según total"""
    return "VIP" if total > 100 else "Normal"

def actualizar_stock(productos: List[Dict]) -> List[Dict]:
    """Devuelve nueva lista de productos con stock actualizado"""
    return [{"nombre": p["nombre"], "precio": p["precio"], "cantidad": p["cantidad"], "stock": p["stock"] - p["cantidad"]} for p in productos]

def procesar_pedido_limpio(pedido: Dict) -> Dict:
    """Pipeline limpio: calcula total, clasifica y actualiza stock"""
    total = calcular_total(pedido["productos"])
    tipo = clasificar_pedido(total)
    productos_actualizados = actualizar_stock(pedido["productos"])
    print(f"Total: {total}, Tipo: {tipo}")
    return {"total": total, "tipo": tipo, "productos": productos_actualizados}


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO 2: Código con side effects → funciones puras
# -------------------------------------------------------------------

# ❌ Código sucio
def agregar_feature_sucio(df):
    df["x2"] = df["x"] ** 2
    df["y_log"] = df["y"].apply(lambda v: np.log(v))
    print(df.head())
    df.to_csv("output.csv", index=False)
    return df

# ✅ Código limpio
import pandas as pd
import numpy as np

def agregar_feature_puro(df: pd.DataFrame) -> pd.DataFrame:
    """Transformación pura sin efectos secundarios"""
    df_new = df.copy()
    df_new["x2"] = df_new["x"] ** 2
    df_new["y_log"] = df_new["y"].apply(np.log)
    return df_new

def guardar_salida(df: pd.DataFrame, ruta: str):
    """Side effect separado: guarda CSV"""
    df.to_csv(ruta, index=False)

def imprimir_resumen(df: pd.DataFrame):
    """Side effect separado: imprime resumen"""
    print(df.describe())


# -------------------------------------------------------------------
# 3️⃣ EJEMPLO 3: Clases mal estructuradas → SRP y composición
# -------------------------------------------------------------------

# ❌ Código sucio
class PedidoDios:
    def __init__(self, usuario, productos):
        self.usuario = usuario
        self.productos = productos
        self.total = 0
    def procesar(self):
        self.total = sum(p["precio"]*p["cantidad"] for p in self.productos)
        print("Total:", self.total)
        for p in self.productos:
            p["stock"] -= p["cantidad"]

# ✅ Código limpio usando composición
class Producto:
    def __init__(self, nombre: str, precio: float, stock: int, cantidad: int):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.cantidad = cantidad

class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

class Pedido:
    def __init__(self, usuario: Usuario, productos: List[Producto]):
        self.usuario = usuario
        self.productos = productos

    def calcular_total(self) -> float:
        return sum(p.precio * p.cantidad for p in self.productos)

    def actualizar_stock(self):
        for p in self.productos:
            p.stock -= p.cantidad

    def procesar(self):
        total = self.calcular_total()
        self.actualizar_stock()
        return total


# -------------------------------------------------------------------
# 4️⃣ EJEMPLO 4: Código repetido → modular y reutilizable
# -------------------------------------------------------------------

# ❌ Código sucio
def enviar_email_usuario(usuario):
    print(f"Enviando email a {usuario['email']}")
def enviar_email_admin(admin):
    print(f"Enviando email a {admin['email']}")

# ✅ Código limpio
def enviar_email(destinatario_email: str, asunto: str, mensaje: str):
    """Función genérica para enviar emails"""
    print(f"Enviando email a {destinatario_email} | Asunto: {asunto}")
    # Aquí iría lógica real de envío

# Uso
# enviar_email(usuario.email, "Pedido procesado", "Su pedido fue procesado")
# enviar_email(admin.email, "Nuevo pedido", "Se ha creado un pedido")


# -------------------------------------------------------------------
# 5️⃣ EJERCICIO FINAL PARA EL USUARIO
# -------------------------------------------------------------------

# ❌ Código sucio a refactorizar:
"""
def procesar_datos(df):
    for i in range(len(df)):
        df['x2'][i] = df['x'][i]**2
        df['y_log'][i] = np.log(df['y'][i])
    print(df.head())
    df.to_csv("output.csv")
"""

# ✅ Tarea: refactorizar usando funciones puras, vectorización y separación de side effects

# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------

# Principios aplicados:
# - SRP: cada función/clase hace una sola cosa
# - Funciones puras y side effects separados
# - Tipado y docstrings completos
# - Código modular y reutilizable
# - Pipelines reproducibles
# - Limpieza y legibilidad profesional
