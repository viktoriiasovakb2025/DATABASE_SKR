from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database_skr.database import Base

if TYPE_CHECKING:
    # Додано відступ для імпорту всередині блоку перевірки типів
    from database_skr.student import Student


class Subject(Base):
    # Виправлено: додано подвійні підкреслення для __tablename__ та відступи для всього класу
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Зв'язок багато-до-багатьох, який посилається на таблицю-посередник рядком
    students: Mapped[list["Student"]] = relationship(
        secondary="student_subjects",
        back_populates="subjects",
    )