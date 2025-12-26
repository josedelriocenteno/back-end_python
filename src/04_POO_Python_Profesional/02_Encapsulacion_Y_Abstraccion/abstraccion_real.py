# abstraccion_real.py
# Ejemplo de abstracción real usando interfaces conceptuales
# Orientado a tu caso: backend y pipelines de datos

"""
La abstracción permite separar *qué* hace algo de *cómo* lo hace.
En Python se usa con clases base abstractas (ABC) o simplemente con contratos conceptuales.
Esto es crucial para sistemas mantenibles y testables.
"""

from abc import ABC, abstractmethod

# -------------------------------------------------
# Definición de una interfaz (contrato) para un repositorio
# -------------------------------------------------
class Repositorio(ABC):
    """Interfaz conceptual de un repositorio de datos"""

    @abstractmethod
    def guardar(self, entidad):
        """Guardar una entidad"""
        pass

    @abstractmethod
    def obtener_por_id(self, id):
        """Obtener una entidad por su ID"""
        pass

# -------------------------------------------------
# Implementación concreta usando la abstracción
# -------------------------------------------------
class RepositorioMemoria(Repositorio):
    """Repositorio en memoria, útil para testing o prototipos"""

    def __init__(self):
        self._datos = {}

    def guardar(self, entidad):
        self._datos[entidad['id']] = entidad

    def obtener_por_id(self, id):
        return self._datos.get(id)

# -------------------------------------------------
# Uso del repositorio
# -------------------------------------------------
repo = RepositorioMemoria()
usuario = {"id": 1, "nombre": "Juan"}
repo.guardar(usuario)

print(repo.obtener_por_id(1))  # {'id': 1, 'nombre': 'Juan'}
print(repo.obtener_por_id(2))  # None

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Define interfaces conceptuales para separar contrato de implementación.
2. Implementa varias clases concretas que cumplan el mismo contrato
   para diferentes escenarios (memoria, base de datos, API externa).
3. Facilita testing: puedes mockear la interfaz sin tocar la lógica de negocio.
4. Mantiene el backend desacoplado: cambios internos no afectan al cliente.
5. Útil para pipelines, servicios, repositorios y cualquier capa de aplicación.
"""
