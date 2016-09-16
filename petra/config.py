import os

import yaml

CONFIG_PATH = os.environ.get('CONFIG_PATH', 'config.yml')

with open(CONFIG_PATH, 'r') as config_file:
    config = yaml.load(config_file)
