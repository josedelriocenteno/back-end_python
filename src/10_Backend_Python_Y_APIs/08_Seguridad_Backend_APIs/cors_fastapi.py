"""
SEGURIDAD: CONFIGURACIÓN DE CORS EN FASTAPI
-----------------------------------------------------------------------------
CORS (Cross-Origin Resource Sharing) es un mecanismo de seguridad del 
navegador que evita que una web maliciosa haga peticiones a tu API sin permiso.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. DEFINICIÓN DE ORÍGENES PERMITIDOS
# Lista de URLs exactas desde las que tu frontend hará las peticiones.
origins = [
    "http://localhost:3000",        # React en desarrollo
    "http://127.0.0.1:3000",
    "https://mi-app-produccion.com",# Tu frontend en la nube
]

# 2. CONFIGURACIÓN DEL MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Orígenes permitidos
    allow_credentials=True,           # Permite enviar cookies y auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Verbos permitidos
    allow_headers=["Content-Type", "Authorization", "X-Custom-Header"], # Headers
)

@app.get("/")
def main():
    return {"message": "CORS configurado correctamente"}

"""
Peligros y Malas Prácticas:
-----------------------------------------------------------------------------
1. allow_origins=["*"]: NUNCA uses el asterisco en producción. Permite que 
   CUALQUIER web del mundo llame a tu API, facilitando ataques como CSRF.
2. Wildcards confusos: Ten cuidado al usar subdominios (*.ejemplo.com).
3. Entornos locales: A veces 'localhost' y '127.0.0.1' se consideran 
   orígenes distintos por el navegador. Pon ambos.
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. CORS no es una medida de seguridad del servidor, sino una instrucción 
   que el servidor da al NAVEGADOR.
2. Si tu cliente no es un navegador (ej: una App móvil o un script de Python), 
   CORS no tiene efecto.
3. La "Petición Preflight" (OPTIONS): El navegador pregunta primero si tiene 
   permiso antes de hacer un POST o PUT. FastAPI maneja esto automáticamente.
"""
