# composicion_en_backend.py
# Uso de composición en un contexto real de backend: servicios, repositorios y clientes

"""
En sistemas backend, la composición permite desacoplar responsabilidades y
facilita testing, mantenimiento y escalabilidad. Cada clase tiene una única responsabilidad
y colabora con otras mediante composición.
"""

# -------------------------------------------------
# REPOSITORIO: acceso a datos
# -------------------------------------------------
class UsuarioRepositorio:
    def __init__(self):
        self.usuarios = {}  # Simula una base de datos en memoria

    def agregar_usuario(self, user_id, nombre):
        self.usuarios[user_id] = nombre

    def obtener_usuario(self, user_id):
        return self.usuarios.get(user_id)

# -------------------------------------------------
# SERVICIO: lógica de negocio
# -------------------------------------------------
class UsuarioServicio:
    def __init__(self, repositorio):
        self.repositorio = repositorio  # Composición: Servicio 'tiene un' Repositorio

    def registrar_usuario(self, user_id, nombre):
        if self.repositorio.obtener_usuario(user_id):
            print(f"Usuario {user_id} ya existe")
        else:
            self.repositorio.agregar_usuario(user_id, nombre)
            print(f"Usuario {nombre} registrado con ID {user_id}")

# -------------------------------------------------
# CLIENTE: capa de presentación o API
# -------------------------------------------------
class ClienteAPI:
    def __init__(self, servicio):
        self.servicio = servicio  # Composición: Cliente 'tiene un' Servicio

    def crear_usuario(self, user_id, nombre):
        self.servicio.registrar_usuario(user_id, nombre)

# -------------------------------------------------
# USO REAL
# -------------------------------------------------
repositorio = UsuarioRepositorio()
servicio = UsuarioServicio(repositorio)
cliente_api = ClienteAPI(servicio)

cliente_api.crear_usuario(1, "Ana")
cliente_api.crear_usuario(2, "Luis")
cliente_api.crear_usuario(1, "Ana")  # Maneja duplicados

# Salida esperada:
# Usuario Ana registrado con ID 1
# Usuario Luis registrado con ID 2
# Usuario 1 ya existe

# -------------------------------------------------
# LECCIONES
# -------------------------------------------------
"""
- Cada clase tiene una responsabilidad clara: repositorio, servicio, cliente.
- La composición permite reemplazar componentes fácilmente:
  por ejemplo, cambiar UsuarioRepositorio por uno que use SQL sin tocar el servicio.
- Facilita testing: se pueden inyectar mocks en los servicios.
- Evita jerarquías rígidas y problemas que surgirían si usáramos herencia para todo.
"""
