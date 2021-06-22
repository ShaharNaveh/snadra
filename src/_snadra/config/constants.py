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

DEFAULT_CONFIG_FILE_PATH = pathlib.Path(
    "~/.config/snadra/snadra_config.toml"
).expanduser()
