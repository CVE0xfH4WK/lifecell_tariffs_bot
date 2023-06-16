from pathlib import Path

from config.Config import ConfigHandler

config_path = Path('./configs/dev.json')

handler = ConfigHandler(config_path)
config = handler.load()
