# validacion.py

def es_numero(valor):
    """Verifica si el valor es un número (int o float)."""
    try:
        float(valor)
        return True
    except ValueError:
        return False

def es_email_valido(email):
    """Verifica si el valor tiene formato de email."""
    return "@" in email and "." in email

def es_palabra_valida(palabra):
    """Verifica si la palabra contiene solo letras."""
    return palabra.isalpha()
