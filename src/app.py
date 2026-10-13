from flask import Flask, jsonify

from src.config import Config
from src.database import init_db, db_health_status_message, get_all_genres
from src.api_fetcher import get_film_list
import asyncio

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG
app.json.ensure_ascii = False


@app.route("/")
def index():
    return jsonify({"message": "Привет, народ!"})


@app.route("/genres")
def genres():
    result = []
    for genre in get_all_genres():
        result.append({
            "id": genre.id,
            "tmdb_id": genre.tmdb_id,
            "name": genre.name_en,
            "name_ru": genre.name_ru,
        })
    return jsonify(result)


@app.route("/films")
def films():
    data = asyncio.run(get_film_list(
        include_adult=True,
        language="ru",
        page=1
    ))
    return jsonify(data)


@app.route("/health")
def health_flask():
    return jsonify({"message": "Сервер работает"})


@app.route("/health/db")
def health_db():
    return jsonify({"message": db_health_status_message()})


def app_run() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    init_db()
    app_run()
