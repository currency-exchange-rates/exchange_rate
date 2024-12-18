from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent
ENV_PATH: Final[Path] = BASE_DIR / ".env"
CURRENCY_JSON_DATA: Final[Path] = BASE_DIR / "currency.json"

DATE_FORMAT: Final[str] = "%Y-%m-%d"

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'
