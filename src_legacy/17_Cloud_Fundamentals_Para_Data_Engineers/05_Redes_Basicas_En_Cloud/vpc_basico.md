# VPC: El centro de datos virtual

Una **VPC (Virtual Private Cloud)** es tu propia red privada dentro de Google Cloud. Es como tener un centro de datos físico con sus cables y switches, pero definido totalmente por software.

## 1. Aislamiento Total
Los recursos dentro de tu VPC (como bases de datos o máquinas virtuales) están aislados del resto de internet y de otros usuarios de Google Cloud. Solo pueden hablar entre ellos según las reglas que tú definas.

## 2. Redes Globales
A diferencia de otros proveedores de nube, una VPC de Google es **Global**. Puedes tener una red que se extienda por todo el mundo, permitiendo que una máquina en Madrid hable con una en Singapur a través de la fibra privada de Google sin pasar por el internet público.

## 3. El Proyecto y la VPC
Por defecto, cada proyecto nuevo tiene una red llamada `default`. No la uses para producción.
- **Mejor práctica:** Crea una VPC personalizada (`custom mode`). Esto te da control total sobre el direccionamiento IP.

## 4. Tipos de Tráfico
- **Ingress (Entrada):** Tráfico que viene de fuera hacia tus recursos. Google lo bloquea casi todo por defecto por seguridad.
- **Egress (Salida):** Tráfico que sale de tus recursos hacia internet. Google lo permite todo por defecto para facilitar las actualizaciones.

## 5. El rol del Data Engineer
Aunque parezca un tema de IT/Sistemas, entender la VPC es vital para:
- Conectar tu pipeline de Python a una base de datos privada.
- Acceder a APIs internas de la empresa.
- Asegurar que tus datos no viajen por redes inseguras.

## Resumen: Tu Casa en la Nube
La VPC es el perímetro que protege tus recursos. Una VPC bien configurada es la primera línea de defensa contra ataques externos y la base para una comunicación rápida y fluida entre tus servicios de datos.
