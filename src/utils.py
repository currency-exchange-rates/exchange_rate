from flask import abort


def validate_currency_code(value: str) -> str:
    """Валидация кода валюты."""
    if len(value) != 3:
        except_message = f"Код {value} должен быть длинной ровно 3 символа."
        abort(400, except_message)

    if not value.isupper():
        except_message = f"У кода {value} должны быть все заглавные символы."
        abort(400, except_message)

    if not (value.isascii() and value.isalpha()):
        except_message = (
            f"У кода {value} все символы должны быть Английской раскладки."
        )
        abort(400, except_message)

    return value


def validate_convert_value(value: str) -> str:
    """Валидация конвертируемого значения."""

    if (isinstance(value, str) and not value.isdigit()):
        except_message = (
            f"Конвертируемое число {value} должно быть числом."
        )
        abort(400, except_message)

    value = int(value)

    if value < 0:
        except_message = (
            f"Конвертируемое число {value} не должно быть меньше нуля."
        )
        abort(400, except_message)

    return value
