from flask import Flask, request
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


@app.route('/convert', methods=['GET'])
def get_pair_amount():
    base_code = request.args.get('base_currency')  # получаем с фронта
    target_code = request.args.get('target_currency')  # получаем с фронта
    amount = request.args.get('amount')  # получаем с фронта
    url = app.config['EXCHANGE_API_URL_PAIR'].format(api_key=app.config['API_KEY']) # noqa
    full_url = f"{url}{base_code}/{target_code}/{amount}"
    response = requests.get(full_url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
