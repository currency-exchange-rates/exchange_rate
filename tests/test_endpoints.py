from typing import Final

from flask.testing import FlaskClient

import pytest


DOC_URL: Final[str] = "/api-docs"
EXCHANGE_RATES: Final[str] = "/api/v1/exchange/exchange-rates/{}"
CONVERSION_RATE: Final[str] = (
    "/api/v1/exchange/?base_currency={}&target_currency={}&amount={}"
)
CONVERSION_RATE_INCORRECT: Final[str] = (
    "/api/v1/exchange/"
)
CONVERSION_RATE_INCORRECT_2: Final[str] = (
    "/api/v1/exchange/?base_currency={}"
)
CONVERSION_RATE_INCORRECT_3: Final[str] = (
    "/api/v1/exchange/?target_currency={}"
)
CONVERSION_RATE_INCORRECT_4: Final[str] = (
    "/api/v1/exchange/?amount={}"
)
CONVERSION_RATE_INCORRECT_5: Final[str] = (
    "/api/v1/exchange/?base_currency={}&target_currency={}"
)
CONVERSION_RATE_INCORRECT_6: Final[str] = (
    "/api/v1/exchange/?target_currency={}&amount={}"
)

USD: Final[str] = "USD"
EUR: Final[str] = "EUR"
AMOUNT: Final[str] = 100

INCORRECT_CODE: Final[str] = "INC"
INCORRECT_CODE_2: Final[str] = "INCORRECT"
INCORRECT_CODE_3: Final[str] = "i213i"
INCORRECT_CODE_4: Final[str] = INCORRECT_CODE.lower()

INCORRECT_AMOUNT: Final[str] = -100
INCORRECT_AMOUNT_2: Final[str] = "123D"
INCORRECT_AMOUNT_3: Final[str] = "ABV"


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
    response_data: dict = response.json
    assert response.status_code == 200, (
        f"При запросе на эндпоинт {url}, должен вернуться 200 статус."
    )
    assert base_currency_key in response_data, (
        f"В теле запроса должно быть поле {base_currency_key}"
    )
    assert conversion_rates_key in response_data, (
        f"В теле запроса должно быть поле {conversion_rates_key}"
    )
    assert response_data.get(base_currency_key) == USD, (
        f"В поле {base_currency_key}, должна быть валюта {USD}."
    )


@pytest.mark.parametrize(
    "code",
    (INCORRECT_CODE, INCORRECT_CODE_2, INCORRECT_CODE_3, INCORRECT_CODE_4)
)
def test_get_exchange_rates_incorrect_code(client: FlaskClient, code: str):
    url = EXCHANGE_RATES.format(code)
    response = client.get(url)
    assert response.status_code == 400, (
        f"При запросе на эндпоинт {url} с неккоректными данными должен "
        f"вернуться статус код 400, а вернулся {response.status_code}."
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


def test_convert_value_equal_currency(client: FlaskClient):
    url = CONVERSION_RATE.format(USD, USD, AMOUNT)
    response = client.get(url)

    convert_key = "conversion_result"

    assert response.status_code == 200, (
        f"При запросе на эндпоинт {url}, должен вернуться 200 статус."
    )
    assert convert_key in response.json, (
        f"В теле запроса должно быть поле {convert_key}"
    )
    rate_data = response.json.get(convert_key)
    assert rate_data == AMOUNT, (
        f"Результат конвертации должен равняться {rate_data} != {AMOUNT}"
    )


@pytest.mark.parametrize(
    "url",
    (
        CONVERSION_RATE_INCORRECT,
        CONVERSION_RATE_INCORRECT_2.format(USD),
        CONVERSION_RATE_INCORRECT_3.format(EUR),
        CONVERSION_RATE_INCORRECT_4.format(AMOUNT),
        CONVERSION_RATE_INCORRECT_5.format(EUR, USD),
        CONVERSION_RATE_INCORRECT_6.format(EUR, AMOUNT),
        CONVERSION_RATE.format(USD, EUR, INCORRECT_AMOUNT),
        CONVERSION_RATE.format(USD, EUR, INCORRECT_AMOUNT_2),
        CONVERSION_RATE.format(USD, EUR, INCORRECT_AMOUNT_3),
        CONVERSION_RATE.format(INCORRECT_CODE, EUR, INCORRECT_AMOUNT),
        CONVERSION_RATE.format(INCORRECT_CODE, EUR, AMOUNT),
        CONVERSION_RATE.format(INCORRECT_CODE, INCORRECT_CODE_2, AMOUNT),
        CONVERSION_RATE.format(EUR, INCORRECT_CODE_2, AMOUNT),
        CONVERSION_RATE.format(EUR, INCORRECT_CODE_2, INCORRECT_AMOUNT),
        CONVERSION_RATE.format(USD, EUR, ""),
        CONVERSION_RATE.format(USD, "", AMOUNT),
        CONVERSION_RATE.format("", EUR, AMOUNT),
    )
)
def test_convert_value_incorrect_params(
    client: FlaskClient,
    url: str
):
    response = client.get(url)
    assert response.status_code == 400, (
        f"При запросе на эндпоинт {url}, должен вернуться 400 статус."
    )
