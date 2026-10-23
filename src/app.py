import asyncio
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.api_fetcher import get_film_list
from src.config import Config
from src.database import db_health_status_message, get_all_genres, init_db

app = Flask(
    import_name=__name__,
    template_folder=Path("../templates"),
    static_folder=Path("../static"),
)
app.config.from_object(Config)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG
app.json.ensure_ascii = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/roulette")
def roulette_page():
    return render_template("roulette.html")


@app.route("/genres")
def genres():
    result = []
    for genre in get_all_genres():
        result.append(
            {
                "id": genre.id,
                "tmdb_id": genre.tmdb_id,
                "name": genre.name_en,
                "name_ru": genre.name_ru,
            }
        )
    return jsonify(result)


@app.route("/films")
def films():
    genre_id = request.args.get('genre', type=int)
    sort_by = request.args.get('sort', default='popularity.desc')
    page = request.args.get('page', type=int, default=1)

    data = asyncio.run(get_film_list(include_adult=True, language="ru", page=page, sort_by=sort_by, genre_id=genre_id))
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
