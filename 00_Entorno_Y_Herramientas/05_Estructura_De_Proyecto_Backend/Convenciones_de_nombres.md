# Convenciones de Nombres en Python Backend

## 1. Introducción

Usar **convenciones de nombres coherentes y claras** es fundamental para mantener un código legible, profesional y mantenible.  
Esto aplica a **variables, funciones, clases, módulos y paquetes**.

> ⚠️ Nota:
> No seguir convenciones provoca código confuso, errores silenciosos y dificultades al trabajar en equipo o con código legado.

---

## 2. Variables

### 2.1 Reglas generales
- Nombre descriptivo, corto pero claro.  
- Usar **snake_case**.  
- Evitar abreviaturas ambiguas.

### 2.2 Ejemplos

```python
# Correcto
user_name = "Juan"
total_amount = 100

# Incorrecto
un = "Juan"          # abreviatura confusa
TotalAmount = 100    # incorrecto, debería ser snake_case
3. Funciones y Métodos
3.1 Reglas generales
snake_case

Verbo + descripción clara de la acción

Evitar nombres genéricos como do_stuff o process_data

3.2 Ejemplos
python
Copiar código
# Correcto
def create_user(name: str, email: str):
    pass

def calculate_total_price(items: list):
    pass

# Incorrecto
def CreateUser():       # incorrecto: CamelCase para función
    pass

def process_data():     # demasiado genérico
    pass
4. Clases
4.1 Reglas generales
CamelCase (UpperCamelCase)

Nombre singular y descriptivo

Representa entidades, no acciones

4.2 Ejemplos
python
Copiar código
# Correcto
class User:
    pass

class OrderItem:
    pass

# Incorrecto
class user:       # incorrecto: minúscula
class order_item: # incorrecto: snake_case para clase
5. Constantes
5.1 Reglas generales
UPPER_CASE

Nombre descriptivo

Evitar abreviaturas

5.2 Ejemplos
python
Copiar código
# Correcto
MAX_RETRIES = 5
API_BASE_URL = "https://api.example.com"

# Incorrecto
max_retries = 5        # minúscula, no es constante
apiBaseUrl = "url"     # camelCase, incorrecto
6. Módulos y Paquetes
6.1 Reglas generales
snake_case para módulos (archivos .py)

lowercase para paquetes (carpetas)

Nombres cortos pero descriptivos

6.2 Ejemplos
bash
Copiar código
# Estructura de proyecto recomendada
app/
├── models/
│   └── user.py
├── services/
│   └── user_service.py
├── repositories/
│   └── user_repository.py
7. Variables y funciones privadas
Se indica con un guion bajo inicial _nombre

Evita el acceso desde fuera del módulo, aunque no es totalmente privado (convención de Python)

python
Copiar código
# Ejemplo
def _calculate_discount(price: float):
    return price * 0.1
8. Buenas prácticas profesionales
Seguir PEP8 como guía principal.

Nombres descriptivos y coherentes.

Mantener consistencia entre todos los módulos y paquetes del proyecto.

Evitar abreviaturas ambiguas.

Documentar cualquier convención especial usada en el proyecto.

9. Errores comunes a evitar
Mezclar estilos (snake_case y CamelCase).

Nombres genéricos o ambiguos (data, temp, stuff).

No diferenciar funciones de clases y constantes.

Ignorar convenciones del equipo o proyecto.

10. Checklist rápido
 Variables y funciones: snake_case

 Clases: CamelCase

 Constantes: UPPER_CASE

 Módulos: snake_case

 Paquetes: lowercase

 Variables privadas: prefijo _

 Consistencia en todo el proyecto

11. Conclusión
Seguir convenciones de nombres profesionales asegura que tu código sea legible, mantenible y consistente, facilitando colaboración en equipo y evitando errores.
No es solo estética: es una práctica de ingeniería profesional crítica.