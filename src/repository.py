from typing import Any
from flask_sqlalchemy import SQLAlchemy

from src.models import Currency


class RepositoryCurrency:
    """Base CRUD operations in current application."""
    model = Currency

    def __init__(self, db: SQLAlchemy):
        """Init repository."""
        self.session = db.session

    def get(
        self,
        obj_id: int,
    ):
        """Get one item model for id."""
        db_obj = self.model.query.where(self.model.id == obj_id)
        return db_obj.first()

    def get_multi(self):
        """Get all items model."""
        return self.model.query.all()

    def create(
        self,
        obj_in,
    ):
        """Create item model for id."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_obj,
        obj_in,
    ):
        """Update item model for id."""
        obj_data = db_obj
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db_obj,
    ):
        """Delete item model for id."""
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj

    def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        """Get model for keyword argument."""
        db_obj = self.model.query.where(getattr(self.model, field) == arg)
        if many:
            return db_obj.all()
        return db_obj.first()
