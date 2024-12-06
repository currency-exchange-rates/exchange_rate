from flask import Flask
import requests
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

currencies = ['USD', 'EUR', 'GBP']


@app.route('/exchange-rates/<string:base_currency>')
def get_exchange_rates(base_currency):
    url = app.config['EXCHANGE_API_URL'].format(api_key=app.config['API_KEY'])
    response = requests.get(url + base_currency)
    data = response.json()
    return data
    

if __name__ == '__main__':
    app.run(debug=True)