from src import db

from sqlalchemy import Integer, Float, String, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class Currency(db.Model):
    """Модель валюты."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Автосоздание имени таблицы."""
        cls.__name__: str
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="Айди в базе данных",
    )
    code: Mapped[str] = mapped_column(
        String(3),
        CheckConstraint("LENGTH(name) == 3", name="check_len_code"),
        unique=True,
        nullable=False,
        comment="Код валюты для API, обязателен, длина кода ровно 3 символа",
    )
    name: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint("LENGTH(name) <= 50", name="check_len_name"),
        unique=True,
        nullable=False,
        comment="Название валюты, обязателен, длина имени до 50 символов",
    )
    country: Mapped[str] = mapped_column(
        String(100),
        CheckConstraint("LENGTH(name) <= 100", name="check_len_country"),
        unique=False,
        nullable=False,
        comment="Страна, обязательно, длина имени страны до 100 символов",
    )

    def __repr__(self) -> str:
        """Строковая репрезентация объекта."""
        return f"Currency {self.code} - {self.name}"


class CurrencyConversionRate(db.Model):
    """Модель для данных конвертации по курсу валют."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Автосоздание имени таблицы."""
        cls.__name__: str
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="Айди в базе данных",
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currency.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Поле айди валюты"
    )
    conversion_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currency.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Поле обменной валюты"
    )
    rate: Mapped[float] = mapped_column(
        Float,
        CheckConstraint(
            "rate > 0",
            name="not_equal_currency_obj"
        ),
        nullable=False,
        comment="Обменный курс валюты.",
    )
