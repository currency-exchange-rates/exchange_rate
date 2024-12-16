import requests

from flask import Flask, request, jsonify
from flask_restx import Namespace, Resource
from config import Config
from docs import create_api

app = Flask(__name__)
app.config.from_object(Config)
api, exchange_rate_model = create_api(app)
exchange_ns = Namespace("exchange", description="Операции с валютами")
api.add_namespace(exchange_ns)


@exchange_ns.route("/exchange-rates/<string:base_currency>")
class ExchangeRates(Resource):
    """Класс для обработки запросов, связанных с актуальными курсами валют."""

    @api.doc(
        description="Получение актуальных курсов валют для базовой валюты",
        params={"base_currency": "Код базовой валюты (например, USD, EUR)"},
        security="apikey",
    )
    @api.response(200, "Успешный ответ", model=exchange_rate_model)
    def get(self, base_currency):
        """Получение актуальных курсов валют для заданной валюты."""
        url = app.config["EXCHANGE_API_URL_LATEST"].format(
            api_key=app.config["API_KEY"]
        )
        headers = {"Authorization": f"Bearer {app.config['API_KEY']}"}
        response = requests.get(url + base_currency, headers=headers)
        return response.json()


# Пример запроса curl:
# curl "http://127.0.0.1:5000/?base_currency=EUR&target_currency=GBP&amount=10"
@app.route("/")
def get_pair_amount():
    """Возвращает значение конвертированного количества валюты."""
    base_currency = request.args.get("base_currency")  # получаем с фронта
    target_currency = request.args.get("target_currency")  # получаем с фронта
    amount = request.args.get("amount")  # получаем с фронта
    url = app.config["EXCHANGE_API_URL_PAIR"].format(api_key=app.config["API_KEY"])
    full_url = f"{url}{base_currency}/{target_currency}/{amount}"
    response = requests.get(full_url)
    data = response.json()
    conversion_result = data.get("conversion_result")
    return jsonify({"conversion_result": float(conversion_result)})


# пример ответа:
# {
#   "conversion_result": 8.29
# }


if __name__ == "__main__":
    app.run(debug=True)
