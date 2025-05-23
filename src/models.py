from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_favorite_planet = Table(
    "user_favorite_planet",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
)


user_favorite_character = Table(
    "user_favorite_character",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_characters: Mapped[List["Character"]] = relationship(
        secondary='user_favorite_character', back_populates="character_fans")
    favorite_planets: Mapped[List["Planet"]] = relationship(
        secondary='user_favorite_planet', back_populates="planet_fans")


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[str] = mapped_column(String(120), nullable=False)

    planet_fans: Mapped[List["User"]] = relationship(
        secondary='user_favorite_planet', back_populates="favorite_planets")


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    homeworld: Mapped[str] = mapped_column(ForeignKey("planet.id"))
    planet : Mapped["Planet"] = relationship("Planet", )

    starship_id: Mapped[int] = mapped_column(ForeignKey("starship.id"))
    starship:    Mapped["Starship"] = relationship(
        "Starship",
        back_populates="crew_members",
    )

    character_fans: Mapped[List["User"]] = relationship(
        secondary='user_favorite_character', back_populates="favorite_characters")


class Starship(db.Model):
    __tablename__ = "starship"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    crew_members: Mapped[List["Character"]] = relationship(
        "Character",
        back_populates="starship"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
