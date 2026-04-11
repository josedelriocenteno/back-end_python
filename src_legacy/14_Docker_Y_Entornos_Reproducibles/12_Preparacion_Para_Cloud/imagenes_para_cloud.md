# Imágenes para la Nube: Optimizando el despliegue

En la nube, el tamaño y la seguridad de la imagen se traducen directamente en dinero (coste de transferencia) y tiempo de escalado.

## 1. El peso importa (Cold Starts)
Si tu imagen pesa 2GB y tienes un pico de tráfico, la nube tardará 3 minutos en descargar la imagen entes de poder servir a los usuarios.
- **Objetivo:** Imágenes por debajo de 200MB.
- **Técnica:** Multi-stage builds y uso de imágenes `.slim`.

## 2. Etiquetas (Tags) Inmutables
NUNCA despliegues con el tag `:latest`.
- **Por qué:** Si el despliegue falla y quieres hacer un rollback, ¿cómo sabes cuál era la versión anterior si todas se llaman `latest`?
- **Solución:** Usa el hash del commit de Git como tag (`mi-api:sha-8f2e1a`). Esto asegura trazabilidad total.

## 3. Logs en Formato JSON
Los sistemas de monitorización de la nube (CloudWatch, Stackdriver) prefieren recibir JSON por la terminal.
- Facilita la creación de alertas automáticas (ej: avisar si hay más de 5 errores 500 en 1 minuto).

## 4. Señales de terminación (SIGTERM)
Asegúrate de que tu aplicación de Python responde a la señal `SIGTERM` cerrando las conexiones a la DB rápidamente. 
- La nube enviará esta señal cada vez que quiera apagar tu contenedor para actualizar el servidor físico subyacente.

## 5. El archivo `.dockerignore` definitivo
Limpia todo lo que no sea necesario para la ejecución final.
```text
.git
.venv
tests/
docs/
*.pyc
.ipynb_checkpoints
.env
```

## Resumen: Una imagen esbelta
Una imagen para la nube debe ser minimalista, estar bien etiquetada y ser capaz de arrancar y morir de forma limpia y predecible. Esto reduce los costes operativos y mejora drásticamente la resiliencia de tu infraestructura.
