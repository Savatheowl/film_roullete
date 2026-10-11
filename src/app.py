from flask import Flask, jsonify

from src.config import Config
from src.database import init_db

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG
app.json.ensure_ascii = False



@app.route("/")
def index():
    return jsonify({"message": "Привет, народ!"})



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
