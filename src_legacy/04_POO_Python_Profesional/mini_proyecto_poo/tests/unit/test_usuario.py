import pytest
import sys
import os
from pathlib import Path

# Añadir src al PYTHONPATH para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.domain.value_objects.id_value import IDValue
from src.domain.entities.usuario import Usuario

class TestUsuario:
    """Tests unitarios Usuario"""
    
    def test_creacion_usuario_valido(self):
        usuario_id = IDValue['Usuario'].generar()
        usuario = Usuario(
            id=usuario_id,
            nombre="Ana López",
            email="ana@tienda.com"
        )
        assert usuario.nombre == "Ana López"
        assert usuario.email == "ana@tienda.com"
    
    def test_str_repr_correcto(self):
        usuario = Usuario(
            IDValue['Usuario'].generar(),
            "Juan Pérez",
            "juan@test.com"
        )
        assert "Juan Pérez" in str(usuario)
        assert "juan@test.com" in str(usuario)
    
    def test_cambiar_nombre_inmutable(self):
        usuario_original = Usuario(
            IDValue['Usuario'].generar(),
            "Ana",
            "ana@test.com"
        )
        usuario_modificado = usuario_original.cambiar_nombre("Ana María")
        
        assert usuario_original.nombre == "Ana"
        assert usuario_modificado.nombre == "Ana María"
        assert usuario_original is not usuario_modificado
    
    def test_nombre_vacio_error(self):
        with pytest.raises(ValueError, match="al menos 2 caracteres"):
            Usuario(
                IDValue['Usuario'].generar(),
                "",
                "test@test.com"
            )
    
    def test_nombre_1_caracter_error(self):
        with pytest.raises(ValueError, match="al menos 2 caracteres"):
            Usuario(
                IDValue['Usuario'].generar(),
                "A",
                "test@test.com"
            )
    
    def test_nombre_muy_largo_error(self):
        nombre_largo = "A" * 101
        with pytest.raises(ValueError, match="muy largo"):
            Usuario(
                IDValue['Usuario'].generar(),
                nombre_largo,
                "test@test.com"
            )
    
    def test_email_sin_arroba_error(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                IDValue['Usuario'].generar(),
                "Ana",
                "invalido"
            )
    
    def test_email_dominio_invalido_error(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                IDValue['Usuario'].generar(),
                "Ana",
                "ana@dominio"
            )
    
    def test_usuarios_diferentes(self):
        id1 = IDValue['Usuario'].generar()
        id2 = IDValue['Usuario'].generar()
        
        u1 = Usuario(id1, "Ana", "ana@test.com")
        u2 = Usuario(id2, "Ana", "ana@test.com")
        
        assert u1 != u2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
