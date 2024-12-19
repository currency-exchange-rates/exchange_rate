from pathlib import Path

from src import app, db
from src.utils import add_data_from_json


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        json_path: Path = Path(__file__).resolve().parent / "currency.json"
        add_data_from_json(json_path, db)
        app.run()
