import pathlib

DEFAULT_CONFIG = {
    "database": {
        "db": "snadra",
        "password": "snadra",
        "user": "snadra",
        "port": 5432,
        "type": "postgres",
    }
}

CONFIG_DIR = pathlib.Path("~/.config/snadra/").expanduser()

DEFAULT_CONFIG_FILE_PATH = CONFIG_DIR / "snadra_config.toml"

DEFUALT_SQLITE_DB_PATH = CONFIG_DIR / "snadra_db.sqlite"
