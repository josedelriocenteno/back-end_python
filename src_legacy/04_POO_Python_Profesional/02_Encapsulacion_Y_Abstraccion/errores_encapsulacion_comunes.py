# errores_encapsulacion_comunes.py
# Ejemplo de errores típicos de encapsulación en Python
# Orientado a tu caso: backend y manejo de datos

"""
Los errores más comunes en encapsulación:
1. Clases anémicas: solo tienen atributos públicos y no encapsulan lógica.
2. Getters y setters inútiles: exponer atributos sin control real no aporta nada.
"""

# -------------------------------------------------
# ERROR 1: Clase anémica
# -------------------------------------------------
class UsuarioAnemico:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

# Uso
usuario = UsuarioAnemico("Ana", "ana@correo.com")
# Todo el acceso se hace directamente: usuario.nombre, usuario.email
# No hay lógica ni control sobre los datos, difícil de mantener y testear

# -------------------------------------------------
# ERROR 2: Getters y setters inútiles
# -------------------------------------------------
class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    # Getters y setters que no hacen nada útil
    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_precio(self):
        return self._precio

    def set_precio(self, valor):
        self._precio = valor

# Uso
p = Producto("Camiseta", 20)
p.set_precio(25)  # No hay validación, solo complicamos el código

# -------------------------------------------------
# CORRECTO: Encapsulación útil
# -------------------------------------------------
class ProductoBien:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

# Uso seguro
p2 = ProductoBien("Camiseta", 20)
p2.precio = 30  # Funciona
# p2.precio = -5  # Lanza ValueError, protección real de datos

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Evita clases anémicas: encapsula comportamiento, no solo datos.
2. No pongas getters y setters que no aporten nada.
3. Usa propiedades (@property) para controlar acceso y validar datos.
4. Mantén la lógica de negocio dentro de las clases, no afuera.
5. Facilita testing y mantenibilidad: los cambios internos no rompen código externo.
"""
