from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database_skr.database import Base

if TYPE_CHECKING:
    # Додано відступи для імпортів всередині блоку перевірки типів
    from database_skr.faculty import Faculty
    from database_skr.subject import Subject


class Student(Base):
    # Виправлено подвійні підкреслення та додано відступи для всього класу
    __tablename__ = "students"

    # Прибрано зайві Integer, String, Boolean (код став чистішим)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    group: Mapped[str] = mapped_column(String(20), nullable=False)
    has_dormitory: Mapped[bool] = mapped_column(default=False)

    # Зовнішній ключ для зв'язку з факультетом
    faculty_id: Mapped[int | None] = mapped_column(
        ForeignKey("faculties.id"),
        nullable=True,
    )

    # Зв'язок один-до-багатьох (багато студентів належать одному факультету)
    faculty: Mapped["Faculty | None"] = relationship(back_populates="students")

    # Зв'язок багато-до-багатьох із предметами
    subjects: Mapped[list["Subject"]] = relationship(
        secondary="student_subjects",
        back_populates="students",
    )