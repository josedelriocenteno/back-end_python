JSON en Backends: APIs, Config y Payloads
1️⃣ JSON como formato estándar

En aplicaciones backend modernas:

JSON es el formato más usado para intercambio de datos.

Se usa para:

Configuraciones de la aplicación (settings, credenciales, paths)

Payloads de APIs (requests y responses)

Almacenamiento temporal o cachés

Ventajas:

Legible para humanos

Ligero

Compatible con casi todos los lenguajes

Desventajas:

No soporta tipos complejos (datetime, objetos personalizados)

Debe validarse antes de usar

2️⃣ JSON en configuración de aplicaciones

Evitar hardcodear rutas, credenciales o parámetros en el código:

Ejemplo:

{
    "db_host": "localhost",
    "db_port": 5432,
    "debug": true,
    "allowed_hosts": ["localhost", "127.0.0.1"]
}


Buenas prácticas:

Guardar configuraciones en un archivo JSON separado (config.json).

Cargarlo al inicio de la aplicación con json.load().

Validar claves y tipos obligatorios.

Para entornos diferentes (dev/prod), usar archivos distintos o variables de entorno combinadas con JSON.

import json
from pathlib import Path

ruta_config = Path("config.json")
with ruta_config.open("r", encoding="utf-8") as f:
    config = json.load(f)

# Validación básica
required_keys = ["db_host", "db_port", "debug"]
for k in required_keys:
    if k not in config:
        raise ValueError(f"Falta clave en config: {k}")

3️⃣ JSON en APIs
a) Requests (entrada)

Cuando recibimos JSON de clientes o frontend:

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/usuario", methods=["POST"])
def crear_usuario():
    data = request.get_json()  # Convierte JSON a dict
    # Validar estructura
    required_keys = ["nombre", "edad"]
    for k in required_keys:
        if k not in data:
            return jsonify({"error": f"Falta {k}"}), 400
    return jsonify({"mensaje": "Usuario creado"}), 201


✅ Buenas prácticas:

Validar siempre la estructura y tipos.

Manejar JSON mal formado → devolver 400 (Bad Request)

No confiar en la entrada del cliente.

b) Responses (salida)

Devolver JSON estandarizado:

usuario = {"nombre": "Ana", "edad": 25}
return jsonify(usuario)  # Flask convierte dict a JSON


Recomendaciones:

Evitar objetos Python que no sean JSON serializable (datetime, set) → convertir antes.

Mantener consistencia en nombres de claves y formato.

Añadir metadata si es necesario (status, message, errors).

4️⃣ Errores comunes al usar JSON en backend

No validar la entrada → KeyError y crashes.

Escribir datos sensibles directamente → seguridad.

Envío de objetos no serializables → TypeError.

No usar UTF-8 → problemas con acentos o caracteres especiales.

No controlar versiones de API → cambios de esquema rompen clientes.

5️⃣ Buenas prácticas profesionales

Separar configuración y datos de negocio.

Validar siempre estructura y tipos de JSON entrante.

Serializar correctamente los tipos complejos (str(datetime) o librerías como pydantic).

Mantener estándares de naming en claves (snake_case recomendado).

Logging de errores de parsing y validación para debug.

Documentar esquemas JSON usados en endpoints (OpenAPI/Swagger).

6️⃣ Resumen

JSON es estándar en backend, pero requiere disciplina.

Validación + manejo de errores = backend robusto.

Separar config / payload / logs para evitar errores y malas prácticas.

Usar herramientas modernas para validación y documentación mejora la confiabilidad.