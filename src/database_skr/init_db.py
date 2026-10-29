import random
from sqlalchemy import text
from database_skr.database import Base, SessionLocal, engine
from database_skr import models  # noqa: F401
from database_skr.student import Student


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        result = db.execute(text("SELECT COUNT(*) FROM students"))
        count = result.scalar_one()
        print(f"Кількість студентів у базі: {count}")
        existing_count = db.query(Student).count()
        missing_count = max(0, 50 - existing_count)

        if missing_count == 0:
            print(f"У базі вже є {existing_count} студентів.")
            return

        students = []

        for i in range(existing_count + 1, existing_count + missing_count + 1):
            students.append(
                Student(
                    full_name=f"Тестовий Студент {i}",
                    specialty="Кібербезпека",
                    course=random.randint(1, 4),
                    group=f"КБ-{random.randint(100, 199)}",
                    has_dormitory=random.choice([True, False]),
                )
            )

        db.add_all(students)
        db.commit()

        print(
            f"Додано {missing_count} студентів. "
            f"Загалом у базі: {existing_count + missing_count}."
        )


if __name__ == "__main__":
    init_db()