from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

app: Flask = Flask(settings.app_name)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
