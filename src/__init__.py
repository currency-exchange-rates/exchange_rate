from flask import Flask

from src.settings import settings

app = Flask(settings.app_name)

from src import views  # noqa
