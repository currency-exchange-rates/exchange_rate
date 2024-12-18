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
        doc="/api-docs",
        prefix="/api/v1",
        authorizations=authorizations,
        security="apikey",
    )

    exchange_rate_model = api.model(
        "ExchangeRate",
        {
            "base_currency": fields.String(
                description="Базовая валюта", example="USD"
            ),
            "rates": fields.Raw(description="Курсы валют относительно базовой"),
        },
    )

    conversion_model = api.model(
        "ConversionResult",
        {
            "conversion_result": fields.Float(
                description="Результат конвертации", example=8.29
            ),
        },
    )

    return api, exchange_rate_model, conversion_model
