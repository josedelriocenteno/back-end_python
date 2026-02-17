"""
SEGURIDAD: CONFIGURACIÓN PROFESIONAL DE CORS
-----------------------------------------------------------------------------
CORS (Cross-Origin Resource Sharing) es un mecanismo de seguridad del 
navegador, NO del servidor, pero se configura en el backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. EL GRAN ERROR: allow_origins=["*"]
# NUNCA uses asterisco en producción. Permite que CUALQUIER web del mundo 
# (incluyendo webs maliciosas) haga peticiones a tu API usando las cookies 
# o el contexto del usuario.

# 2. CONFIGURACIÓN SEGURA
origins = [
    "https://www.tuproyecto.com",      # Tu web oficial
    "https://admin.tuproyecto.com",    # Tu panel de control
    "http://localhost:3000",           # Desarrollo local (React/Next)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Solo orígenes de confianza
    allow_credentials=True,            # Obligatorio si usas cookies de sesión
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Solo verbos necesarios
    allow_headers=["Authorization", "Content-Type"],# Headers permitidos
)

@app.get("/")
def main():
    return {"message": "CORS configurado correctamente"}

"""
REGLA DE ORO PARA EL DESARROLLADOR:
-----------------------------------------------------------------------------
1. CORS no te protege de ataques de servidor a servidor (ej: desde Postman).
2. CORS solo protege al usuario final de que una web maliciosa 'B' robe 
   datos de tu web 'A' mediante el navegador.
3. Si cambias de dominio, no olvides actualizar esta lista o la App dejará 
   de funcionar (errores de 'CORS preflight').
"""

"""
DETECCIÓN DE ERRORES:
Si ves 'Access-Control-Allow-Origin header is missing', revisa:
- Que el dominio origen coincida exactamente (ojo con http vs https).
- Que el método (ej: PUT) esté en allow_methods.
- Que no haya una excepción no controlada en el backend (FastAPI a veces 
  no envía los headers de CORS si la API lanza un 500 interno).
"""
