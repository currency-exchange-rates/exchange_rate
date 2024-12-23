from flask.testing import FlaskClient


TEST_BASE_URL = 'http://localhost'
DOC_URL = "/api-docs"
EXCHANGE_RATES = "/api/v1/exchange/exchange-rates/{}"
CONVERSION_RATE = (
    "/api/v1/exchange/?base_currency={}&target_currency={}&amount={}"
)

USD = "USD"
EUR = "EUR"
AMOUNT = 100


def test_work_app(client: FlaskClient):
    response = client.get(DOC_URL)
    assert response.status_code == 200, (
        f"При запросе на эндпоинт {DOC_URL}, должен вернуться 200 статус."
    )


def test_get_exchange_rates(client: FlaskClient):
    url = EXCHANGE_RATES.format(USD)
    base_currency_key = "base_currency"
    conversion_rates_key = "conversion_rates"

    response = client.get(url)
    assert response.status_code == 200, (
        f"При запросе на эндпоинт {url}, должен вернуться 200 статус."
    )
    assert base_currency_key in response.json, (
        f"В теле запроса должно быть поле {base_currency_key}"
    )
    assert conversion_rates_key in response.json, (
        f"В теле запроса должно быть поле {conversion_rates_key}"
    )
    assert response.json.get(base_currency_key) == USD, (
        f"В поле {base_currency_key}, должна быть валюта {USD}."
    )


def test_convert_value(client: FlaskClient):
    response = client.get(EXCHANGE_RATES.format(USD))
    response_data: dict[str, str] = response.json
    rate = response_data.get("conversion_rates").get(EUR) * AMOUNT

    url = CONVERSION_RATE.format(USD, EUR, AMOUNT)
    response = client.get(url)

    convert_key = "conversion_result"

    assert response.status_code == 200, (
        f"При запросе на эндпоинт {url}, должен вернуться 200 статус."
    )
    assert convert_key in response.json, (
        f"В теле запроса должно быть поле {convert_key}"
    )
    rate_data = response.json.get(convert_key)
    assert rate_data == rate, (
        f"Результат конвертации должен равняться {rate_data} != {rate}"
    )
