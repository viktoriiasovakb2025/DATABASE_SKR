import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    specialty: str = Field(min_length=2, max_length=100)
    course: int = Field(ge=1, le=6)
    group: str = Field(min_length=2, max_length=20)
    has_dormitory: bool = False

    # Тепер ці валідатори знаходяться всередині класу StudentCreate
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not re.fullmatch(r"[А-ЯІЇЄҐа-яіїєґA-Za-z\s'-]+", value):
            raise ValueError("Ім'я може містити лише літери, пробіли та дефіс")
        return value

    @field_validator("group")
    @classmethod
    def validate_group(cls, value: str) -> str:
        if not re.fullmatch(r"[А-ЯІЇЄҐ]{2,4}-\d{2,3}", value):
            raise ValueError("Некоректний формат групи, наприклад КБ-11")
        return value


class StudentResponse(StudentCreate):
    id: int

    # Конфігурація має бути всередині класу, який повертає дані з БД
    model_config = ConfigDict(from_attributes=True)