"""
SQLALCHEMY ORM: RELACIONES AVANZADAS
-----------------------------------------------------------------------------
Cómo manejar One-to-Many, Many-to-One y Many-to-Many con elegancia.
"""

from typing import List
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .modelos_orm import Base

# 1. MANY-TO-MANY (M:N)
# Necesitamos una tabla asociativa intermedia.
user_group_association = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True)
)

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # Relación M:N usando 'secondary'
    members: Mapped[List["User"]] = relationship(
        secondary=user_group_association,
        back_populates="groups"
    )

class User(Base):
    __tablename__ = "users_v2" # Solo ejemplo
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()

    groups: Mapped[List["Group"]] = relationship(
        secondary=user_group_association,
        back_populates="members"
    )

# 2. OPCIONES DE RELACIÓN IMPORTANTES
# cascade: Qué pasa con los hijos si el padre se borra (delete, save-update).
# lazy: Cómo se cargan los datos (visto en el siguiente archivo .md).

class Parent(Base):
    __tablename__ = "parent"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan" # Si borro el padre, borra los hijos
    )

class Child(Base):
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'back_populates' es mejor que 'backref' (más explícito y mejor tipado).
2. Las tablas asociativas M:N no suelen necesitar una clase propia a menos 
   que tengan columnas extra (ej: fecha_union).
3. 'cascade="all, delete-orphan"' es vital para mantener la higiene de la DB 
   desde el ORM.
"""
