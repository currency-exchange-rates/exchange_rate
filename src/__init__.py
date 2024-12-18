from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

app = Flask(settings.app_name)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url


class Base(DeclarativeBase):
    """Базовый класс для бд."""
    pass


db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)

from src import views  # noqa
