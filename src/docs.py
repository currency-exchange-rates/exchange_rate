from typing import Any

from flask import Flask
from flask_restx import Api, fields


def create_api(app: Flask) -> tuple[Api, Any, Any]:
    """Создание экземпляра API. Описание моделей ответов."""
    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Добавьте ключ в формате: Bearer <ваш API ключ>",
        }
    }

    api = Api(
        app,
        title="Exchange Rate API",
        version="1.0",
        description="API для работы с валютными курсами",
        doc="/swagger",
        prefix="/api/v1",
        authorizations=authorizations,
        security="apikey",
    )

    exchange_rate_model = api.model(
        "ExchangeRate",
        {
            "base_currency": fields.String(
                description="Базовая валюта",
                example="USD"
            ),
            "rates": fields.Raw(
                description="Курсы валют относительно базовой",
                example={
                    "AED": 3.6725,
                    "AFN": 70.2515,
                    "ALL": 94.5439,
                    "AMD": 395.2367,
                    "ANG": 1.79,
                    "AOA": 925.3915,
                    "ARS": 1025.42,
                    "AUD": 1.5996,
                    "AWG": 1.79,
                    "AZN": 1.7,
                    "BAM": 1.8751,
                    "BBD": 2,
                    "BDT": 119.505,
                    "BGN": 1.8752,
                    "BHD": 0.376,
                    "BIF": 2954.1185,
                    "BMD": 1,
                    "BND": 1.3563,
                }
            ),
            "rates": fields.Raw(description="Курсы валют относительно базовой"),
        },
    )

    conversion_model = api.model(
        "ConversionResult",
        {
            "conversion_result": fields.Float(
                description="Результат конвертации",
                example=8.29
            ),
        },
    )

    return api, exchange_rate_model, conversion_model
