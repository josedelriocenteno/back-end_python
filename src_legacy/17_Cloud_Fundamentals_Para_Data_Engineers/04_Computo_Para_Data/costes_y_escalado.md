# Costes y Escalado en Cómputo

Manejar el cómputo en la nube requiere entender cómo Google nos cobra y cómo podemos configurar los sistemas para que no gasten más de lo necesario.

## 1. Pago por Segundo
A diferencia de los data centers antiguos, en Cloud se factura por segundos. 
- Si tu Cloud Run tarda 45.2 segundos, pagas exactamente eso. No un minuto completo.

## 2. Sustained Use Discounts (SUD)
Si mantienes una Compute Engine encendida durante todo el mes (24/7), Google te aplica automáticamente un descuento de hasta el **30%** sobre el precio base. No tienes que hacer nada, se aplica solo.

## 3. Committed Use Discounts (CUD)
Si sabes que vas a usar X CPUs durante 1 o 3 años, puedes "prometerlo" a Google. 
- A cambio, recibes descuentos de hasta el **50-70%**. Útil solo para infraestructuras muy estables y consolidadas.

## 4. Auto-scaling (Escalado Automático)
Los **Managed Instance Groups (MIG)** en Compute Engine permiten definir reglas:
- "Si la CPU media sube del 70%, crea otra máquina".
- "Si la CPU baja del 30%, borra una máquina".
Esto asegura que nunca estés pagando por potencia que no usas.

## 5. Recomendaciones de Tamaño (Rightsizing)
Google monitoriza tus máquinas. Si tienes una máquina de 16GB de RAM pero solo usas 2GB, aparecerá un aviso en la consola: "Podrías ahorrar 20€/mes cambiando a una máquina más pequeña". 
- **Tip Senior:** Revisa estas recomendaciones una vez al mes. Es dinero gratis que vuelve al presupuesto del departamento.

## Resumen: Cómputo a Medida
La nube te da elasticidad. Usa el auto-escalado para las puntas de trabajo y las máquinas Preemptibles o los descuentos por compromiso para la carga base. Un Data Engineer que controla los costes es un activo estratégico para la empresa.
