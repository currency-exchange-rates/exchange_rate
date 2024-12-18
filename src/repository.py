from typing import Any
from flask_sqlalchemy import SQLAlchemy

from src.models import Currency
from src.schemas import (
    CurrencySchemaCreate,
    CurrencySchemaDB,
    CurrencySchemaUpdate
)


class RepositoryCurrency:
    """CRUD операции для модели Currency."""

    model = Currency

    def __init__(self, db: SQLAlchemy):
        """Инициализация репо."""
        self.session = db.session

    def get(
        self,
        obj_id: int,
    ) -> Currency:
        """Получение одного объекта по id."""
        db_obj = self.model.query.where(self.model.id == obj_id)
        return db_obj.first()

    def get_multi(self):
        """Получение всех объектов из бд."""
        return self.model.query.all()

    def create(
        self,
        obj_in: CurrencySchemaCreate,
    ) -> Currency:
        """Создание объекта."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_obj: CurrencySchemaDB,
        obj_in: CurrencySchemaUpdate,
    ) -> Currency:
        """Обновление объекта."""
        obj_data = db_obj
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db_obj: CurrencySchemaDB,
    ) -> CurrencySchemaDB:
        """Удаление объекта из бд"""
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj

    def get_obj_for_field_arg(
        self,
        field: str,
        arg: Any,
        many: bool
    ) -> Currency | list[Currency]:
        """Получение объекта/объектов по имени поля и аргументу."""
        db_obj = self.model.query.where(getattr(self.model, field) == arg)
        if many:
            return db_obj.all()
        return db_obj.first()
