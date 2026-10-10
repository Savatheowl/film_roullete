from flask import Flask, jsonify
from src.database import _get_engine
from src.database import Base, User
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['DEBUG'] = Config.DEBUG
app.json.ensure_ascii = False

with app.app_context():
    engine = _get_engine()
    Base.metadata.create_all(engine)
    print("Таблицы созданы (или уже существуют)")


@app.route('/')
def index():
    return jsonify({"message": "Сервер работает"})


if __name__ == '__main__':
    app.run(debug=True)