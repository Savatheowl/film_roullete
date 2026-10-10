from src.app import app_run
from src.database import init_db


def main():
    init_db()
    app_run()


if __name__ == "__main__":
    main()
