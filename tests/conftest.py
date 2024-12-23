from typing import Generator
import os
import sys
from pathlib import Path

import pytest
from flask import Flask
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

_user_environment = os.environ.copy()

from src import app # noqa


@pytest.fixture
def user_environment():
    return _user_environment


@pytest.fixture
def app_() -> Generator[Flask]:
    with app.app_context():
        yield app


@pytest.fixture
def client(app_: Flask):
    return app_.test_client()


@pytest.fixture
def cli_runner():
    return app.test_cli_runner()
