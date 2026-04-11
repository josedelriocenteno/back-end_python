# Naming Convention: Tests que cuentan una historia

El nombre de un test es su documentación. Cuando un test falla en una pipeline de CI/CD a las 3 de la mañana, el nombre debe decirle al ingeniero exactamente qué se ha roto sin necesidad de abrir el código.

## 1. El anti-patrón "Test + Nombre Función"
- **Mal:** `test_login()`
- **Problema:** Si falla, ¿qué ha fallado? ¿la contraseña mal? ¿el usuario no existe? ¿el servidor caído?

## 2. El patrón "Escenario - Estímulo - Respuesta"
Un buen nombre Senior suele seguir esta estructura:
`test_[escenario]_[accion]_[resultado_esperado]`

- **Ejemplo:** `test_login_with_invalid_password_returns_401_unauthorized`
- **Ejemplo:** `test_calculate_total_adds_tax_correctly_when_country_is_spain`

## 3. Uso de Docstrings
Si el nombre es demasiado largo, puedes usar el docstring de la función para explicar el "por qué" o enlazar a un ticket de Jira/GitHub.
```python
def test_user_cannot_buy_without_credits():
    """
    REQ-402: Un usuario con balance 0 debe ser redirigido 
    a la página de recarga.
    """
    ...
```

## 4. Nombres de Variables dentro del Test
- No uses `a`, `b`, `c`. 
- Usa `expected_price`, `input_payload`, `mock_response`.
- El código de test debe ser el código más legible de todo tu proyecto.

## 5. Organización por Clases (Opcional)
Puedes agrupar tests relacionados en clases para compartir una descripción común.
```python
class TestWithdrawalLogic:
    def test_insufficient_funds(self): ...
    def test_exceeds_daily_limit(self): ...
    def test_account_frozen(self): ...
```

## Resumen: Hablar claro
Un desarrollador senior escribe tests para humanos, no para máquinas. Un nombre de test descriptivo ahorra horas de debugging y facilita enormemente la comunicación dentro del equipo de ingeniería.
