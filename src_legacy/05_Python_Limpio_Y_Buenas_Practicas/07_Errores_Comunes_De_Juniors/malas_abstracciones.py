"""
malas_abstracciones.py
======================

Anti-patrón: Malas abstracciones (Abstraer sin sentido)

Objetivos:
- Detectar abstracciones innecesarias o prematuras
- Enseñar cuándo y cómo aplicar abstracción correctamente
- Mejorar legibilidad, testabilidad y mantenimiento
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE MALAS ABSTRACCIONES
# -------------------------------------------------------------------

# ❌ MAL: crear una clase/función solo para añadir capas innecesarias

class CalculadoraBase(ABC):
    @abstractmethod
    def calcular(self, x: float, y: float) -> float:
        pass

class Suma(CalculadoraBase):
    def calcular(self, x: float, y: float) -> float:
        return x + y

class Resta(CalculadoraBase):
    def calcular(self, x: float, y: float) -> float:
        return x - y

# Uso innecesario de herencia y abstracción para operaciones simples
def ejemplo_malas_abstracciones():
    suma = Suma()
    resultado = suma.calcular(3, 5)  # podría haberse hecho con una función simple
    print(resultado)

# Problema:
# - Complejidad adicional
# - Difícil de leer para nuevos desarrolladores
# - No aporta valor real en este contexto
# - Mantener esta jerarquía es más costoso que beneficio


# -------------------------------------------------------------------
# 2️⃣ PRINCIPIOS CLAVE PARA BUENAS ABSTRACCIONES
# -------------------------------------------------------------------

# 1. Aplica abstracción solo cuando ayuda a:
#    - Reducir duplicación
#    - Facilitar extensibilidad futura
#    - Separar responsabilidades
# 2. Evita abstraer “porque se ve profesional”
# 3. No generes jerarquías innecesarias
# 4. Prefiere composición y funciones simples
# 5. Testa cada abstracción y verifica que aporta claridad


# -------------------------------------------------------------------
# 3️⃣ EJEMPLO DE BUENA ABSTRACCIÓN
# -------------------------------------------------------------------

def sumar(x: float, y: float) -> float:
    """Suma dos números, simple y directo."""
    return x + y

def restar(x: float, y: float) -> float:
    """Resta dos números, simple y directo."""
    return x - y

def procesar_operacion(x: float, y: float, operacion: str) -> float:
    """
    Procesa operaciones básicas usando funciones simples.
    - Extensible sin jerarquías innecesarias.
    """
    if operacion == "suma":
        return sumar(x, y)
    elif operacion == "resta":
        return restar(x, y)
    else:
        raise ValueError(f"Operación desconocida: {operacion}")


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS DE ESTA REFACTORIZACIÓN
# -------------------------------------------------------------------

# 1. Código simple y legible
# 2. Fácil de testear
# 3. Evita jerarquías y clases innecesarias
# 4. Extensible usando funciones y dispatch simples
# 5. Mantiene claridad y reduce mantenimiento


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Malas abstracciones = complejidad innecesaria
# Principios clave:
# - Abstrae solo cuando aporta valor real
# - Prefiere funciones y composición sobre herencia innecesaria
# - Código simple = más profesional y fácil de mantener
# - Menos jerarquías = menos riesgo de errores
