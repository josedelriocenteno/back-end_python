"""
OBSERVABILIDAD: HEALTH CHECKS PROFESIONALES
-----------------------------------------------------------------------------
Cómo saber si tu API está realmente "viva" y lista para recibir tráfico.
"""

from fastapi import FastAPI, status, Response
from sqlalchemy.orm import Session
from .db_dependency import get_db

app = FastAPI()

# 1. LIVENESS PROBE (¿Está el proceso corriendo?)
@app.get("/health/live", status_code=status.HTTP_200_OK)
def liveness():
    """
    Indica que el proceso de Python no se ha colgado.
    Si este endpoint falla, Kubernetes reiniciará el contenedor.
    """
    return {"status": "alive"}

# 2. READINESS PROBE (¿Están las dependencias listas?)
@app.get("/health/ready")
def readiness(db: Session = Depends(get_db)):
    """
    Verifica que la base de datos y otros servicios externos respondan.
    Si falla, el balanceador de carga dejará de enviarnos usuarios temporalmente.
    """
    try:
        # Hacemos una query ultra simple para testear la conexión
        db.execute("SELECT 1")
        return {"status": "ready", "database": "up"}
    except Exception as e:
        return Response(
            content={"status": "not_ready", "database": "down", "error": str(e)},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

# 3. ENDPOINT DE VERSIÓN (Información técnica)
@app.get("/version")
def get_version():
    return {
        "version": "1.4.2",
        "commit": "ab23c5",
        "env": "production"
    }

"""
RESUMEN PARA EL DESARROLLADOR:
1. Divide Liveness de Readiness. No quieres que reinicien tu app solo porque 
   la DB tiene un hipo de 1 segundo (Readiness sirve para eso).
2. No pongas lógica pesada en el Health Check, se llama cada pocos segundos.
3. El estándar es que estas rutas estén fuera de la autenticación para que 
   los sistemas de monitorización (AWS, K8s) puedan entrar.
"""
