# modelos_dominio.py

"""
MODELOS DE DOMINIO — ENTIDADES DEL NEGOCIO
========================================

Este archivo es CRÍTICO.
Aquí es donde se separa al programador normal
del que diseña sistemas profesionales.

Si fallas aquí:
❌ tu backend será un CRUD tonto
❌ tu lógica estará dispersa
❌ POO no servirá para nada

Si lo haces bien:
✅ el negocio vive en el código
✅ las reglas están protegidas
✅ el sistema escala sin romperse

Esto está 100% orientado a BACKEND PROFESIONAL
y a tu objetivo real (DAM + IA + sistemas serios).
"""

# ============================================================
# 🧠 ¿QUÉ ES UN MODELO DE DOMINIO?
# ============================================================

"""
Un modelo de dominio NO es:
❌ una tabla de base de datos
❌ un dict con datos
❌ un DTO plano sin lógica

Un modelo de dominio ES:
✅ una representación del NEGOCIO
✅ con estado + comportamiento
✅ que protege sus invariantes

Regla de oro:
👉 Si una regla del negocio existe, VIVE AQUÍ
"""

# ============================================================
# ❌ MAL EJEMPLO (MUY COMÚN)
# ============================================================

class Pedido_MAL:
    def __init__(self, id_, usuario_id, total):
        self.id = id_
        self.usuario_id = usuario_id
        self.total = total


"""
Problemas:
- No protege nada
- total puede ser negativo
- Cualquiera puede mutar el estado
- No hay reglas de negocio

Esto NO es un modelo de dominio.
Es un saco de datos.
"""

# ============================================================
# ✅ BUEN MODELO DE DOMINIO
# ============================================================

class Pedido:
    """
    Entidad Pedido (Domain Entity)

    - Tiene identidad propia (id)
    - Vive en el tiempo
    - Tiene reglas de negocio
    """

    IVA = 0.21  # regla del dominio compartida

    def __init__(self, id_: int, usuario_id: int, total_base: float):
        self._id = id_
        self._usuario_id = usuario_id
        self._total_base = total_base
        self._validar()

    # ----------------------------
    # PROPIEDADES (lectura controlada)
    # ----------------------------

    @property
    def id(self) -> int:
        return self._id

    @property
    def usuario_id(self) -> int:
        return self._usuario_id

    @property
    def total_base(self) -> float:
        return self._total_base

    @property
    def total_con_iva(self) -> float:
        return round(self._total_base * (1 + self.IVA), 2)

    # ----------------------------
    # COMPORTAMIENTO DEL DOMINIO
    # ----------------------------

    def aplicar_descuento(self, porcentaje: float):
        """
        Regla del negocio:
        - No se permiten descuentos negativos
        - No más del 50%
        """
        if not (0 < porcentaje <= 50):
            raise ValueError("Descuento inválido")

        self._total_base *= (1 - porcentaje / 100)

    # ----------------------------
    # INVARIANTES
    # ----------------------------

    def _validar(self):
        if self._total_base <= 0:
            raise ValueError("El total base debe ser mayor que 0")

    def __repr__(self):
        return (
            f"Pedido(id={self.id}, usuario={self.usuario_id}, "
            f"total_base={self.total_base}, total_iva={self.total_con_iva})"
        )


"""
CLAVES IMPORTANTES:
- Los atributos son PRIVADOS
- El estado solo cambia a través de métodos
- Las reglas están encapsuladas
"""

# ============================================================
# 🧠 ENTIDAD VS VALUE OBJECT (CONCEPTO CLAVE)
# ============================================================

"""
ENTIDAD:
- Tiene identidad (id)
- Puede cambiar con el tiempo
- Ej: Pedido, Usuario, Cuenta

VALUE OBJECT:
- No tiene identidad
- Es inmutable
- Se compara por valor
- Ej: Dinero, Email, Coordenadas
"""

# ============================================================
# 🧱 VALUE OBJECT: DINERO
# ============================================================

class Dinero:
    """
    Value Object
    - Inmutable
    - Sin identidad
    - Seguro
    """

    def __init__(self, cantidad: float, moneda: str = "EUR"):
        if cantidad < 0:
            raise ValueError("Cantidad negativa no permitida")
        self._cantidad = round(cantidad, 2)
        self._moneda = moneda

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def moneda(self):
        return self._moneda

    def sumar(self, otro: "Dinero") -> "Dinero":
        if self.moneda != otro.moneda:
            raise ValueError("Monedas incompatibles")
        return Dinero(self.cantidad + otro.cantidad, self.moneda)

    def __eq__(self, other):
        return (
            isinstance(other, Dinero)
            and self.cantidad == other.cantidad
            and self.moneda == other.moneda
        )

    def __repr__(self):
        return f"{self.cantidad} {self.moneda}"


# ============================================================
# 🧠 USANDO VALUE OBJECT DENTRO DE ENTIDAD
# ============================================================

class PedidoConDinero:
    """
    Entidad más segura aún
    """

    def __init__(self, id_: int, usuario_id: int, total: Dinero):
        self._id = id_
        self._usuario_id = usuario_id
        self._total = total

    def aplicar_iva(self) -> Dinero:
        return Dinero(self._total.cantidad * 1.21, self._total.moneda)

    def __repr__(self):
        return f"Pedido(id={self._id}, total={self._total})"


"""
Esto es diseño de dominio SERIO.
Mucho más difícil de romper.
"""

# ============================================================
# 🧠 MODELOS DE DOMINIO ≠ MODELOS DE BD
# ============================================================

"""
ERROR MUY COMÚN:
Usar el modelo de dominio como modelo ORM.

NO:
- El dominio no sabe de SQL
- El dominio no sabe de IDs autoincrementales
- El dominio no sabe de JSON

Eso va en infraestructura.
"""

# ============================================================
# 🧠 DOMINIO EN BACKEND REAL
# ============================================================

"""
Arquitectura limpia:

Domain:
- Pedido
- Usuario
- Dinero
- Reglas del negocio

Application:
- Services
- Casos de uso

Infrastructure:
- SQLAlchemy
- FastAPI
- MongoDB
"""

# ============================================================
# 🧠 DOMINIO EN DATA / IA (TU FUTURO)
# ============================================================

"""
En ML / Data Engineering:
- Dominio = entidades del problema
- Ej: Evento, Feature, VentanaTemporal
"""

class Evento:
    def __init__(self, user_id: int, timestamp: int, valor: float):
        self.user_id = user_id
        self.timestamp = timestamp
        self.valor = valor


class Feature:
    def __init__(self, nombre: str, valor: float):
        self.nombre = nombre
        self.valor = valor


"""
Esto te permite:
- pipelines claros
- features coherentes
- modelos más robustos
"""

# ============================================================
# ⚠️ ERRORES TÍPICOS
# ============================================================

"""
❌ Entidades sin métodos
❌ Lógica en servicios en vez de dominio
❌ Getters/setters sin sentido
❌ Mutabilidad sin control
"""

# ============================================================
# 🎯 CONCLUSIÓN (SIN FILTRO)
# ============================================================

"""
Si tus entidades solo almacenan datos:
👉 NO estás usando POO
👉 estás usando structs caros

Un buen modelo de dominio:
- protege reglas
- expresa el negocio
- reduce bugs
- escala contigo

Esto es lo que diferencia:
🧑‍💻 escribir código
🧠 diseñar sistemas

Y esto es CLAVE para tu camino profesional.
"""
