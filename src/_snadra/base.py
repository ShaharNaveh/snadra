from _snadra.app import SnadraApplication
from _snadra.config import config_file_location

config_file = config_file_location()
app = SnadraApplication(config_file=config_file)
