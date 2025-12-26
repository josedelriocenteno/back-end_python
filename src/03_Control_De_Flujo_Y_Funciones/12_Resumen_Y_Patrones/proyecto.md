# Proyecto Integral: Sistema de Gestión de Usuarios y Actividad en Línea

## Descripción general
Crear un **mini backend simulado** que gestione usuarios y registre actividad de manera eficiente.  
Este proyecto integra:

- **Estructuras de datos**: listas, diccionarios, sets, tuples.  
- **Control de flujo**: condicionales, bucles, comprehensions.  
- **Funciones**: básicas, avanzadas, puras, closures, decorators.  
- **Manejo de errores**: excepciones controladas, validaciones.  
- **Buenas prácticas**: tipado, docstrings, funciones inmutables, idempotencia.  
- **Patrones funcionales**: map/filter/reduce, pipelines limpios.

---

## Requisitos funcionales

### 1. Usuarios
- Cada usuario tiene: `id`, `nombre`, `email`, `edad`, `activo` (bool).  
- Almacenamiento: diccionario `{id: usuario}`.  
- Funcionalidades:
  - Crear usuario nuevo.
  - Editar usuario existente.
  - Eliminar usuario (marcar como inactivo, no borrar).
  - Listar usuarios activos y filtrados por edad.

### 2. Registro de actividad
- Acciones: `"login"`, `"logout"`, `"post"`.  
- Almacenamiento: diccionario de listas `{id_usuario: [acciones]}`.  
- Filtrado por tipo de acción y rango de fechas (`datetime`).

### 3. Validaciones
- Emails válidos (regex).  
- Evitar duplicados.  
- Edad mínima 13 años.  
- Errores mediante excepciones controladas.

### 4. Estadísticas y reportes
- Contar usuarios activos por edad.  
- Contar acciones más frecuentes (`collections.Counter`).  
- Listar usuarios más activos.

### 5. Funciones y patrones funcionales
- **Comprehensions** para filtrar y transformar datos.  
- **Funciones puras** para cálculos y estadísticas.  
- **Closures** para contadores de acciones.  
- **Decorators** para log o medir tiempo de ejecución.  
- **Funciones inmutables** donde sea posible (no modificar listas/diccionarios directamente).

### 6. CLI simulada
- Menú en terminal para:
  - Agregar, editar, eliminar, listar usuarios.
  - Registrar acciones.
  - Mostrar reportes.

---

## Bonus / Nivel profesional
- Funciones **idempotentes** para registro de acciones.  
- Persistencia en archivos (CSV/JSON) para usuarios y actividad.  
- Tipado completo y **docstrings claros**.  
- Función de **pipeline de actividad**: filtra, cuenta, ordena y devuelve datos listos para frontend o análisis.

---

## Objetivos de aprendizaje
Al finalizar, habrás practicado:

- Estructuras de datos y patrones de uso reales.  
- Control de flujo limpio y comprensible.  
- Funciones avanzadas: args/kwargs, closures, decorators, funciones puras.  
- Manejo profesional de errores y validaciones.  
- Patrones funcionales aplicados a pipelines y datos.  
- Integración de todo lo visto en un proyecto tipo backend real.
