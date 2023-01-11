"""
Copyright © psychemisss 2022-2023 - https://github.com/psychemisss
Description: S3 automatic backup tool
Version: 1.1.0
"""

import os
import sys
import shutil
import datetime
from dotenv import load_dotenv
from tools.Logger import Logger
load_dotenv()
log = Logger(__name__)


class FileManager:
    def __init__(self, current_path: str = os.getcwd()):
        self.backup_directory = os.getenv("BACKUP_TARGET_DIR")
        self.current_path = current_path

    def search_target_dir(self):
        """Function for searching target directory."""
        log.debug(f'Searching "{self.backup_directory}" directory...')
        for root, directories, files in os.walk(self.current_path):
            for directory in directories:
                if directory == self.backup_directory:
                    target_directory_path = os.path.join(root, directory)
                    log.success(f'Target directory found: "{target_directory_path}"')
                    return target_directory_path

        log.error('Target directory not found')
        sys.exit(1)

    def create_backup(self, target_directory_path: str):
        """Function for creating a backup of the directory."""
        log.debug('Creating backup...')
        backup_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_path = os.path.join(self.current_path, backup_name)
        shutil.make_archive(backup_path, "zip", target_directory_path)
        log.success(f'Backup "{backup_name}.zip" created successfully')
        return backup_path, backup_name

    def clear_backup(self, backup_path: str) -> None:
        """Function for clearing zip archives after backup."""
        log.debug('Clearing backup...')
        os.remove(backup_path + ".zip")

        if os.path.exists(backup_path):
            log.error('Backup not cleared')
        else:
            log.success('Backup cleared successfully')

    @property
    def config(self):
        """Function for loading configuration from .env file."""
        config = {}
        for key, value in os.environ.items():
            config[key] = value
            log.debug(f"{key}: {value}")
        return config
