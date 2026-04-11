"""
EJERCICIOS PRÁCTICOS DE SEGURIDAD (THINK LIKE A HACKER)
-----------------------------------------------------------------------------
Resuelve estos casos hipotéticos para demostrar tu nivel Senior.
"""

# CASO 1: EL DESARROLLADOR DESPISTADO
def vulnerable_function(user_id, new_email):
    # ¿Qué error de seguridad hay aquí?
    # db.execute(f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}")
    pass

# CASO 2: EL TOKEN ETERNO
def jwt_configuration():
    # ¿Es seguro un ACCESS_TOKEN con expiración de 365 días?
    # ¿Por qué sí o por qué no?
    pass

# CASO 3: MASS ASSIGNMENT
def process_user_registration(user_json: dict):
    # Si el JSON trae 'is_admin': true, ¿cómo evitas que se guarde en la DB?
    # Pista: Pydantic Roles.
    pass

# CASO 4: IDOR EN LA VIDA REAL
def delete_invoice(invoice_id: int, current_user_id: int):
    # Escribe el pseudo-código de la consulta SQL que borra la factura de 
    # forma segura, asegurando que solo el dueño puede borrarla.
    pass

# CASO 5: GESTIÓN DE SECRETOS
# Un junior te pregunta: "¿Por qué no puedo poner la API Key de Stripe en el 
# código si el repositorio es privado?". Dale 3 razones técnicas.

"""
TAREA FINAL:
Revisa uno de tus proyectos anteriores y pásale 'Bandit' y 'Safety'. 
Analiza los resultados y genera un plan de remediación basado en el 
Tema 11 de este curso.
"""
