# singleton_pattern.py

"""
SINGLETON PATTERN — Uso real (y cuándo evitarlo)
===============================================

Este patrón es MUY conocido…
y MUY mal usado.

Si lo usas sin entenderlo:
❌ acoplas todo
❌ rompes tests
❌ creas estados globales ocultos
❌ te cargas la arquitectura

Si lo usas bien:
✅ controlas recursos únicos
✅ centralizas configuración
✅ evitas instancias duplicadas peligrosas

Aquí lo vas a entender DE VERDAD, orientado a backend profesional
(y a tu camino hacia sistemas grandes e IA).
"""

# ============================================================
# 🧨 EL PROBLEMA REAL QUE RESUELVE SINGLETON
# ============================================================

"""
Hay cosas que DEBEN existir una sola vez en un sistema:

- Conexión a base de datos
- Pool de conexiones
- Configuración global (read-only)
- Logger
- Cache en memoria
- Cliente pesado (LLM, modelo ML cargado en RAM)

Si permites múltiples instancias:
- desperdicias memoria
- generas inconsistencias
- puedes romper el sistema
"""

# ============================================================
# ❌ MAL ENFOQUE: variables globales
# ============================================================

config = {
    "DEBUG": True,
    "DB_HOST": "localhost"
}

"""
Problemas:
- Mutable desde cualquier sitio
- Imposible de controlar
- Difícil de testear
- Estado global oculto
"""

# ============================================================
# 🧠 IDEA CLAVE DEL SINGLETON
# ============================================================

"""
Garantizar:
1️⃣ Una sola instancia
2️⃣ Un único punto de acceso
3️⃣ Control explícito del ciclo de vida

NO es “una clase especial”.
Es una decisión de DISEÑO.
"""

# ============================================================
# ❌ IMPLEMENTACIÓN HORRIBLE (anti-patrón clásico)
# ============================================================

class BadSingleton:
    instance = None

    def __init__(self):
        if BadSingleton.instance is not None:
            raise Exception("Ya existe una instancia")
        BadSingleton.instance = self


"""
Problemas:
- Frágil
- Poco pythonico
- Difícil de extender
- Mala experiencia de uso
"""

# ============================================================
# ✅ SINGLETON PYTHONICO (override de __new__)
# ============================================================

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class AppConfig(Singleton):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.debug = True
            self.db_host = "localhost"
            self._initialized = True


config1 = AppConfig()
config2 = AppConfig()

assert config1 is config2  # MISMA instancia


"""
Notas IMPORTANTES:
- __new__ controla la creación
- __init__ se ejecuta varias veces ⇒ hay que protegerlo
"""

# ============================================================
# 🧠 PATRÓN REALISTA: SINGLETON PARA RECURSOS PESADOS
# ============================================================

class ModelLoader(Singleton):
    def __init__(self):
        if not hasattr(self, "_loaded"):
            print("Cargando modelo de IA en memoria...")
            self.model = "MODELO_PESADO"
            self._loaded = True

    def predict(self, data):
        return f"Predicción con {self.model} sobre {data}"


model_a = ModelLoader()
model_b = ModelLoader()

assert model_a is model_b

print(model_a.predict("datos"))


"""
Esto en IA es CRÍTICO:
- Un modelo puede pesar GBs
- Cargarlo varias veces = muerte del sistema
"""

# ============================================================
# 🚀 ALTERNATIVA MEJOR EN BACKEND MODERNO
# ============================================================

"""
En backend serio:
👉 se prefiere INYECCIÓN DE DEPENDENCIAS
👉 el framework controla el ciclo de vida

Ejemplo conceptual (sin framework):
"""

class DatabaseConnection:
    def connect(self):
        print("Conectado a DB")


class Application:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection


db = DatabaseConnection()
app1 = Application(db)
app2 = Application(db)

"""
Esto es EFECTIVAMENTE un singleton,
pero SIN patrón explícito.

MUCHO más testeable.
"""

# ============================================================
# 🧪 TESTS: por qué Singleton es peligroso
# ============================================================

"""
El mayor problema del Singleton:
❌ estado compartido entre tests
❌ orden de ejecución importa
❌ tests no aislados
"""

class CounterSingleton(Singleton):
    def __init__(self):
        if not hasattr(self, "count"):
            self.count = 0

    def increment(self):
        self.count += 1


a = CounterSingleton()
a.increment()

b = CounterSingleton()
assert b.count == 1  # estado compartido → peligro


# ============================================================
# ⚠️ CUÁNDO NO USAR SINGLETON (MUY IMPORTANTE)
# ============================================================

"""
NO uses Singleton si:
❌ El objeto tiene estado mutable de negocio
❌ Necesitas múltiples instancias en tests
❌ Es solo “por comodidad”
❌ Estás empezando y no sabes por qué lo usas

Regla de oro:
👉 Si dudas, NO lo uses
"""

# ============================================================
# ✅ CUÁNDO SÍ USAR SINGLETON
# ============================================================

"""
Úsalo SOLO si:
✔️ El recurso debe ser único
✔️ El estado es técnico (no de negocio)
✔️ El coste de múltiples instancias es alto
✔️ Tienes claro su ciclo de vida

Ejemplos correctos:
- Configuración read-only
- Logger
- Cache
- Cliente LLM
- Cargador de modelos ML
"""

# ============================================================
# 🎯 CONEXIÓN DIRECTA CON TU CAMINO (backend + IA)
# ============================================================

"""
En IA profesional:
- ModelLoader = Singleton (o gestionado por DI)
- Tokenizer = Singleton
- Cliente OpenAI / HF = Singleton
- Cache embeddings = Singleton

Pero:
👉 en aplicaciones grandes, el framework
   (FastAPI, Django, etc.)
   gestiona esto mejor que tú.

Saber Singleton no es para usarlo siempre,
es para SABER CUÁNDO NO USARLO.

Eso es mentalidad senior.
"""
