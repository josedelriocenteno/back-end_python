# Amenazas en el Backend: ¿Qué atacan realmente?

Para defender un sistema, primero debemos entender cómo piensan y qué buscan los atacantes. En el backend, las amenazas no suelen ser "virus" feos, sino abusos de la lógica y de la infraestructura.

## 1. El "Botín" de Datos (Data Theft)
Es el objetivo número uno.
- **Credenciales:** Emails y passwords (para usarlos en otros sitios).
- **Datos PII (Personally Identifiable Information):** Nombres, direcciones, teléfonos.
- **Datos Financieros:** Números de tarjeta, historiales de transacciones.

## 2. Abuso de Recursos (Resource Exhaustion)
A veces el atacante no quiere tus datos, quiere tu hardware.
- **Minado de Cripto:** Infectar procesos backend para usar la CPU del servidor.
- **DDoS (Distributed Denial of Service):** Sobrecargar tus endpoints para tirar el servicio y pedir un rescate o dañar tu competencia.
- **Relay de Spam:** Usar tu servidor de correo para enviar millones de emails basura.

## 3. Elevación de Privilegios
El atacante entra como un usuario normal y busca una "grieta" para convertirse en administrador.
- **IDOR (Insecure Direct Object Reference):** Cambiar un `/api/users/me` por un `/api/users/1` y obtener los datos del admin.
- **Exploits de Kernel/Container:** Escapar del contenedor Docker para tomar el control del servidor físico.

## 4. Inyección de Código
Hacer que el servidor ejecute algo que no debería.
- **SQL Injection:** Modificar la query para "saltarse" el login.
- **Command Injection:** Lograr que el backend ejecute comandos de shell (`rm -rf /`).
- **Log Injection:** Escribir código malicioso en los logs que será ejecutado por el visualizador de logs del administrador.

## 5. Man-in-the-Middle (MitM)
Interceptar el tráfico entre el cliente y el servidor.
- **Fallo:** No usar HTTPS o usar certificados autofirmados.
- **Resultado:** Captura de tokens JWT y contraseñas "en el aire".

## Resumen: Una batalla constante
Las amenazas evolucionan cada día. Un sistema que era seguro hace 2 años puede ser vulnerable hoy debido a nuevos descubrimientos. La monitorización proactiva y el parcheado constante de dependencias son las únicas formas de mitigar estas amenazas de forma efectiva.
