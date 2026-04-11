# Servicios vs Repositorios: ¿Dónde pongo mi código?

Uno de los debates más comunes en el desarrollo Backend es la delgada línea que separa a un **Servicio** de un **Repositorio**. Aquí tienes la guía definitiva para separar responsabilidades.

## 1. El Repositorio (Mecánica de Datos)

El repositorio debe comportarse como una colección en memoria. Su único trabajo es hablar con el mecanismo de persistencia (SQL/ORM/API externa).

*   **Responsabilidades:**
    *   Filtrar datos por criterios técnicos (`get_by_id`, `find_active`).
    *   Gestionar el mapeo de SQL a Objetos.
    *   Ocultar la complejidad de SQLAlchemy (CTEs, Joins complejos).
*   **Qué NO debe hacer:**
    *   Validar reglas de negocio.
    *   Hacer `COMMIT`.
    *   Lanzar notificaciones (Emails, Slack).

## 2. El Servicio (Lógica de Negocio)

El servicio cordina la lógica de tu dominio utilizando uno o varios repositorios.

*   **Responsabilidades:**
    *   Aplicar reglas de negocio ("Solo los usuarios VIP pueden tener más de 10 pedidos").
    *   Coordinar transacciones (Unit of Work).
    *   Transformar datos de entrada (DLO/Schemas) en entidades de dominio.
    *   Integrar con otros sistemas (Servicios de pago, Notificaciones).
*   **Qué NO debe hacer:**
    *   Escribir queries de SQL (`SELECT * FROM...`).
    *   Saber si los datos vienen de Postgres, Redis o un archivo CSV.

## 3. Ejemplo de Confusión Común

**MAL (Lógica en el Repo):**
```python
class UserRepository:
    def create_user(self, data):
        if not data['email'].endswith('@company.com'): # Regla de negocio en el repo!
            raise Error() 
        user = User(**data)
        session.add(user)
        session.commit() # El repo decide el commit!
```

**BIEN (Separación Clara):**
```python
# Servicio
def register_employee(email, db_uow):
    if not email.endswith('@company.com'):
        raise BusinessRuleError()
    
    with db_uow:
        user = User(email=email)
        db_uow.users.add(user)
        # El commit ocurre al final del servicio
```

## 4. El Factor "Fat Models" (Modelos Gordos)
En algunos frameworks (como Django), la lógica se pone en el Modelo. En arquitecturas escalables de Python, preferimos **Modelos Anémicos** (solo datos) y **Servicios Ricos** para facilitar el testing y la legibilidad.

## Resumen: El Principio de Responsabilidad Única

Si tu código de base de datos interrumpe la lectura de tu lógica de negocio, muévelo a un Repositorio. Si tu lógica de negocio está enterrada en archivos de SQL/ORM, muévela a un Servicio.
