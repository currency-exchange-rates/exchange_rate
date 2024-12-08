from flask import Flask, request, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

currencies = ['USD', 'EUR', 'GBP']


@app.route('/exchange-rates/<string:base_currency>')
def get_exchange_rates(base_currency):
    url = app.config['EXCHANGE_API_URL_LATEST'].format(api_key=app.config['API_KEY']) # noqa
    response = requests.get(url + base_currency)
    data = response.json()
    return data

# Пример запроса curl:
# curl "http://127.0.0.1:5000/?base_currency=EUR&target_currency=GBP&amount=10"
@app.route('/')
def get_pair_amount():
    """Возвращает значение конвертированного количества валюты."""
    base_currency = request.args.get('base_currency')  # получаем с фронта
    target_currency = request.args.get('target_currency')  # получаем с фронта
    amount = request.args.get('amount')  # получаем с фронта
    url = app.config['EXCHANGE_API_URL_PAIR'].format(api_key=app.config['API_KEY']) # noqa
    full_url = f"{url}{base_currency}/{target_currency}/{amount}"
    response = requests.get(full_url)
    data = response.json()
    conversion_result = data.get("conversion_result")
    return jsonify({"conversion_result": float(conversion_result)})


if __name__ == '__main__':
    app.run(debug=True)
