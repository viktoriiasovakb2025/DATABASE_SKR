from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database_skr.database import Base

if TYPE_CHECKING:
    # Додано відступ для імпорту всередині блоку перевірки типів
    from database_skr.student import Student


class Faculty(Base):
    # Додано подвійні підкреслення __tablename__ та відступи для всього класу
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Зв'язок один-до-багатьох (один факультет — багато студентів)
    students: Mapped[list["Student"]] = relationship(back_populates="faculty")
