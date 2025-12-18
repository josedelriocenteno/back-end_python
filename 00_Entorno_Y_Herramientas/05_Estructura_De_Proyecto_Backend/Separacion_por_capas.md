# Separación por Capas en Backend

## 1. Introducción

En el desarrollo backend profesional, la **separación por capas** es un principio de arquitectura que **organiza el código en niveles funcionales**, facilitando mantenimiento, escalabilidad y pruebas.

> ⚠️ Nota:
> Mezclar lógica de negocio, acceso a datos y presentación en un mismo archivo genera código confuso, difícil de escalar y propenso a errores.

---

## 2. Capas típicas en un proyecto backend

### 2.1 Capa de Presentación (o API)

- Se encarga de **interactuar con el usuario o cliente**.  
- Recibe peticiones, valida datos y responde.  
- Ejemplos: FastAPI endpoints, serializers, controladores HTTP.

```python
from fastapi import FastAPI
from app.services.user_service import create_user

app = FastAPI()

@app.post("/users")
def create_user_endpoint(name: str, email: str):
    return create_user(name, email)
2.2 Capa de Lógica de Negocio (o Services)
Contiene reglas de negocio y procesamiento de datos.

Separa la lógica de cómo se procesan los datos de cómo se reciben o almacenan.

python
Copiar código
# app/services/user_service.py
from app.repositories.user_repository import insert_user

def create_user(name: str, email: str):
    # Validaciones o reglas de negocio
    if not email.endswith("@example.com"):
        raise ValueError("Email inválido")
    return insert_user(name, email)
2.3 Capa de Acceso a Datos (o Repository / DAO)
Encapsula interacciones con la base de datos.

Permite cambiar de base de datos sin afectar la lógica de negocio.

python
Copiar código
# app/repositories/user_repository.py
from app.database import db_session
from app.models import User

def insert_user(name: str, email: str):
    user = User(name=name, email=email)
    db_session.add(user)
    db_session.commit()
    return user
2.4 Capa de Configuración y Utilidades
Contiene configuración del proyecto, constantes, helpers y funciones comunes.

Facilita mantener limpio el resto del código.

python
Copiar código
# app/config.py
DATABASE_URL = "postgresql://user:password@localhost/dbname"
SECRET_KEY = "supersecretkey"
3. Ventajas de la separación por capas
Mantenibilidad

Cambiar una capa (por ejemplo, la base de datos) no afecta la lógica de negocio ni la API.

Reutilización

La lógica de negocio puede ser usada en múltiples interfaces (API REST, CLI, cron jobs).

Testabilidad

Se pueden testear las capas individualmente (unit tests) y combinadas (integration tests).

Escalabilidad

Facilita crecer el proyecto, añadir nuevas funcionalidades o migrar tecnologías.

4. Estructura de proyecto profesional
bash
Copiar código
app/
├── main.py                 # Punto de entrada (API)
├── config.py               # Configuración
├── models/                 # Definición de modelos de datos
│   └── user.py
├── repositories/           # Acceso a datos
│   └── user_repository.py
├── services/               # Lógica de negocio
│   └── user_service.py
├── api/                    # Endpoints y routers
│   └── user_router.py
├── utils/                  # Funciones de utilidad
│   └── validators.py
└── tests/                  # Tests por capas
    ├── test_services.py
    └── test_repositories.py
💡 Tip:
Mantener esta estructura desde el inicio evita deuda técnica y facilita la incorporación de nuevos desarrolladores.

5. Buenas prácticas
Cada capa tiene responsabilidad única (principio SRP).

Evitar que la capa de presentación acceda directamente a la base de datos.

Usar interfaces claras entre capas (parámetros y retornos bien definidos).

Documentar funciones y endpoints para facilitar mantenimiento.

Aplicar testing unitario y de integración por capa.

6. Errores comunes a evitar
Mezclar lógica de negocio con acceso a datos en un mismo archivo.

Escribir endpoints que contengan SQL directo.

No separar configuraciones y constantes del código.

Crear dependencias circulares entre capas.

7. Checklist rápido
 Capa de presentación separada (API / Endpoints)

 Capa de lógica de negocio (Services) definida

 Capa de acceso a datos (Repository / DAO) aislada

 Configuración y utilidades centralizadas

 Tests independientes por capa

 Responsabilidad única de cada capa

8. Conclusión
La separación por capas es un principio fundamental en backend profesional.
Permite escribir código mantenible, escalable y testeable, evitando problemas de deuda técnica y facilitando la colaboración en equipos grandes.