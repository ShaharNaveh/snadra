from _snadra.config.constants import DEFAULT_CONFIG_FILE_PATH
from _snadra.config.utils import get_config

state = {
    # TODO: make this recive the path from the cli
    "config": get_config(path=DEFAULT_CONFIG_FILE_PATH),
    "current_workspace": "default",
}
