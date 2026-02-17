"""
SQLALCHEMY ORM: DEFINICIÓN DE MODELOS (DECLARATIVE)
-----------------------------------------------------------------------------
El ORM nos permite definir tablas usando clases de Python. SQLAlchemy 2.0 
introduce el estilo 'Mapped' y 'mapped_column' para mejor soporte de tipado.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. CLASE BASE
# Todos tus modelos deben heredar de una clase base que hereda de DeclarativeBase.
class Base(DeclarativeBase):
    pass

# 2. MODELO DE USUARIO
class User(Base):
    __tablename__ = "users" # Nombre físico de la tabla

    # Estilo Moderno (SQLAlchemy 2.0 + Typing)
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(100)) # Opcional -> Nullable
    
    # Campo con valor por defecto en servidor
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relación (Lógica, no es una columna física)
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

# 3. MODELO DE POSTS
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'Mapped[T]' ayuda a los IDEs (VSCode/PyCharm) a saber el tipo del atributo.
2. 'mapped_column' es donde definimos los detalles de SQL (length, unique, etc).
3. 'Base' es el pegamento que permite a SQLAlchemy trackear todos tus modelos.
4. Las relaciones no son columnas, son "atajos" para navegar entre objetos Python.
"""
