# strategy_pattern.py

"""
STRATEGY PATTERN — Algoritmos intercambiables
=============================================

Este patrón SÍ es oro puro.
Si lo entiendes bien, pasas de programador junior a pensar como arquitecto.

Strategy sirve para:
✅ Eliminar if/elif gigantes
✅ Cambiar comportamiento sin tocar código existente
✅ Aplicar SOLID (OCP + DIP)
✅ Diseñar sistemas extensibles (backend, IA, ML, reglas de negocio)

Está DIRECTAMENTE alineado con:
- Backend profesional
- Pipelines de datos
- IA (modelos, scoring, validación, preprocesado)
"""

# ============================================================
# ❌ PROBLEMA REAL: if/elif según el comportamiento
# ============================================================

def calcular_precio(tipo_usuario: str, precio_base: float) -> float:
    if tipo_usuario == "normal":
        return precio_base
    elif tipo_usuario == "premium":
        return precio_base * 0.9
    elif tipo_usuario == "empresa":
        return precio_base * 0.8
    else:
        raise ValueError("Tipo no válido")


"""
Problemas GRAVES:
- Cada nuevo tipo = tocar esta función
- Código rígido
- No testeable por partes
- Violación directa de OCP (Open/Closed)
"""

# ============================================================
# 🧠 IDEA CLAVE DEL STRATEGY PATTERN
# ============================================================

"""
Separar:
- EL QUÉ se hace
- DEL CÓMO se hace

El algoritmo se encapsula en objetos intercambiables.
El sistema usa una estrategia SIN saber cuál es.
"""

# ============================================================
# 🧱 DEFINIMOS LA INTERFAZ (contrato)
# ============================================================

from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    @abstractmethod
    def calcular_precio(self, precio_base: float) -> float:
        pass


"""
Esto es CLAVE:
- El sistema depende de la abstracción
- No de implementaciones concretas
(DIP en acción)
"""

# ============================================================
# 🧩 IMPLEMENTACIONES (estrategias concretas)
# ============================================================

class PrecioNormal(PricingStrategy):
    def calcular_precio(self, precio_base: float) -> float:
        return precio_base


class PrecioPremium(PricingStrategy):
    def calcular_precio(self, precio_base: float) -> float:
        return precio_base * 0.9


class PrecioEmpresa(PricingStrategy):
    def calcular_precio(self, precio_base: float) -> float:
        return precio_base * 0.8


# ============================================================
# 🚀 CONTEXTO: quien USA la estrategia
# ============================================================

class CalculadoraPrecios:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def calcular(self, precio_base: float) -> float:
        return self.strategy.calcular_precio(precio_base)


# ============================================================
# ✅ USO REAL
# ============================================================

precio = 100.0

calc_normal = CalculadoraPrecios(PrecioNormal())
calc_premium = CalculadoraPrecios(PrecioPremium())
calc_empresa = CalculadoraPrecios(PrecioEmpresa())

print(calc_normal.calcular(precio))   # 100
print(calc_premium.calcular(precio))  # 90
print(calc_empresa.calcular(precio))  # 80


"""
Ventajas inmediatas:
- Sin ifs
- Código limpio
- Fácil de extender
"""

# ============================================================
# 🔥 AÑADIR NUEVA ESTRATEGIA SIN TOCAR NADA
# ============================================================

class PrecioEstudiante(PricingStrategy):
    def calcular_precio(self, precio_base: float) -> float:
        return precio_base * 0.85


calc_estudiante = CalculadoraPrecios(PrecioEstudiante())
print(calc_estudiante.calcular(100))


"""
NO se ha modificado:
- CalculadoraPrecios
- Otras estrategias

Esto es OCP REAL.
"""

# ============================================================
# 🧠 STRATEGY EN BACKEND PROFESIONAL
# ============================================================

"""
Casos reales donde Strategy es CLAVE:

- Autenticación (JWT, OAuth, API Key)
- Envío de emails (SMTP, Sendgrid, SES)
- Pagos (Stripe, Paypal, Bizum)
- Validación de datos
- Serialización (JSON, XML, CSV)
- Rate limiting
"""

# ============================================================
# 🧠 STRATEGY EN IA / DATA (MUY IMPORTANTE)
# ============================================================

"""
Aquí es donde BRILLA para tu futuro:
"""

class PreprocessStrategy(ABC):
    @abstractmethod
    def process(self, data):
        pass


class NormalizeStrategy(PreprocessStrategy):
    def process(self, data):
        return [x / max(data) for x in data]


class StandardizeStrategy(PreprocessStrategy):
    def process(self, data):
        mean = sum(data) / len(data)
        return [x - mean for x in data]


class DataPipeline:
    def __init__(self, preprocess: PreprocessStrategy):
        self.preprocess = preprocess

    def run(self, data):
        return self.preprocess.process(data)


pipeline_norm = DataPipeline(NormalizeStrategy())
pipeline_std = DataPipeline(StandardizeStrategy())

print(pipeline_norm.run([1, 2, 3]))
print(pipeline_std.run([1, 2, 3]))


"""
Esto es EXACTAMENTE:
- pipelines ML
- feature engineering
- selección de modelos
"""

# ============================================================
# ⚠️ ERROR COMÚN: strategy innecesaria
# ============================================================

"""
NO uses Strategy si:
❌ Solo hay un algoritmo
❌ No va a cambiar
❌ Añade complejidad artificial

Regla:
👉 Si no hay variación, no hay estrategia
"""

# ============================================================
# 🎯 CONCLUSIÓN CLARA (sin humo)
# ============================================================

"""
Strategy es uno de los patrones MÁS IMPORTANTES que existen.

Si lo dominas:
- eliminas ifs
- diseñas para el cambio
- escribes código profesional
- estás preparado para backend serio e IA

Este patrón SÍ debes usarlo mucho.
El Singleton, con cuidado.
"""

