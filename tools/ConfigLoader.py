"""
Copyright © psychemisss 2022-2023 - https://github.com/psychemisss
Description: S3 automatic backup tool
Version: 1.1.0
"""

import json
import sys
from functools import cache
from tools.Logger import Logger
log = Logger(__name__)


class ConfigLoader:
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file

    @property
    def profiles_count(self):
        with open(self.config_file, 'r') as f:
            data = json.load(f)
            return len(data)

    @property
    def config(self):
        """Function for loading configuration from json file."""
        try:
            with open(self.config_file) as f:
                config = json.load(f)
                log.debug(f'Configuration file "{self.config_file}" loaded successfully')
                return config
        except FileNotFoundError:
            log.error(f'Configuration file "{self.config_file}" not found')
            sys.exit(FileNotFoundError)

    @cache
    def unpack_profile(self, config_name: str) -> dict:
        """Function for unpacking configuration profile."""

        try:
            with open(self.config_file, 'r') as config_file:
                config = json.load(config_file)
                unpacked_config = config[config_name]
        except FileNotFoundError:
            log.error(f"Config file {self.config_file} not found")
            sys.exit(1)
        except KeyError:
            log.error(f"Config {config_name} not found")
            sys.exit(1)

        return unpacked_config
