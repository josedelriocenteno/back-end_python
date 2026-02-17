# Ejercicios Prácticos: Pon a prueba tus conocimientos

Te proponemos 3 ejercicios para que pongas en práctica los conceptos de este módulo. Intenta resolverlos antes de mirar las soluciones.

## Ejercicio 1: El Dilema del Formato
Tienes un dataset de 50GB en archivos CSV. Tu jefe se queja de que las consultas tardan 20 minutos y cuestan mucho dinero en la nube.
- **Tarea:** Describe los pasos técnicos para optimizar este almacenamiento. ¿Qué formato elegirías? ¿Qué particionado aplicarías? ¿Cómo lo harías con Python/PyArrow?

## Ejercicio 2: Diseño de Pipeline Idempotente
Debes bajar los pedidos de una API que a veces se corta. El script actual inserta duplicados si lo lanzas dos veces para la misma fecha.
- **Tarea:** Escribe el pseudocódigo o lógica de un proceso que sea seguro re-ejecutar. Incluye la estrategia de reintentos y el método de carga en el destino.

## Ejercicio 3: Modelado Dimensional
Una App de Delivery (tipo Glovo/UberEats) tiene datos de: Pedidos, Clientes, Repartidores, Restaurantes y Platos.
- **Tarea:** Diseña un Esquema Estrella. Identifica quiénes serían tus Hechos y quiénes tus Dimensiones. Elige 3 métricas críticas y 3 atributos por cada dimensión.

## Ejercicio Extra: Defensa del PII
Un cliente pide que se borren todos sus datos (GDPR). Sus datos están en un Data Lake de archivos Parquet inmutables organizados por fecha.
- **Tarea:** Explica qué arquitectura (Lakehouse/Database) facilitaría este borrado y cómo implementarías una estrategia de enmascaramiento para que los analistas no vean el email del cliente en el día a día.

---
**Nota:** Estos ejercicios no tienen una única respuesta correcta. Lo importante es que seas capaz de justificar tus decisiones basándote en los principios de ingeniería explicados en los temas anteriores.
