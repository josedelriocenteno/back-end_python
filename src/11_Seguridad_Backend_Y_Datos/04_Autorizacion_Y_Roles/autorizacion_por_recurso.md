# Autorización por Recurso (Object-Level Security)

Incluso si eres un "Editor", no deberías poder editar los artículos de *otros* editores. Aquí es donde el RBAC se queda corto y necesitamos **Autorización a Nivel de Objeto**.

## 1. El problema del "Acceso Horizontal"
Si solo compruebas el rol:
- Juan (Editor) -> Puede entrar en `PUT /articles/10`.
- Pero el Artículo 10 es de María.
- Juan acaba de hackear a María legalmente. Esto se conoce como **BOLA (Broken Object Level Authorization)** o **IDOR**.

## 2. Cómo solucionarlo en el Backend
La autorización no termina en el decorador de la ruta; debe continuar en la lógica de negocio.

### Opción A: En la Query SQL (Recomendado)
Es la forma más eficiente. No pidas el objeto y luego compruebes el dueño; pide el objeto *filtrando* por el dueño.
```python
# Mal
article = db.query(Article).get(id)
if article.owner_id != current_user.id: raise 403

# Bien
article = db.query(Article).filter(Article.id == id, Article.owner_id == current_user.id).first()
if not article: raise 404 # O 403 según tu política de privacidad
```

### Opción B: Capa de Servicio / Policy
Si la lógica es muy compleja (ej: puedes editar si eres el dueño O si eres el supervisor del departamento), encapsúlala en una función de "Política".
```python
def can_edit_article(user, article):
    if user.is_admin: return True
    if article.owner_id == user.id: return True
    if user.id in article.collaborators: return True
    return False
```

## 3. Seguridad en la Base de Datos (RLS)
Sistemas avanzados como PostgreSQL permiten **Row-Level Security (RLS)**. Puedes configurar la base de datos para que un usuario de DB específico solo pueda "ver" las filas que le pertenecen, independientemente de la query que lance el backend. Es la defensa definitiva.

## 4. Auditoría de Acceso
Cada vez que deniegues un acceso a un recurso, loguéalo. Un pico de errores 403 en un ID específico suele ser señal de que alguien está intentando un ataque de enumeración o robo de datos.

## Resumen: Sé granular
Un backend senior no solo pregunta "¿Quién eres?", sino "¿Tienes derecho a tocar ESTE dato exacto?". La autorización granular es la diferencia entre un sistema "que funciona" y un sistema que protege los datos de sus usuarios con responsabilidad.
