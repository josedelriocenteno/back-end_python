# SQL desde Python: ¿Por qué no todo es ORM?

En el desarrollo Backend moderno, existe una tensión constante entre la comodidad del ORM (Object-Relational Mapper) y el control total del SQL puro. Para ser un desarrollador senior, debes entender cuándo usar cada herramienta.

## 1. El Espectro del Acceso a Datos

Podemos interactuar con la base de datos en tres niveles principales:

1.  **SQL Puro (Drivers):** Uso directo de `psycopg` o `asyncpg`. Envías strings SQL y recibes tuplas/diccionarios.
2.  **SQL Expresivo (Core):** Usas un lenguaje de expresiones (como SQLAlchemy Core) para construir queries programáticamente sin mapearlas a objetos.
3.  **ORM:** Mapeas tablas a clases de Python. Manipulas objetos y el ORM genera el SQL por ti.

## 2. Por qué aprender SQL "Puro" si existen los ORMs

A pesar de la popularidad de frameworks como Django o FastAPI + SQLAlchemy, el SQL puro sigue siendo vital por varias razones:

*   **Rendimiento Crítico:** Los ORMs añaden una capa de abstracción (overhead) que puede ser lenta en operaciones masivas.
*   **Funcionalidades Avanzadas:** Hay características de PostgreSQL (como Window Functions complejas, Recursive CTEs o extensiones específicas) que son difíciles o imposibles de expresar elegantemente en un ORM.
*   **Depuración:** Para entender por qué una query va lenta, necesitas leer el SQL que el ORM está generando. Si no sabes SQL, estás ciego.
*   **Data Engineering:** En procesos ETL pesados, mover millones de registros fila a fila como "objetos Python" crasheará tu memoria. SQL puro (o batching) es la única opción.

## 3. El Problema de la "Fricción Objeto-Relacional"

Las bases de datos relacionales guardan datos en **tablas** (filas y columnas). Python guarda datos en **objetos** (clases y atributos).
Esta diferencia fundamental crea problemas:
*   En SQL no hay herencia, en Python sí.
*   En SQL las relaciones son IDs de Foreign Keys, en Python son referencias a otros objetos.

El acceso a datos profesional busca soluciones para "traducir" estos dos mundos de forma eficiente.

## 4. Cuándo NO usar un ORM

1.  **Reportes y Analítica:** Donde necesitas JOINs masivos y agregaciones complejas.
2.  **Scripts de Migración de Datos:** Donde la velocidad de inserción es lo más importante.
3.  **Microservicios Ultra-Ligeros:** Donde quieres minimizar el consumo de memoria y el tiempo de arranque.

## Resumen: La Herramienta Correcta para el Trabajo

Un desarrollador backend profesional no es "Team ORM" o "Team SQL". Es alguien que conoce ambos y elige la abstracción más alta posible que mantenga el rendimiento necesario. En este tema, aprenderemos a dominar todo el espectro, empezando por los fundamentos de `psycopg3`.
