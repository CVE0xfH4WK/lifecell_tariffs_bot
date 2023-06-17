from pathlib import Path

from shared.config.Config import ConfigHandler

config_path = Path('./config/dev.json')

handler = ConfigHandler(config_path)
config = handler.load()
